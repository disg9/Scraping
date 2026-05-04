

import os, re, json
import pdfplumber

DATASHEET_FOLDER = os.path.join("COSOL", "DATASHEET")
OUTPUT_FOLDER    = os.path.join("COSOL", "OUTPUT")



FAMILY_OVERVIEW = (
    "Cisco offers a broad range of cloud-managed switches designed to be easy to manage "
    "without compromising the power and flexibility traditionally found in enterprise-class switches. "
    "All models are managed through the Meraki Dashboard — an elegant, intuitive cloud interface "
    "that frees administrators to spend less time on configuration and more time on business needs. "
    "The portfolio spans access and aggregation switches from basic Layer 2 to high-performance "
    "Layer 3, covering MS130/MS150 (cost-effective access), MS210/MS225 (stackable access), "
    "Catalyst 9200L-M/9300-M (advanced campus), and MS450 (40G fiber aggregation)."
)

FAMILY_FEATURES = [
    "Wide range of models for campus, branch, and rugged environments — basic Layer 2 to high-performance Layer 3",
    "Up to 10 GbE access ports and 100 GbE uplinks for scalable deployments",
    "True zero-touch configuration that scales with organizational needs",
    "Integrated troubleshooting, logging, and alerting to lower operational costs",
    "Energy-efficient, low-noise design with fanless options",
    "Cloud management for reduced cost, overhead, and faster issue resolution",
    "Advanced security with IEEE 802.1x, MAC-based RADIUS authentication, and multiple admin roles",
    "QoS to prioritize critical traffic like voice and video",
    "Link Aggregation (LACP) and Rapid Spanning Tree Protocol (RSTP) for high availability",
    "Voice VLAN, DHCP snooping, and IGMP snooping to optimize and secure network traffic",
    "StackPower, advanced physical stacking, multigigabit, and UPOE+ options on select models",
    "Virtual stacking to manage thousands of ports from a single dashboard",
    "Layer 7 fingerprinting — identify hundreds of applications per client",
    "Rogue DHCP server detection across the entire network",
    "Remote cable testing and packet capture for rapid troubleshooting",
    "Adaptive Policy Segmentation on select models",
    "Limited lifetime hardware warranty with next-day advance replacement (Meraki MS models)",
]

FAMILY_USAGE = (
    "Deployed in branch offices, campus environments, retail stores, hospitals, and industrial "
    "locations. The MS130/MS130R series suits small/compact and rugged deployments. The MS150 "
    "adds multigigabit for Wi-Fi 7 backhaul. MS210/MS225 provide stackable campus access. "
    "Catalyst 9200L-M and 9300-M/9300L-M/9300X-M deliver advanced enterprise switching. "
    "MS450 provides 40G fiber aggregation for large campuses."
)



SPEC_PAGES = [3, 4, 5, 6, 7, 8]


def clean(v):
    return " ".join(str(v).split()) if v else ""


def find_ms_pdf():
    if not os.path.exists(DATASHEET_FOLDER):
        print(f"[ERROR] Folder not found: {DATASHEET_FOLDER}")
        return None
    files = os.listdir(DATASHEET_FOLDER)
    print(f"[INFO] Files in {DATASHEET_FOLDER}:")
    for f in files: print(f"  • {f}")
    for f in files:
        if f.upper().startswith("MS") and f.lower().endswith(".pdf"):
            path = os.path.join(DATASHEET_FOLDER, f)
            print(f"[FOUND] {path}")
            return path
    print("[ERROR] No MS PDF found.")
    return None


def extract_spec_tables(pdf_path):

    print("\n[INFO] Extracting spec tables...")
    all_specs = {}

    with pdfplumber.open(pdf_path) as pdf:
  
        for page_idx in SPEC_PAGES:
            page  = pdf.pages[page_idx]
            tables = page.extract_tables()
            if not tables:
                continue
            table = tables[0]

            
            header = table[0]
            model_cols = {}
            for ci, cell in enumerate(header):
                v = clean(cell)
                if v and ci > 0:
                    model_cols[ci] = v

            for m in model_cols.values():
                if m not in all_specs:
                    all_specs[m] = {}

            for row in table[1:]:
                if not row or not row[0]:
                    continue
                key = clean(row[0])
                if not key:
                    continue
                for ci, m in model_cols.items():
                    if ci < len(row):
                        val = clean(row[ci])
                        if not val:
                            for back in range(ci - 1, 0, -1):
                                if back < len(row) and clean(row[back]):
                                    val = clean(row[back])
                                    break
                        if val:
                            all_specs[m][key] = val

            print(f"  Page {page_idx+1}: {list(model_cols.values())}")

      
        ms450_page = pdf.pages[8]
        ms450_tables = ms450_page.extract_tables()
        if ms450_tables:
            t = ms450_tables[0]
            ms450_specs = {}
            for row in t:
                if not row or len(row) < 2:
                    continue
                key = clean(row[0])
                val = clean(row[1])
                if key and val:
                    ms450_specs[key] = val
            all_specs["MS450"] = ms450_specs
            print(f"  Page 9: MS450 ({len(ms450_specs)} spec rows)")

    return all_specs


