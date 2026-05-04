

import os
import re
import json
import pdfplumber



DATASHEET_FOLDER = os.path.join("COSOL", "DATASHEET")
OUTPUT_FOLDER    = os.path.join("COSOL", "OUTPUT")


FAMILY_OVERVIEW = (
    "The Cisco Meraki MX is a multifunctional security and SD-WAN enterprise appliance. "
    "It is 100% cloud managed via the Meraki Dashboard — zero-touch installation, "
    "ideal for distributed branches, campuses, and data centers. Natively integrates "
    "firewalling, SD-WAN, AMP, IDS/IPS, content filtering, Auto VPN, and more."
)

FAMILY_FEATURES = [
    # QoE Analytics
    "Monitor end-to-end health of web applications across LAN, WAN, and application server",
    "Machine-learned smart application thresholds to identify anomalies",
    "Monitor health of all MX WAN links including cellular across entire organization",
    # Security
    "Next-gen layer 7 firewall for identity-based security policies and application management",
    "Advanced Malware Protection (AMP) with sandboxing powered by Cisco AMP",
    "Intrusion prevention: PCI-compliant IPS sensor using SNORT® signature database from Cisco Talos",
    "Granular and automatically updated category-based content filtering",
    "SSL decryption/inspection, DLP, CASB, SaaS tenant restrictions, granular app control",
    "Unified SASE and SSE through Cisco Secure Access / Cisco Secure Connect",
    "Native integration with Cisco XDR for AI-driven analytics and fast incident response",
    # Branch gateway
    "Built-in DHCP, NAT, QoS, and VLAN management services",
    "Load balancing across multiple WAN links with QoS and failover policies",
    "Smart connection monitoring with automatic layer 2/3 outage detection",
    "Support for 5G cellular connection with MG52 as cellular gateway",
    # Cloud management
    "100% cloud managed via intuitive Cisco Meraki Dashboard",
    "Zero-touch remote deployment — no on-site staging needed",
    "Template-based settings that scale from small to tens of thousands of devices",
    "Role-based administration with email alerts and auditable change logs",
    # VPN / SD-WAN
    "Auto VPN: automatic IKE/IKEv2/IPsec site-to-site VPN setup",
    "SD-WAN with active/active VPN, policy-based routing, and dynamic path selection",
    "Automated MPLS to VPN failover within seconds",
    "Support for Cisco AnyConnect remote client VPN (license required)",
    "Mix-and-match Meraki and Cisco Catalyst SD-WAN from a single dashboard",
]

FAMILY_USAGE = (
    "Designed for organizations of all sizes across all industries. "
    "Ideal for distributed branches, small offices, campuses, data centers, "
    "and cloud-connected environments. Scales from 50-user small branches (MX67/MX68) "
    "to 10,000-user campus/VPN concentrators (MX450/C8455-G2-MX)."
)

COMMON_SPECS = {
    "Management": "100% cloud managed via Cisco Meraki Dashboard",
    "Deployment": "Zero-touch, no staging required",
    "Firewall": "Next-gen layer 7 (NGFW) with application-based policies",
    "VPN": "Auto VPN (IKEv2/IPsec), Client VPN (IPsec L2TP), Cisco AnyConnect",
    "SD-WAN": "Active/active VPN, policy-based routing, dynamic path selection",
    "Security": "AMP, IDS/IPS (SNORT), content filtering, SSL inspection, CASB, DLP",
    "Warranty": "Limited lifetime hardware warranty with next-day advanced replacement",
    "Regulatory": "FCC (US), CB (IEC), CISPR, RCM",
    "Cloud Platforms (vMX)": "AWS, Microsoft Azure, Google Cloud, Alibaba Cloud",
}



def find_mx_pdf():
    
    if not os.path.exists(DATASHEET_FOLDER):
        print(f"\n[ERROR] Folder not found: '{DATASHEET_FOLDER}'")
        print("  Make sure you are running this script from the folder that CONTAINS COSOL.")
        print("  Example: if COSOL is on your Desktop, open your terminal, type:")
        print("    cd Desktop")
        print("    python scrape_mx_family.py")
        return None

    files = os.listdir(DATASHEET_FOLDER)
    print(f"\n[INFO] Files in {DATASHEET_FOLDER}:")
    for f in files:
        print(f"  • {f}")

    for f in files:
        if f.upper().startswith("MX") and f.lower().endswith(".pdf"):
            path = os.path.join(DATASHEET_FOLDER, f)
            print(f"\n[FOUND] Using: {path}")
            return path

    print("\n[ERROR] No MX PDF found. Make sure the filename starts with 'MX'.")
    return None





