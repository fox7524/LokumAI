import os
import shutil
import urllib.request
import urllib.parse
import json
import ssl
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context

knowledge_dir = "/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge"
archive_dir = "/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Archive"

if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)

for file in os.listdir(knowledge_dir):
    if file.endswith(".md") and file != "LokumAI-1.0.md":
        shutil.move(os.path.join(knowledge_dir, file), os.path.join(archive_dir, file))

input_layer = ["Sensors_Data", "User_Prompt", "Hardware_Telemetry", "Web_Crawler_Input"]
hidden_layer_1 = ["Tokenization", "Signal_Processing", "Noise_Reduction", "Feature_Extraction", "Syntax_Analysis"]
hidden_layer_2 = ["Attention_Mechanism", "Zero_Copy_Routing", "Context_Window", "Weight_Matrices", "Activation_Functions"]
output_layer = ["Code_Generation", "Hardware_Control", "Security_Alert", "Cognitive_Response"]

def fetch_summary(query):
    try:
        url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query.replace('_', ' '))}"
        req = urllib.request.Request(url, headers={"User-Agent": "LokumAI-Crawler/1.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        return data.get("extract", "Kavramsal ANN düğümü (Otonom araştırma verisi).")
    except Exception:
        return "Kavramsal ANN düğümü (Bağlantı için oluşturuldu)."

def save_ann_node(name, layer_tag, forward_links):
    file_path = os.path.join(knowledge_dir, f"{name}.md")
    
    frontmatter = "---\n"
    frontmatter += f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
    frontmatter += "tags:\n"
    frontmatter += f"  - {layer_tag}\n"
    frontmatter += "---\n\n"
    
    content = fetch_summary(name)
    
    body = f"# {name.replace('_', ' ')}\n\n{content}\n\n## İleri Besleme (Feed-Forward Connections)\n"
    
    if forward_links:
        for link in forward_links:
            body += f"- [[{link}]]\n"
    else:
        body += "- (Output Node - İleri bağlantı yok)\n"
        body += "- [[LokumAI-1.0]]\n"
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + body)
    print(f"[+] {layer_tag} node created: {name}")

for node in input_layer:
    save_ann_node(node, "layer/input", hidden_layer_1)

for node in hidden_layer_1:
    save_ann_node(node, "layer/hidden_1", hidden_layer_2)

for node in hidden_layer_2:
    save_ann_node(node, "layer/hidden_2", output_layer)

for node in output_layer:
    save_ann_node(node, "layer/output", [])
