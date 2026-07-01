import json
from playwright.sync_api import sync_playwright

from scrape_assessment import extract_assessment

# Read all links
with open("data/assessment_links.json", "r", encoding="utf8") as f:
    urls = json.load(f)

catalog = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for i, url in enumerate(urls, start=1):

        print(f"[{i}/{len(urls)}] Scraping: {url}")

        try:
            page.goto(url, wait_until="networkidle", timeout=60000)

            html = page.content()

            product = extract_assessment(html, url)

            catalog.append(product)

            print("✅", product["name"])

        except Exception as e:

            print("❌ Failed:", url)
            print(e)

    browser.close()

# Save catalog
with open("data/catalog.json", "w", encoding="utf8") as f:

    json.dump(
        catalog,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"\nSaved {len(catalog)} products to catalog.json")