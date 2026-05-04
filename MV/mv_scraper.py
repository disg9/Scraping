import os
import json
import re
import pdfplumber

PDF_PATH   = os.path.join("DATASHEET", "MV-family-datasheet_20240930_R1.pdf")
OUTPUT_DIR = "OUTPUT"
FAMILY     = "MV"

INDOOR_ROW_LABELS  = ["Camera type", "Sensor and resolution",
                       "Field of view", "Storage",
                       "IR illumination", "Best for"]

OUTDOOR_ROW_LABELS = ["Camera type", "Sensor and resolution",
                       "Field of view", "Storage", "Ratings",
                       "IR illumination", "Best for"]


def extract_overview(pdf):
    text = pdf.pages[0].extract_text() or ""
    if "Overview" in text:
        overview = text.split("Overview")[-1].strip()
        return overview.replace("MERAKI.COM", "").strip()
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
        elif current and line and "MERAKI" not in line and "DATASHEET" not in line:
            current += " " + line
    if current:
        features.append(current)
    return features


def parse_mv_table(table, row_labels):
    if not table or len(table) < 2:
        return {}

    header_row = table[0]

    col_models = {}
    for col_idx in range(1, len(header_row)):
        cell = header_row[col_idx]
        if not cell:
            continue
        raw_names = [n.strip() for n in cell.split("\n") if n.strip()]
        models = []
        for name in raw_names:
            clean = re.sub(r'\s*-\s*HW$', '', name).strip()
            clean = re.sub(r'HW$', '', clean).strip().rstrip('-').strip()
            if clean:
                models.append(clean)
        if models:
            col_models[col_idx] = models

    if not col_models:
        return {}

    all_models = {}
    for col_idx, model_list in col_models.items():
        for model in model_list:
            all_models[model] = {"_col": col_idx, "_siblings": model_list}

    data_rows = table[1:]
    for row_pos, row in enumerate(data_rows):
        if row_pos >= len(row_labels):
            break
        label = row_labels[row_pos]

        for col_idx, model_list in col_models.items():
            if col_idx >= len(row):
                continue
            raw_val = row[col_idx]
            if raw_val is None:
                for c in range(1, len(row)):
                    if row[c] is not None:
                        raw_val = row[c]
                        break
            if raw_val is None:
                continue

            value = raw_val.strip()
            lines = [l.strip() for l in value.split("\n") if l.strip()]

            for model in model_list:
                if model in all_models:
                    all_models[model][label] = lines if len(lines) > 1 else value

    result = {}
    for model, specs in all_models.items():
        clean_specs = {k: v for k, v in specs.items()
                       if not k.startswith("_")}
        result[model] = clean_specs

    return result


def get_environment(page_text):
    text = (page_text or "").lower()
    if "outdoor" in text:
        return "Outdoor"
    return "Indoor"


def build_product_url(model_name):
    slug = model_name.lower().replace(" ", "-")
    return f"https://meraki.cisco.com/products/cameras/{slug}/"


def extract_mv_products(pdf_path):
    PAGE_CONFIG = {
        7: ("Indoor",  INDOOR_ROW_LABELS),
        8: ("Indoor",  INDOOR_ROW_LABELS),
        9: ("Outdoor", OUTDOOR_ROW_LABELS),
    }

    all_products = []

    with pdfplumber.open(pdf_path) as pdf:
        print("Reading family overview and features...")
        overview = extract_overview(pdf)
        features = extract_features(pdf)
        print(f"Overview: {len(overview)} chars")
        print(f"Features: {len(features)} items")

        print("\nScanning product tables (pages 8-10)...")

        for page_idx, (environment, row_labels) in PAGE_CONFIG.items():
            page      = pdf.pages[page_idx]
            page_text = page.extract_text() or ""
            tables    = page.extract_tables()

            if not tables:
                continue

            for table in tables:
                parsed = parse_mv_table(table, row_labels)

                for model_name, specs in parsed.items():
                    if not model_name or not specs:
                        continue

                    entry = {
                        "family":  FAMILY,
                        "name":    model_name,
                        "url":     build_product_url(model_name),
                        "images":  [],
                        "content": {
                            "Overview":    overview,
                            "Features":    features,
                            "Environment": environment,
                            "Specifications": {
                                "Camera Type":          specs.get("Camera type", ""),
                                "Sensor and Resolution":specs.get("Sensor and resolution", ""),
                                "Field of View":        specs.get("Field of view", ""),
                                "Storage":              specs.get("Storage", ""),
                                "IR Illumination":      specs.get("IR illumination", ""),
                                "Ratings":              specs.get("Ratings", "N/A"),
                                "Management":           "Cloud-managed via Meraki dashboard",
                                "Connectivity":         "Wired (PoE) + integrated wireless",
                            },
                            "Usage":       specs.get("Best for", ""),
                            "Performance": {
                                "Sensor and Resolution": specs.get("Sensor and resolution", ""),
                                "Field of View":         specs.get("Field of view", ""),
                                "IR Illumination":       specs.get("IR illumination", ""),
                            }
                        }
                    }

                    all_products.append(entry)
                    print(f"{model_name:<18}  ({environment})")

    return all_products


def save_products(products, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    saved = []
    seen  = set()

    for product in products:
        name = product["name"]
        if name in seen:
            continue
        seen.add(name)

        filename = f"{name}.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(product, f, indent=2, ensure_ascii=False)
        saved.append(name)

    combined_path = os.path.join(output_dir, "MV_family_all_products.json")
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump([p for p in products if p["name"] in saved],
                  f, indent=2, ensure_ascii=False)

    return saved, combined_path


def main():
    print("=" * 55)
    print("Cisco MV Family Datasheet Scraper")
    print("=" * 55)

    if not os.path.exists(PDF_PATH):
        print(f"\nERROR: PDF not found at  →  {PDF_PATH}")
        print("Put the datasheet inside a DATASHEET/ folder.\n")
        return

    products = extract_mv_products(PDF_PATH)

    if not products:
        print("\nNo products extracted.")
        return

    print(f"\nSaving {len(products)} products to {OUTPUT_DIR}/...")
    saved, combined_path = save_products(products, OUTPUT_DIR)

    print("\n" + "=" * 55)
    print("ALL DONE!")
    print("=" * 55)
    print(f"Products saved : {len(saved)}")
    print(f"Combined file  : {combined_path}")
    print(f"\nProducts extracted:")
    for name in saved:
        print(f"• {name}")
    print()
    print("Note on images:")
    print("PDFs contain no image URLs. The 'images' field is empty.")
    print("=" * 55)


if __name__ == "__main__":
    main()