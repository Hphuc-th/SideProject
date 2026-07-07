from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import cloudscraper
import json
from pathlib import Path

try:
    from database import posting
    DB_AVAILABLE = True
except:
    posting = None
    DB_AVAILABLE = False


def get_search_results(keyword="developer"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto(
            f"https://itviec.com/it-jobs?query={keyword}",
            wait_until="domcontentloaded",
        )
        page.wait_for_selector("#query", timeout=120000)
        page.wait_for_timeout(3000)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    for script in soup.find_all("script", type="application/ld+json"):
        data = json.loads(script.string)
        if data.get("@type") == "ItemList":
            for item in data.get("itemListElement", []):
                jobs.append(item["url"])

    print(f"Found {len(jobs)} job URLs")
    return jobs


def get_job_details(url):
    """cloudscraper -> fetch từng job page -> parse JobPosting JSON-LD."""
    scraper = cloudscraper.create_scraper()
    resp = scraper.get(url)
    if resp.status_code != 200:
        return None

    soup = BeautifulSoup(resp.text, "html.parser")
    for script in soup.find_all("script", type="application/ld+json"):
        data = json.loads(script.string)
        if data.get("@type") == "JobPosting":
            org = data.get("hiringOrganization", {})
            salary_data = data.get("baseSalary")
            salary = None
            if salary_data:
                v = salary_data.get("value", {})
                salary = {
                    "currency": salary_data.get("currency"),
                    "min": v.get("minValue"),
                    "max": v.get("maxValue"),
                    "unit": v.get("unitText"),
                    "text": v.get("value"),
                }

            locations = data.get("jobLocation") or []
            if not isinstance(locations, list):
                locations = [locations]
            location = []
            for loc in locations:
                addr = loc.get("address", {})
                location.append(
                    {
                        "street": addr.get("streetAddress"),
                        "city": addr.get("addressLocality"),
                        "region": addr.get("addressRegion"),
                    }
                )

            return {
                "title": data.get("title"),
                "company": org.get("name") if isinstance(org, dict) else org,
                "company_logo": org.get("logo") if isinstance(org, dict) else None,
                "location": location,
                "salary": salary,
                "skills": data.get("skills", ""),
                "employment_type": data.get("employmentType"),
                "description": BeautifulSoup(
                    data.get("description", ""), "html.parser"
                ).get_text(separator="\n",strip=True),
                "benefits": BeautifulSoup(
                    data.get("jobBenefits", ""), "html.parser"
                ).get_text(separator="\n",strip=True),
                "date_posted": data.get("datePosted"),
                "url": url,
                "source": "itviec",
            }

    return None


def main():
    keyword = "developer"
    urls = get_search_results(keyword)

    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url.split('/')[-1][:50]}...")
        job = get_job_details(url)
        if job:
            results.append(job)
            if DB_AVAILABLE:
                posting.update_one({"url": job["url"]}, {"$set": job}, upsert=True)
            print(f"  OK: {job['title']} @ {job['company']}")

    Path("results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nDone! {len(results)} jobs saved to results.json")


if __name__ == "__main__":
    main()