def clean(text):

    if text is None:
        return ""
    return " ".join(str(text).split())

def extract_spec_tables(pdf_path):
   
    print("\n[INFO] Extracting specification tables...")

    spec_pages = [12, 13, 14, 15, 16]  

    all_specs = {}  

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx in spec_pages:
            page = pdf.pages[page_idx]
            tables = page.extract_tables()

            if not tables:
                continue

            table = tables[0] 

        
            header_row = table[0]

           
            model_columns = {} 
            for col_idx, cell in enumerate(header_row):
                val = clean(cell)
                if val and col_idx > 0:
                    model_columns[col_idx] = val

            
            for model_name in model_columns.values():
                if model_name not in all_specs:
                    all_specs[model_name] = {}

            
            for row in table[1:]:
                if not row or not row[0]:
                    continue

                spec_key = clean(row[0])
                if not spec_key:
                    continue

                
                for col_idx, model_name in model_columns.items():
                    if col_idx < len(row):
                        val = clean(row[col_idx])
                        
                        
                        if not val:
                            
                            for back in range(col_idx - 1, 0, -1):
                                if back < len(row) and clean(row[back]):
                                    val = clean(row[back])
                                    break
                        if val:
                            all_specs[model_name][spec_key] = val

            print(f"  Page {page_idx+1}: found models {list(model_columns.values())}")

   
    VMX_MODELS = ["vMX – Small", "vMX – Medium", "vMX – Large"]
    with pdfplumber.open(pdf_path) as pdf:
        vmx_table = pdf.pages[17].extract_tables()
        if vmx_table:
            t = vmx_table[0]
            for m in VMX_MODELS:
                all_specs[m] = {}
            for row in t:
                if not row or not row[0]:
                    continue
                key = clean(row[0])
                if not key:
                    continue
                
                for ci, m in enumerate(VMX_MODELS, start=1):
                    if ci < len(row):
                        val = clean(row[ci])
                        if val:
                            all_specs[m][key] = val
            print(f"  Page 18: found vMX models {VMX_MODELS}")

    return all_specs




def extract_license_skus(pdf_path):
   
    print("\n[INFO] Extracting license SKU tables...")
    sku_pages = list(range(24, 31))  
    sku_data = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx in sku_pages:
            page = pdf.pages[page_idx]
            tables = page.extract_tables()
            if not tables:
                continue
            for table in tables:
                for row in table:
                    if not row or len(row) < 2:
                        continue
                    hw_sku = clean(row[0])
                    licenses_raw = clean(row[1]) if len(row) > 1 else ""
                    
                    if not hw_sku or not licenses_raw:
                        continue
                    
                    match = re.match(r'^([A-Z0-9]+-?[A-Z0-9]*?)(?:-HW|-NA|-WW)?$', hw_sku)
                    if match:
                        product_key = match.group(1)
                        license_list = [l.strip() for l in licenses_raw.split("\n") if l.strip()]
                        if product_key not in sku_data:
                            sku_data[product_key] = {
                                "hardware_sku": hw_sku,
                                "license_skus": license_list
                            }
                        else:
                            sku_data[product_key]["license_skus"].extend(license_list)

    return sku_data

 

