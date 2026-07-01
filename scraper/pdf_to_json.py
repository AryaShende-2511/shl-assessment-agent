import pdfplumber
import json
import re

PDF_PATH = "data/shl_cat.pdf"

text = ""

with pdfplumber.open(PDF_PATH) as pdf:
    print("Total pages:", len(pdf.pages))

    for page in pdf.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"

print("Total characters:", len(text))

with open("all_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("✅ all_text.txt saved")