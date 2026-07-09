import json
import requests
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:1.7b"

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


def parse_with_qwen(description_text, benefits_text=None, max_retries=2):
    if not description_text:
        return None

    MAX_DESC_LEN = 6000
    trimmed = description_text[:MAX_DESC_LEN]
    if benefits_text:
        trimmed += "\n\nJob benefits:\n" + benefits_text[:2000]

    payload = {
        "model": MODEL,
        "prompt": PARSING_PROMPT + trimmed,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 2048}
    }

    for attempt in range(max_retries):
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=180)
            resp.raise_for_status()
            text = resp.json().get("response", "").strip()
            text = text.removeprefix("```json").removeprefix("```\n").removeprefix("```").strip()
            text = text.removesuffix("```").strip()
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                print(f"  [Qwen] JSON decode failed, raw output (first 300 chars): {text[:300]}")
                return None
        except requests.exceptions.Timeout:
            print(f"  [Qwen] Timeout on attempt {attempt + 1}")
        except Exception as e:
            print(f"  [Qwen] Error: {e}")
        time.sleep(2)

    return None