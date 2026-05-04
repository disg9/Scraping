

import os
import json
import re
import pdfplumber


 
 
PDF_PATH   = os.path.join("DATASHEET", "MR-family-datasheet-20250205-english.pdf")
OUTPUT_DIR = "OUTPUT"
FAMILY     = "MR"
FAMILY_URL = "https://meraki.cisco.com/products/wi-fi/"


 

 
def extract_family_overview(pdf):

    overview_text = ""
    page1_text = pdf.pages[0].extract_text() or ""
    if "Overview" in page1_text:
        overview_text = page1_text.split("Overview")[-1].strip()
        overview_text = overview_text.replace("MERAKI.COM", "").strip()


    features = []
    page3_text = pdf.pages[2].extract_text() or ""
    for line in page3_text.split("\n"):
        line = line.strip()
        if line.startswith("•"):
            feature = line.lstrip("•").strip()
            if feature and len(feature) > 5:
                features.append(feature)

    return overview_text, features

 
MODEL_TOKEN_RE = re.compile(r'^[A-Z0-9][A-Z0-9/]{2,14}$')

def extract_model_names_from_text(page_text, num_products):
    """
    Returns a list of exactly num_products model-name tokens found
    on a single line of page_text, or None if no such line exists.
    """
    for line in (page_text or "").split("\n"):
        tokens = line.strip().split()
        if (len(tokens) == num_products
                and all(MODEL_TOKEN_RE.match(t) for t in tokens)):
            return tokens
    return None



 
def parse_product_table(table, model_names_from_page=None):
    """
    Returns dict: { model_name: { spec_label: value_or_list, ... }, ... }
    """
    if not table or len(table) < 2:
        return {}

    header_row = table[0]
    first_cell = (header_row[0] or "").strip()

    if model_names_from_page and first_cell:
  
        product_names = model_names_from_page[:]
        data_rows     = table           
    else:
        
        product_names = []
        for cell in header_row[1:]:
            if cell:
                name = cell.replace("*", "").replace("\n", " ").strip()
                product_names.append(name)
            else:
                product_names.append(None)

        while product_names and product_names[-1] is None:
            product_names.pop()

        data_rows = table[1:]         

    if not product_names:
        return {}

    products = {name: {} for name in product_names if name}

    for row in data_rows:
        spec_label = (row[0] or "").replace("\n", " ").strip()
        if not spec_label:
            continue

        for col_idx, product_name in enumerate(product_names):
            if product_name is None:
                continue

            raw_col = col_idx + 1
            if raw_col >= len(row):
                continue

            cell_value = row[raw_col]

            
            if cell_value is None:
                for c in row[1:]:
                    if c is not None:
                        cell_value = c
                        break

            if cell_value is None:
                continue

            value = cell_value.strip()
            lines = [l.strip() for l in value.split("\n") if l.strip()]
            products[product_name][spec_label] = (
                lines if len(lines) > 1 else value
            )

    return products



 
def get_wifi_generation(page_text):
    text = (page_text or "").lower()
    if "wi-fi 7" in text:
        return "Wi-Fi 7"
    elif "wi-fi 6e" in text or "6e" in text:
        return "Wi-Fi 6E"
    elif "outdoor" in text:
        return "Wi-Fi 6 (Outdoor)"
    else:
        return "Wi-Fi 6 (Indoor)"


 

 
def build_product_url(product_name):
    slug = product_name.lower().replace(" ", "-").replace("/", "-")
    return f"https://meraki.cisco.com/products/wi-fi/{slug}/"


 

 
