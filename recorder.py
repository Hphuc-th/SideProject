import json
from pathlib import Path
from playwright.sync_api import sync_playwright


class NetworkRecorder:
    def __init__(self):
        self.requests = []
        self.cookies = {}

    def on_request(self, request):
        if request.resource_type not in ["xhr", "fetch"]:
            return

        item = {
            "method": request.method,
            "url": request.url,
            "resource_type": request.resource_type,
            "headers": dict(request.headers),
            "post_data": request.post_data,
            "response": None,
        }

        self.requests.append(item)

        print(f"[REQUEST] {request.method} {request.url}")

    def on_response(self, response):
        if response.request.resource_type not in ["xhr", "fetch"]:
            return

        url = response.url

        for req in reversed(self.requests):
            if req["url"] == url:
                req["status"] = response.status

                try:
                    req["response"] = response.json()
                except Exception:
                    try:
                        req["response"] = response.text()
                    except Exception:
                        req["response"] = None

                print(f"[RESPONSE] {response.status} {url}")
                break

    def save(self, filename="network_log.json"):
        data = {
            "cookies": self.cookies,
            "requests": self.requests,
        }

        Path(filename).write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        print(f"\nSaved to {filename}")


def main():
    recorder = NetworkRecorder()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
        )

        context = browser.new_context()

        page = context.new_page()

        page.on("request", recorder.on_request)
        page.on("response", recorder.on_response)

        page.goto("https://itviec.com")

        page.wait_for_timeout(10000)

        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except:
            print("networkidle timeout on first page, continuing...")

        page.locator("input[name='query']").fill("developer")

        page.keyboard.press("Enter")

        page.wait_for_timeout(8000)

        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except:
            print("networkidle timeout on search page, continuing...")

        recorder.cookies = {
            c["name"]: c["value"]
            for c in context.cookies()
        }

        browser.close()

    recorder.save()


if __name__ == "__main__":
    main()
