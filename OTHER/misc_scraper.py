import os
import json
import re
import pdfplumber

DATASHEET_DIR = "DATASHEET"
OUTPUT_DIR    = "OUTPUT"

PDF_FILES = {
    "C8455-G2-MX":    "C8455-G2-MX_Data_Sheet.pdf",
    "Campus-Gateway": "campus-gateway-ds.pdf",
    "MA-INJ-6":       "MA-INJ-6_Meraki_Multigigabit_802_3bt_Power_over_Ethernet_Injector.pdf",
}

def get_all_text(pdf):
    return "\n".join(page.extract_text() or "" for page in pdf.pages)

def tables_to_dict(pdf, skip_labels=None):
    skip_labels = skip_labels or {"item", "specification", "port",
                                  "purpose", "standard", "models",
                                  "description", "cisco e-llw",
                                  "product number"}
    result = {}
    for page in pdf.pages:
        for table in page.extract_tables():
            for row in table:
                if not row or len(row) < 2:
                    continue
                key = (row[0] or "").replace("\n", " ").strip()
                val = (row[1] or "").replace("\n", " ").strip()
                if not key or key.lower() in skip_labels:
                    continue
                lines = [l.strip() for l in (row[1] or "").split("\n") if l.strip()]
                result[key] = lines if len(lines) > 1 else val
    return result

def parse_key_value_text(text, pairs):
    result = {}
    for label, pattern in pairs:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            result[label] = m.group(1).strip()
    return result

def scrape_c8455(pdf_path):
    print("  Parsing C8455-G2-MX...")
    with pdfplumber.open(pdf_path) as pdf:
        text = get_all_text(pdf)

    overview = ""
    if "Overview" in text:
        overview = text.split("Overview")[-1].split("Throughput")[0].strip()

    throughput = parse_key_value_text(text, [
        ("Maximum NGFW Throughput",           r"Maximum NGFW Throughput\s+([\d\w\s]+?Gbps)"),
        ("Maximum Site-to-Site VPN Throughput",r"Maximum Site-to-Site VPN Throughput\s+([\d\w\s]+?Gbps)"),
        ("Advanced Security Throughput",       r"Advanced Security Throughput\s+([\d\w\s]+?Gbps)"),
        ("Recommended Device Count",           r"Recommended Device Count\s+([\d,]+)"),
        ("Maximum Recommended Tunnels",        r"Maximum Recommended Tunnels\s+([\d,]+)"),
    ])

    wan_ports = re.findall(r'([\dx]+\s+SFP28[^\n]+)', text)
    lan_ports = re.findall(r'([\dx]+\s+SFP[+/][^\n]+)', text)

    physical = parse_key_value_text(text, [
        ("Mount Type",           r"Mount Type\s+([^\n]+)"),
        ("Dimensions",           r"Dimensions\s*\(h x w x d\)\s*([^\n]+)"),
        ("Weight",               r"Weight\s+([\d.]+ lbs)"),
        ("Input Operating Voltage", r"Input operating voltage\s+([\d\s]+Vac[\s\d\w]+Hz)"),
        ("Power Supply",         r"Power Supply Unit\s+([^\n]+)"),
        ("Operating Temperature",r"Operating temperature\s+([^\n]+)"),
        ("Humidity",             r"Humidity\s+([^\n]+)"),
    ])

    accessories = re.findall(r'(MA-PWR-CORD-\w+)\s+([^\n]+)', text)
    acc_list = [{"sku": a[0], "description": a[1].strip()} for a in accessories]

    sfp_section = text.split("Compatible Fiber Transceiver")[-1].split("Warranty")[0]
    sfp_modules = list(dict.fromkeys(re.findall(r'((?:SFP|MA-SFP|MA-CBL)[\w\-/]+)', sfp_section)))

    warranty = parse_key_value_text(text, [
        ("Warranty Period", r"C8455-G2-MX\s+(2 Year)"),
    ])

    entry = {
        "family": "MX",
        "name":   "C8455-G2-MX",
        "url":    "https://meraki.cisco.com/products/security-sd-wan/c8455-g2-mx/",
        "images": [],
        "content": {
            "Overview": overview,
            "Features": [
                "Security and SD-WAN firewall for large campus environments",
                "VPN concentration for large VPN networks",
                "Cloud-managed via Meraki dashboard with minimal pre-configuration",
                "2x 25G SFP28 WAN, 2x 10G SFP+ LAN, 8x 1G SFP LAN interfaces",
            ],
            "Specifications": {
                **throughput,
                "Recommended Use Case": "Large Campus & VPN Concentrator",
                "WAN Interfaces":  "2x SFP28 / 25 Gigabit Ethernet",
                "LAN Interfaces":  "2x SFP+ 10G, 8x SFP 1G",
                "Management Port": "1x RJ45 Console, 1x RJ45 Management",
                **physical,
                "Compatible SFP Modules": sfp_modules,
            },
            "Usage":       "Large campus environments and VPN concentration",
            "Performance": {
                "Maximum NGFW Throughput":            throughput.get("Maximum NGFW Throughput", ""),
                "Maximum Site-to-Site VPN Throughput":throughput.get("Maximum Site-to-Site VPN Throughput", ""),
                "Advanced Security Throughput":        throughput.get("Advanced Security Throughput", ""),
                "Recommended Device Count":            throughput.get("Recommended Device Count", ""),
                "Maximum Recommended Tunnels":         throughput.get("Maximum Recommended Tunnels", ""),
            },
            "Accessories": acc_list,
            "Warranty":    warranty.get("Warranty Period", "2 Year"),
        }
    }
    print("   C8455-G2-MX extracted")
    return entry