def extract_general_specs(pdf_path):
    """
    Pages 23-24 have family-wide capability lists organised into
    categories. We extract them as lists per category.
    """
    print("\n[INFO] Extracting general MX specifications (pages 23-24)...")
    general = {}

    category_map = {
        
        "Management": [],
        "Monitoring and reporting": [],
        "Network and firewall services": [],
        "WAN performance management": [],
     
        "Advanced security services": [],
        "Integrated wireless (MX67W, MX68W, MX68CW)": [],
        "Integrated cellular (MX67C and MX68CW only)": [],
        "Power over Ethernet (MX68, MX68W, MX68CW)": [],
        "Regulatory": [],
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx in [22, 23]:  
            page = pdf.pages[page_idx]
            tables = page.extract_tables()
            text = page.extract_text() or ""

            
            lines = [l.strip() for l in text.split("\n") if l.strip()]

            current_category = None
            for line in lines:
                
                matched = False
                for cat_key in category_map:
                    
                    if cat_key.lower() in line.lower() or line.lower() in cat_key.lower():
                        current_category = cat_key
                        matched = True
                        break
                if not matched and current_category:
                    
                    if re.match(r'MX FAMILY DATASHEET', line):
                        continue
                    if line and len(line) > 5:
                        category_map[current_category].append(line)

 
    for k, v in category_map.items():
        if v:
            general[k] = v

    return general


 

def build_product_url(product_name):
    slug = product_name.lower().replace(" ", "-")
    return f"https://meraki.cisco.com/products/appliances/{slug}"

def build_product_entry(product_name, specs, sku_data, general_specs):
   
    perf_keys = [
        "NGFW throughput", "Advanced security services throughput",
        "Advanced security services throughput1",
        "Maximum site-to-site VPN throughput",
        "Maximum site-to-site VPN tunnels", "Maximum site-to- site VPN tunnels2",
        "Recommended use case", "Recommended use cases"
    ]

    performance = {}
    specifications = {}

    for key, val in specs.items():
        clean_key = key.replace("\n", " ").strip()
        
        is_perf = any(pk.lower() in clean_key.lower() for pk in perf_keys)
        if is_perf:
            performance[clean_key] = val
        else:
            specifications[clean_key] = val

    
    sku_key = product_name  
    license_info = {}
    if sku_key in sku_data:
        license_info = sku_data[sku_key]
    else:
        
        for k, v in sku_data.items():
            if product_name in k or k in product_name:
                license_info = v
                break

    content = {
        "Overview": FAMILY_OVERVIEW,
        "Features": FAMILY_FEATURES,
        "Specifications": specifications,
        "Performance": performance,
        "Usage": FAMILY_USAGE,
        "General_Capabilities": general_specs,
    }

    if license_info:
        content["Licensing"] = license_info

    return {
        "family": "MX",
        "name": product_name,
        "url": build_product_url(product_name),
        "images": [], 
        "content": content
    }


 

def save_output(products, report_lines):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    json_path   = os.path.join(OUTPUT_FOLDER, "mx_products.json")
    report_path = os.path.join(OUTPUT_FOLDER, "mx_scrape_report.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"\n[SAVED] JSON  → {json_path}")
    print(f"[SAVED] Report → {report_path}")


 

def main():
    print("=" * 60)
    print("  Cisco MX Family Datasheet Scraper — Final Version")
    print("=" * 60)

    
    pdf_path = find_mx_pdf()
    if not pdf_path:
        return

    
    all_specs = extract_spec_tables(pdf_path)

    
    sku_data = extract_license_skus(pdf_path)

    
    general_specs = extract_general_specs(pdf_path)

   
    products = []
    found = []
    for product_name, specs in sorted(all_specs.items()):
        print(f"\n[BUILDING] {product_name} — {len(specs)} spec rows found")
        entry = build_product_entry(product_name, specs, sku_data, general_specs)
        products.append(entry)
        found.append(product_name)

   
    report_lines = [
        "CISCO MX FAMILY SCRAPE REPORT",
        "=" * 40,
        f"Source PDF: {pdf_path}",
        f"Total products extracted: {len(products)}",
        "",
        "Products found in spec tables:",
    ]
    for p in found:
        spec_count = len(products[found.index(p)]["content"]["Specifications"])
        perf_count = len(products[found.index(p)]["content"]["Performance"])
        report_lines.append(f"  ✓ {p:20s} | Specs: {spec_count:2d}  | Performance rows: {perf_count}")

    report_lines += [
        "",
        "Notes:",
        "  - 'images' field is empty: PDF has embedded raster images, not URLs",
        "  - 'url' field is a best-guess Meraki product page URL (verify manually)",
        "  - General capabilities (pages 23-24) stored under 'General_Capabilities'",
        "  - License SKUs extracted from pages 25-31",
        "  - Family-level features apply to ALL products and are stored in each entry",
    ]

    
    save_output(products, report_lines)

    # Final summary
    print("\n" + "=" * 60)
    print(f"  Extracted {len(products)} MX products.")
    print(f"  Output folder: {OUTPUT_FOLDER}")
    print("=" * 60)
    print("\nProducts extracted:")
    for p in found:
        print(f"  • {p}")


if __name__ == "__main__":
    main()
