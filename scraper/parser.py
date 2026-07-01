import re
import json

# Read the extracted text
with open("all_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Find every catalog object
pattern = r'\{\s*"entity_id".*?\n\s*\}'

matches = re.findall(pattern, text, flags=re.DOTALL)

print("Objects found:", len(matches))

products = []

for obj in matches:
    try:
        # Remove PDF line-break hyphens
        obj = re.sub(r'-\n', '', obj)

        # Join wrapped lines inside strings
        obj = re.sub(r'\n\s*', ' ', obj)

        # Remove strange unicode if present
        obj = obj.replace("￾", "")
                # Remove strange PDF hyphen character
        obj = obj.replace("￾", "-")

        product = json.loads(obj)

        products.append(product)

    except Exception:
        continue

print("Parsed:", len(products))

with open("data/catalog.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=4, ensure_ascii=False)

print("✅ catalog.json saved")