def extract_mr_products(pdf_path):
    """
    Reads the PDF and returns a list of product dicts.
    """
    PRODUCT_TABLE_PAGES = list(range(12, 23))   
    WIFI7_PAGE_INDICES  = {12, 13}              

    all_products = []

    with pdfplumber.open(pdf_path) as pdf:

        print(" Reading family overview and features...")
        overview_text, family_features = extract_family_overview(pdf)
        print(f"   ✓ Overview: {len(overview_text)} chars")
        print(f"   ✓ Features: {len(family_features)} items")

        print("\n Scanning product tables...")

        for page_idx in PRODUCT_TABLE_PAGES:
            if page_idx >= len(pdf.pages):
                break

            page      = pdf.pages[page_idx]
            page_text = page.extract_text() or ""
            tables    = page.extract_tables()

            if not tables:
                continue

            wifi_gen = get_wifi_generation(page_text)

            for table in tables:
                if not table or len(table[0]) < 3:
                    continue    

               
                if page_idx in WIFI7_PAGE_INDICES:
                    num_products = len(table[0]) - 1
                    model_names  = extract_model_names_from_text(page_text, num_products)
                else:
                    model_names = None

                parsed = parse_product_table(table, model_names_from_page=model_names)

                for product_name, specs in parsed.items():
                    if not product_name or not specs:
                        continue

                   
                    sub_names = [n.strip() for n in re.split(r'\s+/\s+', product_name)]

                    for sub_name in sub_names:
                        if not sub_name:
                            continue

                        product_entry = {
                            "family": FAMILY,
                            "name":   sub_name,
                            "url":    build_product_url(sub_name),
                            "images": [],   # images need separate web scraping
                            "content": {
                                "Overview":         overview_text,
                                "Wi-Fi Generation": wifi_gen,
                                "Features":         family_features,
                                "Specifications":   specs,
                                "Usage":            specs.get("Usage", ""),
                                "Performance": {
                                    "Radio Specification":  specs.get("Radio specification", ""),
                                    "Aggregate Frame Rate": specs.get("Aggregate frame rate", ""),
                                    "Spatial Streams":      specs.get("Spatial streams", ""),
                                    "Performance Features": specs.get("Performance features", ""),
                                }
                            }
                        }

                        all_products.append(product_entry)
                        print(f"   ✓ {sub_name:<18}  ({wifi_gen})")

    return all_products



 
def save_products(products, output_dir):
    """
    Writes:
      OUTPUT/<ModelName>.json          – one per unique product
      OUTPUT/MR_family_all_products.json  – all products combined
    """
    os.makedirs(output_dir, exist_ok=True)

    saved_names = []
    seen        = set()

    for product in products:
        name = product["name"]
        if name in seen:
            continue
        seen.add(name)

        filename = f"{name.replace(' ', '_').replace('/', '-')}.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(product, f, indent=2, ensure_ascii=False)
        saved_names.append(name)

    unique_products = [p for p in products if p["name"] in saved_names]
    combined_path   = os.path.join(output_dir, "MR_family_all_products.json")
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(unique_products, f, indent=2, ensure_ascii=False)

    return saved_names, combined_path

 
def main():
    print("=" * 55)
    print("  Cisco MR Family Datasheet Scraper")
    print("=" * 55)

    if not os.path.exists(PDF_PATH):
        print(f"\n ERROR: PDF not found at  →  {PDF_PATH}")
        print("   Put the datasheet inside a DATASHEET/ folder.\n")
        return

    products = extract_mr_products(PDF_PATH)

    if not products:
        print("\n  No products extracted.")
        return

    print(f"\n Saving {len(products)} products to {OUTPUT_DIR}/...")
    saved_names, combined_path = save_products(products, OUTPUT_DIR)

    print("\n" + "=" * 55)
    print("   ALL DONE!")
    print("=" * 55)
    print(f"  Products saved : {len(saved_names)}")
    print(f"  Combined file  : {combined_path}")
    print(f"\n  Products extracted:")
    for name in saved_names:
        print(f"    • {name}")
    print()
    print("  Note on images:")
    print("     PDFs don't contain image URLs. To populate the")
    print("     'images' field, a separate web scraper would")
    print("     visit each product's page on meraki.cisco.com.")
    print("=" * 55)


if __name__ == "__main__":
    main()
