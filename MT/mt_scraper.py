

import os
import json
import pdfplumber 

 
PDF_PATH   = os.path.join("DATASHEET", "MT-family-datasheet-20230905-english.pdf")
OUTPUT_DIR = "OUTPUT"
FAMILY     = "MT"
 
def extract_overview(pdf):
    text = pdf.pages[0].extract_text() or ""
    if "Overview" in text:
        overview = text.split("Overview")[-1].strip()
        overview = overview.replace("MERAKI.COM", "").strip()
        # Stop before the key benefits checklist
        if "Smart sensors" in overview:
            overview = overview.split("Smart sensors")[0].strip()
        return overview
    return ""


 
def extract_features(pdf):
    text = pdf.pages[1].extract_text() or ""
    features = []
    current = ""
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("•"):
            if current:
                features.append(current)
            current = line.lstrip("•").strip()
        elif current and line and not line.startswith("MT FAMILY") and not line.startswith("MERAKI"):
         
            current += " " + line
    if current:
        features.append(current)
    return features



 
def extract_key_benefits(pdf):
    text = pdf.pages[0].extract_text() or ""
    benefits = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("✓"):
            benefit = line.lstrip("✓").strip()
            if benefit:
                benefits.append(benefit)
    return benefits


 
def extract_products_and_accessories(pdf):
    page       = pdf.pages[9]    # page 10 (0-indexed = 9)
    tables     = page.extract_tables()
    full_text  = page.extract_text() or ""

    products    = {}  
    accessories = {}   

    for table in tables:
        for row in table:
            if not row or not row[0]:
                continue
            sku  = row[0].strip()
            desc = (row[1] or "").strip()

            if sku.startswith("MT") and "-HW" in sku:
                
                model = sku.replace("-HW", "")
                products[model] = {
                    "sku":         sku,
                    "description": desc
                }
            elif sku.startswith("MA-"):
                accessories[sku] = desc

    notes = []
    in_notes = False
    for line in full_text.split("\n"):
        line = line.strip()
        if line.lower().startswith("notes"):
            in_notes = True
            continue
        if in_notes and line.startswith("•"):
            note = line.lstrip("•").strip()
            if note:
                notes.append(note)

    return products, accessories, notes


def match_accessories_to_products(notes, accessories):
    """
    Returns dict: { "MT11": ["MA-CBL-TEMP-ME-1", "MA-CBL-TEMP-GL-1"], ... }
    """
    product_accessories = {}
    for note in notes:
        
        model = None
        for word in note.split():
            clean = word.strip(".,;")
            if clean.startswith("MT") and "-HW" in clean:
                model = clean.replace("-HW", "")
                break
        if not model:
            continue

     
        acc_codes = [w.strip(".,;()") for w in note.split()
                     if w.strip(".,;()").startswith("MA-")]

        if acc_codes:
            if model not in product_accessories:
                product_accessories[model] = []
            for code in acc_codes:
                if code in accessories and code not in product_accessories[model]:
                    product_accessories[model].append(code)

    return product_accessories



 
def build_product_url(model_name):
    slug = model_name.lower()
    return f"https://meraki.cisco.com/products/sensors/{slug}/"


 
 
def build_product_entries(products, accessories, product_accessories,
                          overview, features, key_benefits):
    entries = []
    for model, info in products.items():
       
        acc_list = []
        for code in product_accessories.get(model, []):
            acc_list.append({
                "sku":         code,
                "description": accessories.get(code, "")
            })

        entry = {
            "family": FAMILY,
            "name":   model,
            "url":    build_product_url(model),
            "images": [],    
            "content": {
                "Overview":     overview,
                "Key Benefits": key_benefits,
                "Features":     features,
                "Specifications": {
                    "SKU":          info["sku"],
                    "Description":  info["description"],
                    "Connectivity": "Bluetooth Low Energy (BLE) to MR/MV gateway",
                    "Management":   "Cloud-managed via Meraki dashboard",
                    "Data Export":  ".csv, .xls, API, MQTT",
                    "Local Storage":"Up to 5 days onboard",
                    "Alerts":       "SMS, email, push notification, webhook",
                },
                "Usage":        info["description"],
                "Accessories":  acc_list,
                "Licensing": {
                    "SKU":         "LIC-MT-XY",
                    "Description": "Meraki MT Enterprise license (X = 1, 3, 5, 7 years)"
                }
            }
        }
        entries.append(entry)
        print(f"   ✓ {model:<10}  →  {info['description']}")

    return entries


 
 
def save_products(entries, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    saved = []
    for entry in entries:
        name     = entry["name"]
        filename = f"{name}.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2, ensure_ascii=False)
        saved.append(name)

    combined_path = os.path.join(output_dir, "MT_family_all_products.json")
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    return saved, combined_path



 
def main():
    print("=" * 55)
    print("  Cisco MT Family Datasheet Scraper")
    print("=" * 55)

    if not os.path.exists(PDF_PATH):
        print(f"\n ERROR: PDF not found at  →  {PDF_PATH}")
        print("   Put the datasheet inside a DATASHEET/ folder.\n")
        return

    with pdfplumber.open(PDF_PATH) as pdf:
        print("\n Extracting family overview and features...")
        overview     = extract_overview(pdf)
        features     = extract_features(pdf)
        key_benefits = extract_key_benefits(pdf)
        print(f"   ✓ Overview: {len(overview)} chars")
        print(f"   ✓ Key benefits: {len(key_benefits)} items")
        print(f"   ✓ Feature highlights: {len(features)} items")

        print("\nExtracting products from ordering table (page 10)...")
        products, accessories, notes = extract_products_and_accessories(pdf)
        print(f"    Hardware products found: {len(products)}")
        print(f"    Accessories found: {len(accessories)}")

        product_accessories = match_accessories_to_products(notes, accessories)

        print("\n Building product entries...")
        entries = build_product_entries(
            products, accessories, product_accessories,
            overview, features, key_benefits
        )

    print(f"\nSaving {len(entries)} products to {OUTPUT_DIR}/...")
    saved, combined_path = save_products(entries, OUTPUT_DIR)

    print("\n" + "=" * 55)
    print("  ALL DONE")
    print("=" * 55)
    print(f"  Products saved : {len(saved)}")
    print(f"  Combined file  : {combined_path}")
    print(f"\n  Products extracted:")
    for name in saved:
        print(f"    • {name}")
    print()
    print("  Note on images:")
    print("     PDFs contain no image URLs. The 'images' field")
    print("     is empty. A web scraper visiting meraki.cisco.com")
    print("     would be needed to populate it.")
    print()
    print("  Note on specs:")
    print("     The MT datasheet does not contain per-product")
    print("     spec tables (unlike MR). Detailed specs like")
    print("     operating temperature, battery life, and sensor")
    print("     range would need to be scraped from individual")
    print("     product pages on meraki.cisco.com.")
    print("=" * 55)


if __name__ == "__main__":
    main()
