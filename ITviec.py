from bs4 import BeautifulSoup
import cloudscraper
import json
from pathlib import Path
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_AVAILABLE = False
gemini_client = None
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key != "your_api_key_here":
        gemini_client = genai.Client(api_key=api_key)
        GEMINI_AVAILABLE = True
except Exception as e:
    print(f"[Gemini] Init failed: {e}")

PARSING_PROMPT = """You are a job description parser. Extract structured information from the job description below.
Return ONLY valid JSON (no markdown, no code fences) matching this schema:
{
  "responsibilities": [],
  "requirements": [],
  "benefits": [],
  "hard_skills": [],
  "soft_skills": [],
  "programming_languages": [],
  "frameworks": [],
  "databases": [],
  "cloud": [],
  "tools": [],
  "experience_years": 0,
  "education": "",
  "english_level": ""
}

Rules:
- fields MUST be arrays of strings (or number/integer for experience_years)
- If a field has no data, return empty array [] (or 0 for experience_years, "" for education/english_level)
- hard_skills: technical abilities (e.g., "CI/CD", "REST API", "Testing")
- soft_skills: interpersonal skills (e.g., "Teamwork", "Communication", "Problem-solving")
- programming_languages: e.g., "Python", "Java", "JavaScript"
- frameworks: e.g., "Spring Boot", "React", "Django"
- education: degree/certification required (e.g., "Bachelor's degree in Computer Science")
- english_level: "Native", "Fluent", "Advanced", "Intermediate", "Basic", or ""
- experience_years: minimum years of experience required (0 if none)

Job description:
"""

try:
    from database import get_posting, close_db
    DB_AVAILABLE = True
except ImportError:
    get_posting = None
    close_db = None
    DB_AVAILABLE = False

def parse_description(description_text):
    if not GEMINI_AVAILABLE or not description_text:
        return None
    MAX_DESC_LEN = 6000
    trimmed = description_text[:MAX_DESC_LEN]
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=PARSING_PROMPT + trimmed
        )
        text = response.text.strip()
        text = text.removeprefix("```json").removeprefix("```\n").removesuffix("```").strip()
        return json.loads(text)
    except Exception as e:
        print(f"[Gemini] Parse error: {e}")
        return None


def get_job_urls(keyword):
    scraper = cloudscraper.create_scraper()
    urls = []
    page = 1
    while True:   
        resp = scraper.get(f"https://itviec.com/it-jobs?query={keyword}&page={page}")
        if resp.status_code != 200: continue
        soup = BeautifulSoup(resp.text, "html.parser")
        script = soup.find("script", type="application/ld+json")
        if script and script.string:
            data = json.loads(script.string)
            urls.extend([item["url"] for item in data.get("itemListElement", []) if "url" in item])   
        next_page = soup.find("a", rel="next")
        if not next_page:
            break
        page += 1
        time.sleep(2) 
        
    return {
        "urls": urls,
        "total": len(urls),
        "time": time.time()
    }

def get_job_details(url, crawl_time):
    scraper = cloudscraper.create_scraper()
    resp = scraper.get(url)
    if resp.status_code != 200:
        return None
    soup = BeautifulSoup(resp.text, "html.parser")
    script = soup.find("script", type="application/ld+json")
    if script and script.string:
        data = json.loads(script.string)
        locations_raw = data.get("jobLocation") or []
        if not isinstance(locations_raw, list):
            locations_raw = [locations_raw]
        locations = []
        for loc in locations_raw:
            addr = loc.get("address", {})
            locations.append({
                "street": addr.get("streetAddress"),
                "city": addr.get("addressLocality"),
                "region": addr.get("addressRegion"),
                "country": addr.get("addressCountry"),
            })
        salary_data = data.get("baseSalary", {}).get("value", {})
        try:
            salary_min = float(salary_data.get("minValue")) if salary_data.get("minValue") else None
        except (TypeError, ValueError):
            salary_min = None
        try:
            salary_max = float(salary_data.get("maxValue")) if salary_data.get("maxValue") else None
        except (TypeError, ValueError):
            salary_max = None
        job_data = {
            "title": data.get("title"),
            "updated_at": crawl_time,
            "industry": data.get("industry"),
            "date_posted": datetime.strptime(
                data.get("datePosted"),
                "%Y-%m-%d"
            ).date(),
            "valid_through": datetime.strptime(
                data.get("validThrough"),
                "%Y-%m-%d"
            ).date(),
            "description": BeautifulSoup(
                data.get("description", ""),
                "html.parser"
            ).get_text(separator="\n", strip=True),
            "skills_list": [
                skill.strip()
                for skill in data.get("skills", "").split(",")
                if skill.strip()
            ],
            "employment_type": data.get("employmentType"),
            "location": locations,
            "salary": {
                "currency": data.get("baseSalary", {}).get("currency"),
                "unit": salary_data.get("unitText"),
                "min": salary_min,
                "max": salary_max,
            },
            "benefits": BeautifulSoup(
                data.get("jobBenefits", ""),
                "html.parser"
            ).get_text(separator="\n", strip=True),
            "company": data.get("hiringOrganization", {}).get("name"),
            "source": "itviec",
            "url": url
        }
        return job_data
    return None



def main():
    keyword = "developer"
    result = get_job_urls(keyword)
    urls = result["urls"]
    crawl_time = result["time"]
    results = []

    posting = None
    if DB_AVAILABLE:
        try:
            posting = get_posting()
        except Exception as e:
            print(f"  DB connect failed: {e}")

    for i, url in enumerate(urls, 1):
        job = get_job_details(url, crawl_time=crawl_time)
        if job:
            if GEMINI_AVAILABLE:
                parsed = parse_description(job.get("description", ""))
                if parsed:
                    job["parsed"] = parsed
                else:
                    print(f"  Gemini: parse failed")
            results.append(job)
            if posting is not None:
                try:
                    posting.update_one({"url": job["url"]}, {"$set": job}, upsert=True)
                except Exception as e:
                    print(f"  DB save skipped: {e}")
            print(f"  OK: {job['title']} @ {job['company']}")

    if posting is not None:
        close_db()

    Path("results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nDone! {len(results)} jobs saved to results.json")


if __name__ == "__main__":
    main()
