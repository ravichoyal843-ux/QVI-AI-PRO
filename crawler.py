from playwright.sync_api import sync_playwright
import os

BASE_URL = "https://www.myqvi.com"

os.makedirs("scraped", exist_ok=True)

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(BASE_URL)

    page.wait_for_timeout(3000)

    links = page.locator("a")

    found = set()

    for i in range(links.count()):

        href = links.nth(i).get_attribute("href")

        if href:
            if href.startswith("/"):
                href = BASE_URL + href

            if "myqvi.com" in href:
                found.add(href)

    print(f"\nFound {len(found)} pages\n")

    for url in sorted(found):

        try:

            print("Reading:", url)

            page.goto(url)

            page.wait_for_timeout(2000)

            text = page.locator("body").inner_text()

            filename = (
                url.replace("https://", "")
                   .replace("/", "_")
                   .replace("?", "_")
                   .replace("&", "_")
            )

            with open(f"scraped/{filename}.txt", "w", encoding="utf-8") as f:
                f.write(text)

        except Exception as e:
            print("Skipped:", url)

    browser.close()

print("\nFinished!")