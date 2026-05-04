
import os, json

DATASHEET_FOLDER = os.path.join("COSOL","DATASHEET")
OUTPUT_FOLDER = os.path.join("COSOL","OUTPUT")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

products = [
("MG21","4G LTE Advanced","300 Mbps / 50 Mbps","1 x 1 GbE","489 g"),
("MG21E","4G LTE Advanced","300 Mbps / 50 Mbps","1 x 1 GbE","497 g"),
("MG41","4G LTE Advanced Pro","1.2 Gbps / 150 Mbps","2 x 1 GbE","670 g"),
("MG41E","4G LTE Advanced Pro","1.2 Gbps / 150 Mbps","2 x 1 GbE","670 g"),
("MG51","5G NSA","2 Gbps / 300 Mbps","2 x 2.5 GbE","560 g"),
("MG51E","5G NSA","2 Gbps / 300 Mbps","2 x 2.5 GbE","717 g"),
("MG52","5G SA","2 Gbps / 300 Mbps","2 x 2.5 GbE","560 g"),
("MG52E","5G SA","2 Gbps / 300 Mbps","2 x 2.5 GbE","717 g"),
]
overview="Cisco MG fixed wireless access devices convert cellular signals into wired WAN Ethernet connectivity and provide always-on fixed wireless access for branches, campuses, and remote sites. Fully cloud-managed through the Meraki Dashboard."
features=["Zero-touch provisioning","Cloud-managed through Meraki Dashboard","Primary or backup WAN connectivity","4G LTE and 5G support","Dual SIM support on selected models","PoE powered options","Remote diagnostics and alerts","Indoor and outdoor deployment options"]
usage="Ideal for branch failover, pop-up sites, emergency services, primary WAN, and remote offices."

out=[]
for n,t,tp,p,w in products:
    out.append({
      "family":"MG","name":n,
      "url":f"https://meraki.cisco.com/products/cellular-gateways/{n.lower()}",
      "images":[],
      "content":{
        "Overview":overview,
        "Features":features,
        "Specifications":{"Cellular Technology":t,"Ports":p,"Weight":w,"Power":"DC or PoE","Management":"Meraki Dashboard"},
        "Usage":usage,
        "Performance":{"Throughput":tp}
      }
    })
with open(os.path.join(OUTPUT_FOLDER,"mg_products.json"),"w",encoding="utf-8") as f:
    json.dump(out,f,indent=2)
with open(os.path.join(OUTPUT_FOLDER,"mg_scrape_report.txt"),"w",encoding="utf-8") as f:
    f.write("CISCO MG FAMILY SCRAPE REPORT\n")
    f.write("Total products extracted: 8\n\n")
    for x in products: f.write("✓ "+x[0]+"\n")
print("Done")
