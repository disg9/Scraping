

import os, json

OUTPUT_FOLDER = os.path.join("COSOL", "OUTPUT")

PRODUCTS = [

    # Z4C 
    {
        "family": "Z",
        "name": "Z4C",
        "url": "https://meraki.cisco.com/products/teleworker/z4c",
        "images": [],
        "content": {
            "Overview": (
                "The Cisco Meraki Z4C is an enterprise-class teleworker gateway combining a "
                "firewall, VPN gateway, router, WiFi 6 access point, and built-in LTE modem in "
                "one device. It offers five gigabit ethernet ports including a PoE-enabled port "
                "for VoIP phones, and is designed to securely extend Meraki cloud-managed "
                "networking to remote workers and small locations. Recommended for up to 15 devices."
            ),
            "Features": [
                # Software
                "Managed via Cisco Meraki Dashboard",
                "Automatic firmware upgrades",
                "L3/L7 Stateful Firewall",
                "1:1 and 1:Many NAT",
                "Configurable VLANs and DHCP support",
                "Static Routing",
                "Client VPN endpoint",
                "Meraki AutoVPN and IPSec VPN endpoint",
                "Custom Traffic Shaping",
                "Historical Client Usage statistics",
                "Netflow support",
                "Syslog integration",
                "Remote Packet Capture tools",
                "IPv6 Support",
                "802.1X wired and wireless support",
                # Hardware
                "Built-in WiFi 6 (802.11ax) dual-band 2x2 MU-MIMO wireless",
                "Built-in PoE+ on 1x GbE LAN port (802.3at)",
                "Built-in CAT12 LTE modem with 2x external LTE antennas for cellular backup",
                "Desktop or wall mount form factor",
            ],
            "Specifications": {
                "WAN Interface": "1x dedicated GbE RJ45",
                "Cellular Uplink": "1x built-in CAT12 LTE modem",
                "LAN Interfaces": "4x dedicated GbE RJ45",
                "PoE": "1x GbE RJ45 LAN port (802.3at)",
                "WiFi Standard": "802.11a/b/g/n/ac/ax (2.4 GHz or 5 GHz)",
                "WiFi MIMO": "2x2 MU-MIMO with two spatial streams",
                "Max WiFi Data Rate": "1.5 Gbps (maximum chipset rate)",
                "Cellular Antennas": "2x external LTE antennas",
                "Mount Type": "Desktop / Wall Mount",
                "Dimensions (h x d x w)": "7.9 x 4.41 x 1.04 in / 200 x 112 x 26 mm",
                "Weight": "1.1 lbs / 0.487 kg",
                "Power Supply": "50W DC",
                "Power Load (idle/max)": "15W / 46W",
                "Operating Temperature": "32°F to 113°F (0°C to 45°C)",
                "Storage Temperature": "-4°F to 158°F (-20°C to 70°C)",
                "Humidity": "5% to 95%",
                "Compliance": "FCC Class B",
                "Warranty": "Lifetime (device), 1 year (accessories)",
            },
            "Performance": {
                "Recommended Use Case": "Up to 15 devices",
                "Stateful Firewall Throughput": "500 Mbps (NAT mode)",
                "Max VPN Throughput": "250 Mbps",
                "Security Throughput": "300 Mbps",
                "Single Wired WAN Uplink": "Yes",
                "Cellular Uplink": "Yes",
            },
            "Usage": (
                "Designed for teleworkers, home offices, and small remote locations needing "
                "enterprise-grade security with simple cloud management. The built-in LTE modem "
                "provides cellular failover or primary connectivity for locations without "
                "reliable wired internet. Ideal for VPN back to corporate headquarters."
            ),
            "Hardware_SKUs": {
                "Z4C-HW": "Meraki Z4C Cloud Managed Teleworker Gateway",
            },
            "Accessories": {
                "MA-PWR-50WAC":    "Meraki MX Replacement Power Adapter (Z4/C) 50W AC",
                "MA-PWR-CORD-US":  "1x AC Power Cable, US plug",
                "MA-PWR-CORD-EU":  "1x AC Power Cable, EU plug",
                "MA-PWR-CORD-UK":  "1x AC Power Cable, UK plug",
                "MA-PWR-CORD-AU":  "1x AC Power Cable, AU plug",
            },
        }
    },

    # vMX 
    {
        "family": "MX",
        "name": "vMX",
        "url": "https://meraki.cisco.com/products/appliances/vmx",
        "images": [],
        "content": {
            "Overview": (
                "The Cisco Meraki vMX is a virtual instance of a Meraki security and SD-WAN "
                "appliance, available in three sizes (Small, Medium, Large). It extends secure "
                "SD-WAN and Auto VPN connectivity from branch sites to public and private cloud "
                "environments. Supported cloud platforms: AWS, Microsoft Azure, Alibaba Cloud, "
                "and Google Cloud. All instances require a Meraki license."
            ),
            "Features": [
                "Auto-VPN (SD-WAN termination from branch)",
                "IPsec VPN",
                "AnyConnect / L2TP VPN",
                "VPN firewall",
                "BGP and OSPF routing",
                "One-Armed concentrator mode",
                "NAT mode",
                "One WAN and One LAN port (MX firmware 18.2+)",
                "L3/L7 Firewall (MX firmware 19.1+)",
                "Content Filtering (MX firmware 19.1+)",
                "Intrusion Detection/Prevention (MX firmware 19.1+)",
                "Security Center (MX firmware 19.1+)",
                "Static IP support via Meraki Dashboard",
                "Stop/restart instance supported (pause/hibernate not recommended)",
                "Reconfigurable after deployment (vMX must be powered down first)",
            ],
            "Specifications": {
                "Deployment Type": "Virtual appliance (no physical hardware)",
                "Supported Cloud Platforms": "AWS, Microsoft Azure, Alibaba Cloud, Google Cloud",
                "Interfaces": "Virtual (no physical ports)",
                "Minimum Firmware (AWS/Alibaba)": "MX15.37+",
                "Minimum Firmware (Azure vMX-S/M)": "MX15.37+",
                "Minimum Firmware (Azure vMX-L)": "MX18.2+",
                "Licenses": "1, 3, 5-year Enterprise and Advanced Security",
                "BGP Support": "MX15.37+",
                "Concentrator Mode (vMX-S)": "MX18.2+",
                "Concentrator Mode (vMX-M/L)": "MX15.37+",
            },
            "Performance": {
                "vMX-S VPN Throughput":    "250 Mbps",
                "vMX-S NAT Throughput":    "250 Mbps",
                "vMX-S NGFW Throughput":   "200 Mbps",
                "vMX-S Max VPN Tunnels":   "50",
                "vMX-M VPN Throughput":    "500 Mbps",
                "vMX-M NAT Throughput":    "500 Mbps",
                "vMX-M NGFW Throughput":   "400 Mbps",
                "vMX-M Max VPN Tunnels":   "250",
                "vMX-L VPN Throughput":    "1 Gbps",
                "vMX-L NAT Throughput":    "1 Gbps",
                "vMX-L NGFW Throughput":   "1 Gbps",
                "vMX-L Max VPN Tunnels":   "1,000",
            },
            "Cloud_Instance_Sizes": {
                "vMX-S (AWS)":     "M4.large, C5.large",
                "vMX-S (Azure)":   "Standard_F4s_V2, Standard_D2_v2, Standard_D2_v3",
                "vMX-S (Alibaba)": "C5.large, C6.large",
                "vMX-M (AWS)":     "M4.large, C5.large",
                "vMX-M (Azure)":   "Standard_F4s_V2, Standard_D2_v2, Standard_D2_v3",
                "vMX-M (Alibaba)": "C5.large, C6.large",
                "vMX-L (AWS)":     "C5.xlarge",
                "vMX-L (Azure)":   "Standard_F4s_v2",
                "vMX-L (Alibaba)": "C5.xlarge, C6.xlarge",
            },
            "Unsupported_Features": [
                "High Availability (HA) — recommended alternative is DC-DC failover",
                "Umbrella DNS Security (MR/Z1/Z3 only)",
                "Active Directory Content Filtering",
                "HTTP Content Caching",
                "802.1x Port Authentication",
                "MX Splash Pages",
                "Dual WAN",
                "Trusted Traffic Exclusions",
            ],
            "Usage": (
                "Deploy vMX in public cloud environments to extend Meraki SD-WAN to cloud-hosted "
                "resources. Acts as a VPN concentrator for branch MX appliances connecting to AWS, "
                "Azure, or Alibaba Cloud workloads. Choose vMX-S for small deployments (up to 50 "
                "tunnels), vMX-M for medium (up to 250), and vMX-L for large (up to 1,000)."
            ),
            "Licensing": {
                "Tiers": "Enterprise, Advanced Security",
                "Terms": "1-year, 3-year, 5-year",
                "Note": "All vMX instances require a valid Meraki license to operate",
            },
        }
    },

    # SFP Accessories
    {
        "family": "Accessories",
        "name": "SFP and Stacking Accessories",
        "url": "https://documentation.meraki.com/MS/MS_Installation_Guides/SFP_and_Stacking_Accessories",
        "images": [],
        "content": {
            "Overview": (
                "Cisco Meraki offers branded SFP/QSFP fiber transceivers, direct attach cables, "
                "stacking cables, StackPower cables, and uplink modules compatible with Meraki MX "
                "and MS devices. Many Cisco Optics compatible with native Catalyst Switch platforms "
                "are also compatible with their Cloud Managed counterparts (e.g. C9300-M series). "
                "Third-party accessories may function but are not officially supported."
            ),
            "Features": [
                "1G SFP: Multi-mode (SX, OM1/OM2/OM3/OM4) and single-mode (LX10) transceivers",
                "1G SFP: Copper module (1000BASE-T) for twisted pair",
                "10G SFP+: SR (OM1-OM4), LR, LRM, ER, ZR variants",
                "40G QSFP: SR4, LR4, CSR4, SR-BD variants",
                "100G QSFP: LR4 and SR4 variants",
                "Direct attach (Twinax) cables: 10G SFP+ (1m, 3m)",
                "Stacking cables: 40G (50cm, 1m, 3m), 100G (50cm, 1m, 3m), 120G (50cm, 1m, 3m)",
                "Catalyst 9300/X StackWise cables: 480G/1Tbps (50cm, 1m, 3m)",
                "Catalyst 9300L stacking kit and cables: 320G",
                "StackPower cables: 30cm and 1.5m for MS390 and C9300/C9300X",
                "Uplink modules: 4x10G, 8x10G, 2x40G, 2x25G, 8x25G, 2x100G options",
            ],
            "Specifications": {
                "1G SX Multimode (MA-SFP-1GB-SX)": "850nm, MMF OM1-OM4, 220m-1km, Compatible: MX, MS series",
                "1G LX10 Singlemode (MA-SFP-1GB-LX10)": "1310nm, SMF OS1/OS2, 10km, Compatible: MX, MS series",
                "1G Copper (MA-SFP-1GB-TX)": "1000BASE-T, 100m, Compatible: All MX, all MS except MS130R/Catalyst",
                "10G SR Multimode (MA-SFP-10GB-SR)": "850nm, MMF OM1-OM4, 26m-400m, Compatible: MX, MS series",
                "10G LR Singlemode (MA-SFP-10GB-LR)": "1310nm, SMF OS1/OS2, 10km, Compatible: MX, MS series",
                "10G LRM Multimode (MA-SFP-10GB-LRM)": "1310nm, MMF/SMF, 220-300m, Compatible: MS series, C9300",
                "10G ER Singlemode (MA-SFP-10GB-ER)": "1550nm, SMF OS1/OS2, 40km, Compatible: MX, MS series",
                "10G ZR Singlemode (MA-SFP-10GB-ZR)": "1550nm, SMF OS1/OS2, 80km, Compatible: select MX models",
                "40G SR4 QSFP (MA-QSFP-40G-SR4)": "850nm, MMF OM2/OM3/OM4, 30-150m, Compatible: MS350/390/410/425, C9300",
                "40G LR4 QSFP (MA-QSFP-40G-LR4)": "1310nm, SMF OS1/OS2, 10km, Compatible: MS350/390/410/425, C9300",
                "40G CSR4 QSFP (MA-QSFP-40G-CSR4)": "850nm, MMF OM2/OM3/OM4, 82-400m, Compatible: MS350/390/410/425, C9300",
                "100G LR4 QSFP (MA-QSFP-100G-LR4)": "1295-1309nm, SMF OS1/OS2, 10km, Compatible: MS450",
                "100G SR4 QSFP (MA-QSFP-100G-SR4)": "850nm, MMF OM3/OM4, 70-100m, Compatible: MS450",
                "Direct Attach 10G 1m (MA-CBL-TA-1M)": "Passive Twinax, Compatible: MX95/105/250/450, MS125-450",
                "Direct Attach 10G 3m (MA-CBL-TA-3M)": "Passive Twinax, Compatible: MX95/105/250/450, MS125-450",
                "Stacking 40G 50cm (MA-CBL-40G-50CM)": "QSFP+ Twinax, Compatible: MS210/225/250/350/410/425",
                "Stacking 100G 50cm (MA-CBL-100G-50CM)": "QSFP28 Twinax, Compatible: MS150/355/450",
                "Stacking 120G 50cm (MA-CBL-120G-50CM)": "120G (480G), Compatible: MS390, C9300",
                "Catalyst 9300 Stack 50cm (STACK-T1-50CM-M)": "480G/1Tbps, Compatible: C9300/C9300X",
                "Catalyst 9300L Stack Kit (C9300L-STACK-KIT2-M)": "320G, Compatible: C9300L",
                "StackPower 30cm (MA-CBL-SPWR-30CM)": "Compatible: MS390",
                "StackPower 30cm Catalyst (CAB-SPWR-30CM-M)": "Compatible: C9300, C9300X",
                "Uplink Module 4x10G (MA-MOD-4x10G)": "4-port 1/10G SFP+, Compatible: MS390, C9300 (End of Sale)",
                "Uplink Module 8x10G (MA-MOD-8x10G)": "8-port 1/10G SFP+, Compatible: MS390, C9300",
                "Uplink Module 2x40G (MA-MOD-2x40G)": "2-port 40G QSFP+, Compatible: MS390, C9300",
                "Uplink Module 2x100G (C9300X-NM-2C-M)": "2-port 100G/40G QSFP28, Compatible: C9300X",
            },
            "Performance": {
                "1G transceivers": "Gigabit Ethernet",
                "10G transceivers": "10 Gigabit Ethernet",
                "40G transceivers": "40 Gigabit Ethernet",
                "100G transceivers": "100 Gigabit Ethernet",
                "Stacking bandwidth (120G cable)": "480 Gbps aggregate",
                "Stacking bandwidth (Catalyst 9300)": "480 Gbps or 1 Tbps",
            },
            "Usage": (
                "Used to extend fiber connectivity, enable stacking between Meraki switches, "
                "and add high-speed uplinks to MS390 and Catalyst 9300-M series. Select the "
                "appropriate transceiver based on distance requirements and fiber type available. "
                "Cisco Optics compatible with native Catalyst platforms are also compatible with "
                "corresponding cloud-managed Catalyst (-M) platforms including MS390."
            ),
            "Compatibility_Notes": [
                "Cisco Optics warranty handled by Cisco TAC (not Meraki warranty)",
                "Meraki support assists with troubleshooting Cisco Optics on cloud-managed switches",
                "Third-party accessories should be tested by user for compatibility",
                "MS130R does not support MA-SFP-1GB-TX copper module",
                "Catalyst 9300X does not support LRM modules",
                "MA-MOD-4x10G for MS390 is end of sale",
                "C9300X-NM-2C-M operates at 40Gbps in CS17 firmware; 100G requires IOS-XE 17.15+",
            ],
        }
    },
]


