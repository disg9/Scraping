import os, json

OUTPUT_FOLDER = os.path.join("COSOL", "OUTPUT")

PRODUCTS = [

    {
        "family": "GX",
        "name": "GX20",
        "url": "https://meraki.cisco.com/products/meraki-go/gx20",
        "images": [],
        "content": {
            "Overview": (
                "The Meraki Go GX20 is a Security Gateway designed for small businesses. "
                "It provides stateful firewall, DHCP, and DNS-based security powered by "
                "Cisco Umbrella, all managed through the simple Meraki Go mobile app and "
                "web portal. Recommended for deployments with 50 clients or fewer."
            ),
            "Features": [
                "Stateful firewall",
                "Port Forwarding",
                "DHCP services",
                "DNS-based security powered by Cisco Umbrella (additional subscription required)",
                "1x 802.3af PoE enabled LAN port (15.5W)",
                "Kensington lock hard point",
                "Remote cloud management via mobile app and web portal",
                "Automatic firmware updates",
            ],
            "Specifications": {
                "WAN Interface": "1x 10/100/1000 BASE-T Ethernet (RJ45)",
                "LAN Interfaces": "4x 10/100/1000 BASE-T Ethernet (RJ45)",
                "PoE": "1x 802.3af enabled port (15.5W)",
                "Operating Temperature": "32°F to 104°F (0°C to 40°C)",
                "Humidity": "5 to 95% non-condensing",
                "Power Supply": "50W (54V / 0.92A) included",
                "Dimensions": "6.83 x 4.41 x 1.04 in (173.4 x 112 x 26.3 mm), excluding feet/mount",
                "Mounting": "Desktop",
                "Warranty": "1 year (US/Japan), 2 year (UK/EU)",
                "Compliance": "Kensington lock hard point",
            },
            "Performance": {
                "Firewall Throughput": "250 Mbps",
                "Recommended Clients": "50 or fewer",
            },
            "Usage": (
                "Designed for small businesses needing basic security gateway functionality. "
                "Ideal for offices with up to 50 clients requiring stateful firewall, DHCP, "
                "and optional DNS-layer threat protection via Cisco Umbrella."
            ),
            "LED Indicators": [
                "2x Ethernet status LEDs",
                "1x Power/booting/firmware upgrade status LED",
            ],
            "In_the_Box": [
                "GX20-HW: Meraki Go Security Gateway",
                "Wall mount and screw kit",
                "Quick start guide",
                "PSU and ethernet cable",
            ],
            "Hardware_SKUs": {
                "GX20-HW-XX": "Security Gateway - Desktop (XX = US/UK/EU)",
            },
            "Accessories": {
                "GA-PWR-50WAC": "50W Replacement Laptop Style Adapter for GX20",
            },
        }
    },

    {
        "family": "GX",
        "name": "GX50",
        "url": "https://meraki.cisco.com/products/meraki-go/gx50",
        "images": [],
        "content": {
            "Overview": (
                "The Meraki Go GX50 is a Router Firewall Plus designed for small businesses "
                "needing more advanced connectivity. It adds Client VPN and Site-to-Site VPN "
                "(GX50 to GX50) on top of the GX20's security gateway features, with 500+ Mbps "
                "firewall throughput. Managed entirely through the Meraki Go mobile app."
            ),
            "Features": [
                "Stateful firewall",
                "Port Forwarding",
                "DHCP services",
                "DNS-based security powered by Cisco Umbrella (additional subscription required)",
                "Client VPN",
                "Site-to-Site VPN (GX50 to GX50 only)",
                "Kensington lock hard point",
                "Remote cloud management via mobile app and web portal",
                "Automatic firmware updates",
            ],
            "Specifications": {
                "WAN Interface": "1x 10/100/1000 BASE-T Ethernet (RJ45)",
                "LAN Interfaces": "4x 10/100/1000 BASE-T Ethernet (RJ45)",
                "Operating Temperature": "32°F to 113°F (0°C to 45°C)",
                "Humidity": "5 to 95% non-condensing",
                "Power Supply": "18W DC included",
                "Power Load (idle)": "5W",
                "Power Load (max)": "14W",
                "Dimensions": "1.1 x 5.1 x 9.4 in (27 x 130 x 239 mm), excluding feet/mount",
                "Weight": "1.74 lb / 0.79 kg",
                "Warranty": "1 year (US/Japan), 2 year (UK/EU)",
            },
            "Performance": {
                "Firewall Throughput": "500+ Mbps",
                "Client VPN Throughput": "300 Mbps",
                "VPN Tunnels": "50",
                "Recommended Clients": "50",
            },
            "Usage": (
                "Ideal for small businesses needing VPN capabilities in addition to firewall. "
                "Supports client VPN for remote workers and site-to-site VPN between GX50 units "
                "for connecting multiple branch offices."
            ),
            "LED Indicators": [
                "2x Ethernet status LEDs",
                "1x Power/booting/firmware upgrade status LED",
            ],
            "In_the_Box": [
                "GX50-HW: Meraki Go Security Gateway",
                "Wall mount and screw kit",
                "Quick start guide",
                "PSU and ethernet cable",
            ],
            "Hardware_SKUs": {
                "GX50-HW-XX": "Security Gateway - Desktop (XX = US/UK/EU)",
            },
            "Accessories": {
                "GA-PWR-50WAC": "50W Replacement Laptop Style Adapter for GX50",
            },
        }
    },

    {
        "family": "GR",
        "name": "GR10",
        "url": "https://meraki.cisco.com/products/meraki-go/gr10",
        "images": [],
        "content": {
            "Overview": (
                "The Cisco Meraki Go GR10 is a dual-radio, cloud-managed 2x2:2 802.11ac Wave 2 "
                "indoor access point with MU-MIMO support."
            ),
            "Features": [
                "Dual-band 802.11ac Wave 2 with 2x2:2 MU-MIMO",
                "1.04 Gbps maximum aggregate frame rate",
            ],
            "Specifications": {
                "Radio 1": "2.4 GHz 802.11b/g/n",
                "Radio 2": "5 GHz 802.11a/n/ac",
            },
            "Performance": {
                "Aggregate Frame Rate": "1.04 Gbps (maximum)",
            },
            "Usage": "Indoor small business Wi-Fi deployments",
        }
    },

    {
        "family": "GR",
        "name": "GR60",
        "url": "https://meraki.cisco.com/products/meraki-go/gr60",
        "images": [],
        "content": {
            "Overview": "Outdoor version of GR10 with extended temperature support.",
            "Features": [
                "Outdoor-rated hardware",
                "Dual-band 802.11ac Wave 2",
            ],
            "Specifications": {
                "Operating Temperature": "-20°C to 55°C",
            },
            "Performance": {
                "Aggregate Frame Rate": "1.04 Gbps",
            },
            "Usage": "Outdoor Wi-Fi deployments",
        }
    },

    {
        "family": "GS",
        "name": "GS110",
        "url": "https://meraki.cisco.com/products/meraki-go/gs110",
        "images": [],
        "content": {
            "Overview": "Cloud-managed switches for small businesses.",
            "Features": [
                "No licensing required",
                "Remote cloud management",
            ],
            "Specifications": {
                "Port Options": "8/24/48",
            },
            "Performance": {
                "Switching Capacity": "Up to 104 Gbps",
            },
            "Usage": "Small business networking",
        }
    },
]


def save_output(products):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    json_path   = os.path.join(OUTPUT_FOLDER, "meraki_go_products.json")
    report_path = os.path.join(OUTPUT_FOLDER, "meraki_go_report.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    report_lines = [
        "CISCO MERAKI GO SCRAPE REPORT",
        "=" * 40,
        f"Total products: {len(products)}",
        "",
        "Products extracted:",
    ] + [f"{p['name']:10s} | family: {p['family']} | specs: {len(p['content']['Specifications'])}" for p in products]

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"[SAVED] JSON   → {json_path}")
    print(f"[SAVED] Report → {report_path}")


def main():
    print("=" * 60)
    print("Cisco Meraki Go Family Scraper")
    print("=" * 60)
    for p in PRODUCTS:
        specs = len(p["content"]["Specifications"])
        feats = len(p["content"].get("Features", []))
        print(f"{p['name']:8s} | {specs} specs | {feats} features")
    save_output(PRODUCTS)
    print("\n" + "=" * 60)
    print(f"DONE! {len(PRODUCTS)} products saved.")
    print(f"Output: {OUTPUT_FOLDER}")
    print("=" * 60)


if __name__ == "__main__":
    main()