def scrape_campus_gateway(pdf_path):
    print("  Parsing Campus Gateway...")
    with pdfplumber.open(pdf_path) as pdf:
        text = get_all_text(pdf)

        overview = ""
        if "Overview" in text:
            raw = text.split("Overview")[-1]
            overview = raw.split("Platform highlights")[0].strip()

        features = {}
        how_it_works = {}
        if len(pdf.pages) > 2:
            for table in pdf.pages[2].extract_tables():
                for row in table:
                    if row and row[0] and row[1]:
                        k = row[0].replace("\n", " ").strip()
                        v = row[1].replace("\n", " ").strip()
                        if any(x in k for x in ["cloud","scale","infra","segment","onboard"]):
                            features[k] = v
                        else:
                            how_it_works[k] = v

        specs = {}
        if len(pdf.pages) > 4:
            for table in pdf.pages[4].extract_tables():
                for row in table:
                    if row and row[0] and row[1]:
                        k = row[0].replace("\n", " ").strip()
                        v = row[1].replace("\n", " ").strip()
                        if k.lower() not in {"item", "specification"}:
                            specs[k] = v

        ports = {}
        if len(pdf.pages) > 3:
            for table in pdf.pages[3].extract_tables():
                for row in table:
                    if row and len(row) >= 3 and row[1] and row[2]:
                        port_label = row[1].replace("\n", " ").strip()
                        purpose    = row[2].replace("\n", " ").strip()
                        if port_label and purpose and port_label not in {"Port", "Purpose"}:
                            ports[port_label] = purpose

        supported_aps = {}
        if len(pdf.pages) > 7:
            for table in pdf.pages[7].extract_tables():
                for row in table:
                    if row and row[0] and row[1]:
                        k = row[0].strip()
                        v = row[1].strip()
                        if k.lower() not in {"standard", "models"}:
                            supported_aps[k] = [m.strip() for m in v.split(",")]

        warranty = {}
        if len(pdf.pages) > 8:
            for table in pdf.pages[8].extract_tables():
                for row in table:
                    if row and row[0] and row[1]:
                        k = row[0].replace("\n"," ").strip()
                        v = row[1].replace("\n"," ").strip()
                        if k.lower() not in {"description","cisco e-llw"}:
                            warranty[k] = v

    entry = {
        "family": "Campus Gateway",
        "name":   "Campus-Gateway",
        "url":    "https://meraki.cisco.com/products/campus-gateway/",
        "images": [],
        "content": {
            "Overview":  overview,
            "Features":  features,
            "How It Works": how_it_works,
            "Specifications": {
                "SKU":           specs.get("SKU", "CW9800H1-MCG"),
                "Throughput":    specs.get("Throughput", "Up to 100 Gbps (200 Gbps clustered)"),
                "Scale":         specs.get("Scale", "5,000 APs and 50,000 clients"),
                "Data Ports":    specs.get("Data ports", "4x 25 Gbps SFP28, 8x 1/10 Gbps SFP+"),
                "Power":         specs.get("Power", "Dual 750W AC"),
                "Redundancy Ports": specs.get("Redundancy ports", ""),
                "Service Ports": specs.get("Service ports", "1x RJ-45"),
                "Min. Release":  specs.get("Minimum supported release", "MR31.2"),
                "Ports":         ports,
                "Form Factor":   "1RU rack-mount",
                "Management":    "Cloud-managed via Meraki dashboard",
            },
            "Usage":         "Large campus wireless networks requiring seamless roaming at scale",
            "Supported APs": supported_aps,
            "Performance": {
                "Throughput": specs.get("Throughput", "Up to 100 Gbps"),
                "Scale":      specs.get("Scale", "5,000 APs, 50,000 clients"),
            },
            "Licensing": {
                "Device License": "Not required for Campus Gateway itself",
                "AP License":     "Enterprise or Advanced tier cloud license required per AP",
                "Wi-Fi 7 APs":   "Cisco Networking Subscription (Essentials or Advantage tier)",
            },
            "Warranty": warranty,
        }
    }
    print("   Campus-Gateway extracted")
    return entry