def save_output(products):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    json_path   = os.path.join(OUTPUT_FOLDER, "z4c_vmx_sfp_products.json")
    report_path = os.path.join(OUTPUT_FOLDER, "z4c_vmx_sfp_report.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    report_lines = [
        "CISCO Z4C / vMX / SFP ACCESSORIES SCRAPE REPORT",
        "=" * 50,
        f"Total products/entries: {len(products)}",
        "",
        "Entries extracted:",
    ]
    for p in products:
        specs = len(p["content"].get("Specifications", {}))
        feats = len(p["content"].get("Features", []))
        report_lines.append(
            f"  ✓ {p['name']:35s} | family: {p['family']:12s} | specs: {specs:2d} | features: {feats}"
        )
    report_lines += [
        "",
        "Source documents:",
        "  - Z4C_Datasheet.pdf (9 pages)",
        "  - vMX_Comparison_Datasheet.pdf (2 pages)",
        "  - Small-Form_Factor_Pluggable_(SFP)_and_Stacking_Accessories.pdf (15 pages)",
        "",
        "Notes:",
        "  - All data hardcoded directly from PDFs (no table parsing needed)",
        "  - vMX covers all 3 sizes (S/M/L) in one entry with per-size performance fields",
        "  - SFP entry covers all transceivers, stacking cables, and uplink modules",
        "  - 'images' field empty for all entries (PDFs have no extractable image URLs)",
        "  - Z4C has a lifetime hardware warranty",
        "  - vMX requires licensing (Enterprise or Advanced Security, 1/3/5-year)",
    ]

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"[SAVED] JSON   → {json_path}")
    print(f"[SAVED] Report → {report_path}")


def main():
    print("=" * 60)
    print("  Cisco Z4C / vMX / SFP Accessories Scraper")
    print("=" * 60)
    for p in PRODUCTS:
        specs = len(p["content"].get("Specifications", {}))
        feats = len(p["content"].get("Features", []))
        print(f"[BUILT] {p['name']:35s} | {specs} specs | {feats} features")
    save_output(PRODUCTS)
    print("\n" + "=" * 60)
    print(f"  ✅ DONE! {len(PRODUCTS)} entries saved.")
    print(f"  Output: {OUTPUT_FOLDER}")
    print("=" * 60)


if __name__ == "__main__":
    main()
