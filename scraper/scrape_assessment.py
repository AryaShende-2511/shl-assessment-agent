import re
from bs4 import BeautifulSoup


def extract_assessment(html: str, url: str):
    soup = BeautifulSoup(html, "html.parser")

    data = {
        "name": "",
        "url": url,
        "description": "",
        "duration_minutes": None,
        "languages": None,
        "features": [],
        "sections": {}
    }
    # --------------------------
    # Name
    # --------------------------
    h1 = soup.find("h1")
    if h1:
        data["name"] = h1.get_text(strip=True)

    # --------------------------
    # Banner Description
    # --------------------------
    desc = soup.find("p", class_="-banner-text")
    if desc:
        data["description"] = desc.get_text(" ", strip=True)

    text = soup.get_text(" ", strip=True)

    # --------------------------
    # Duration
    # --------------------------
    m = re.search(r'(\d+)\s*minutes?', text, re.I)
    if m:
        data["duration_minutes"] = int(m.group(1))

    # --------------------------
    # Languages
    # --------------------------
    m = re.search(r'(\d+)\s*languages', text, re.I)
    if m:
        data["languages"] = int(m.group(1))

    # --------------------------
    # Features
    # --------------------------
    content = soup.find("div", class_="general-content__row")

# --------------------------
# Features
# --------------------------
    data["features"] = []

    blocks = soup.select("div.general-content__content")

    for block in blocks:
        for li in block.find_all("li"):
            text = li.get_text(" ", strip=True)

            if text and text not in data["features"]:
                data["features"].append(text)

    # --------------------------
    # Detail Sections
    # --------------------------
    for detail in soup.find_all("details"):

        heading = detail.find("h3")
        para = detail.find("p")

        if heading and para:

            data["sections"][heading.get_text(strip=True)] = para.get_text(
                " ",
                strip=True
            )

    return data