def scrape_ma_inj6(pdf_path):
    print("  Parsing MA-INJ-6...")
    with pdfplumber.open(pdf_path) as pdf:
        text = get_all_text(pdf)

    overview = ""
    if "MA-INJ-6 Reliable" in text:
        overview = text.split("MA-INJ-6 Reliable")[-1].split("Product Highlights")[0].strip()
        overview = "MA-INJ-6 Reliable " + overview

    features = []
    if "Product Highlights" in text:
        hl_section = text.split("Product Highlights")[-1].split("Power")[0]
        for line in hl_section.split("\n"):
            line = line.strip().lstrip("•").strip()
            if line and len(line) > 10:
                features.append(line)

    power = parse_key_value_text(text, [
        ("Input Voltage",          r"Input voltage:\s*([^\n]+)"),
        ("Maximal Input Current",  r"Maximal input current:\s*([^\n]+)"),
        ("AC Input Frequency",     r"AC input frequency:\s*([^\n]+)"),
        ("Output Voltage",         r"Output voltage:\s*([^\n]+)"),
        ("Maximum Output Power",   r"Maximum output power:\s*([^\n]+)"),
        ("Max Device Distance",    r"Powered device can be up to ([^\*\n]+)"),
    ])

    env = parse_key_value_text(text, [
        ("Ethernet Compatibility",   r"Compatible with Ethernet ([^\n]+)"),
        ("Operating Temperature",    r"Operating temperature:\s*([^\n]+)"),
        ("Storage Temperature",      r"Storage temperature:\s*([^\n]+)"),
        ("Operating Humidity",       r"Operating humidity:\s*([^\n]+)"),
    ])

    physical = parse_key_value_text(text, [
        ("Dimensions", r"Physical dimensions\s*([\d.]+\s*mm[^\n]+)"),
        ("Weight",     r"Weight:\s*([^\n]+)"),
        ("Mounting",   r"Mounting\s*([^\n]+)"),
    ])

    regulatory = []
    if "Regulatory" in text:
        reg_section = text.split("Regulatory")[-1].split("Warranty")[0]
        for line in reg_section.split("\n"):
            line = line.strip()
            if line and len(line) > 2:
                regulatory.append(line)

    leds = []
    if "LED indicators" in text:
        led_section = text.split("LED indicators")[-1].split("Regulatory")[0]
        for line in led_section.split("\n"):
            line = line.strip()
            if line and len(line) > 5:
                leds.append(line)

    cord_skus = re.findall(r'(MA-PWR-CORD-\w+)\s*\(([^)]+)\)', text)
    power_cords = [{"sku": s, "region": r} for s, r in cord_skus]

    entry = {
        "family": "Accessories",
        "name":   "MA-INJ-6",
        "url":    "https://meraki.cisco.com/products/accessories/ma-inj-6/",
        "images": [],
        "content": {
            "Overview":  overview,
            "Features":  features,
            "Specifications": {
                **power,
                **env,
                **physical,
                "Standards Compliance": "IEEE 802.3bt (backward compatible with 802.3af and 802.3at)",
                "Regulatory":           regulatory,
                "LED Indicators":       leds,
                "Warranty":             "1 Year Hardware",
            },
            "Usage": (
                "Powers Wi-Fi 6, 6E and Wi-Fi 7 Meraki access points via "
                "single Ethernet cable; backward compatible with 802.3af/at devices"
            ),
            "Performance": {
                "Maximum Output Power":  power.get("Maximum Output Power", "60W"),
                "Output Voltage":        power.get("Output Voltage", "55 VDC"),
                "Ethernet Compatibility":env.get("Ethernet Compatibility", "10 Gbps Multigigabit"),
                "Max Device Distance":   power.get("Max Device Distance", "100m"),
            },
            "Ordering": {
                "SKU":        "MA-INJ-6",
                "Power Cords": power_cords,
                "Note":       "Power cords ordered separately",
            },
        }
    }
    print("   MA-INJ-6 extracted")
    return entry

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

    combined_path = os.path.join(output_dir, "Misc_products_all.json")
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    return saved, combined_path

def main():
    print("=" * 55)
    print("Cisco Misc Products Scraper")
    print("C8455-G2-MX | Campus Gateway | MA-INJ-6")
    print("=" * 55)

    entries = []
    missing = []

    scrapers = {
        "C8455-G2-MX":    scrape_c8455,
        "Campus-Gateway": scrape_campus_gateway,
        "MA-INJ-6":       scrape_ma_inj6,
    }

    print("\nExtracting products...")
    for name, filename in PDF_FILES.items():
        path = os.path.join(DATASHEET_DIR, filename)
        if not os.path.exists(path):
            print(f"Missing: {path}")
            missing.append(name)
            continue
        entry = scrapers[name](path)
        entries.append(entry)

    if not entries:
        print("\nNo products extracted.")
        return

    print(f"\nSaving {len(entries)} products to {OUTPUT_DIR}/...")
    saved, combined_path = save_products(entries, OUTPUT_DIR)

    print("\n" + "=" * 55)
    print("ALL DONE!")
    print("=" * 55)
    print(f"Products saved : {len(saved)}")
    print(f"Combined file  : {combined_path}")
    if missing:
        print(f"Missing PDFs   : {', '.join(missing)}")
    print(f"\nProducts extracted:")
    for name in saved:
        print(f"{name}")
    print("=" * 55)

if __name__ == "__main__":
    main()