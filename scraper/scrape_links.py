from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.shl.com"

CATALOG_URL = "https://www.shl.com/products/product-catalog/"


def get_links():

    links = set()

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(CATALOG_URL, wait_until="networkidle")

        page.wait_for_timeout(5000)

        soup = BeautifulSoup(page.content(), "html.parser")

        browser.close()

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if "/products/assessments/" in href:

            if href.startswith("/"):

                href = BASE_URL + href

            links.add(href)

    return sorted(links)


if __name__ == "__main__":

    links = get_links()

    # Remove category pages
    links = [
        link for link in links
        if not any(
            link.rstrip("/").endswith(page)
            for page in [
                "assessments",
                "behavioral-assessments",
                "personality-assessment",
                "cognitive-assessments",
                "job-focused-assessments",
                "skills-and-simulations",
                "business-skills",
                "call-center-simulations",
                "coding-simulations",
                "language-evaluation",
                "technical-skills",
                "assessment-and-development-centers",
                "universal-competency-framework",
            ]
        )
    ]

    print(f"Found {len(links)} assessment links")

    with open("data/assessment_links.json", "w", encoding="utf8") as f:
        json.dump(links, f, indent=4)

    print("Saved assessment_links.json")