def extract_license_skus(pdf_path):
   
    print("\n[INFO] Extracting license SKUs...")
    lic_data = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx in range(13, 18): 
            page = pdf.pages[page_idx]
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row or len(row) < 2:
                        continue
                    product = clean(row[0])
                    model   = clean(row[1]) if len(row) > 1 else ""
                    license = clean(row[2]) if len(row) > 2 else ""
                    if not product or not model:
                        continue
                    if product not in lic_data:
                        lic_data[product] = {"hardware_models": [], "license_skus": []}
                    if model and model not in lic_data[product]["hardware_models"]:
                        lic_data[product]["hardware_models"].append(model)
                    if license and license not in lic_data[product]["license_skus"]:
                        lic_data[product]["license_skus"].append(license)

    return lic_data


def build_product_url(name):
    slug = name.lower().replace(" ", "-").replace("(","").replace(")","")
    return f"https://meraki.cisco.com/products/switches/{slug}"


def build_entry(name, specs, lic_data):
    perf_keys = ["usage", "routing capabilities", "stacking capabilities",
                 "advanced capabilities", "models"]
    perf, spec_clean = {}, {}
    for k, v in specs.items():
        if any(pk in k.lower() for pk in perf_keys):
            perf[k] = v
        else:
            spec_clean[k] = v


    license_info = {}
    for prod_key, data in lic_data.items():
        # Match e.g. "MS130" in "MS130 compact" or "Catalyst 9200L-M"
        if any(part in name for part in prod_key.split()) or prod_key in name:
            license_info = data
            break

    content = {
        "Overview": FAMILY_OVERVIEW,
        "Features": FAMILY_FEATURES,
        "Specifications": spec_clean,
        "Performance": perf,
        "Usage": FAMILY_USAGE,
    }
    if license_info:
        content["Licensing"] = license_info

    return {
        "family": "MS",
        "name": name,
        "url": build_product_url(name),
        "images": [],
        "content": content,
    }


def save_output(products, report_lines):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    json_path   = os.path.join(OUTPUT_FOLDER, "ms_products.json")
    report_path = os.path.join(OUTPUT_FOLDER, "ms_scrape_report.txt")
    with open(json_path,   "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"\n[SAVED] JSON   → {json_path}")
    print(f"[SAVED] Report → {report_path}")


def main():
    print("=" * 60)
    print("  Cisco MS Family Datasheet Scraper")
    print("=" * 60)

    pdf_path = find_ms_pdf()
    if not pdf_path:
        return

    all_specs = extract_spec_tables(pdf_path)
    lic_data  = extract_license_skus(pdf_path)
    products  = []
    found     = []

    for name, specs in sorted(all_specs.items()):
        print(f"[BUILDING] {name} — {len(specs)} spec rows")
        products.append(build_entry(name, specs, lic_data))
        found.append(name)

    report = [
        "CISCO MS FAMILY SCRAPE REPORT", "=" * 40,
        f"Source: {pdf_path}",
        f"Products extracted: {len(products)}",
        "",
        "Products:"
    ] + [f"  ✓ {p}" for p in found] + [
        "",
        "Notes:",
        "  - 'images' field empty (PDF has no extractable image URLs)",
        "  - Catalyst 9200L-M, 9300-M, 9300L-M, 9300X-M included (in MS datasheet)",
        "  - License info extracted from subscription + co-term tables (pages 14-18)",
        "  - Lifetime warranty applies to all Meraki MS models",
    ]

    save_output(products, report)

    print("\n" + "=" * 60)
    print(f"  DONE {len(products)} MS products extracted.")
    print(f"  Output: {OUTPUT_FOLDER}")
    print("=" * 60)
    for p in found:
        print(f"  • {p}")


if __name__ == "__main__":
    main()
