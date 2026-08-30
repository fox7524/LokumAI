import os
import shutil
import urllib.request
import urllib.parse
import json
import ssl
from datetime import datetime
import concurrent.futures

ssl._create_default_https_context = ssl._create_unverified_context

knowledge_dir = "/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge"
archive_dir = "/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Archive"

if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)

for file in os.listdir(knowledge_dir):
    if file.endswith(".md"):
        shutil.move(os.path.join(knowledge_dir, file), os.path.join(archive_dir, file))

input_layer = [
    "Core_Temperature_Sensors", "Memory_Bandwidth_Monitors", "Network_Packet_Sniffer", 
    "User_Terminal_Input", "Web_Crawler_Stream", "File_System_Events", 
    "Syscall_Hooks", "Bluetooth_LE_Scanner", "I2C_Bus_Analyzer", 
    "GPU_Compute_Metrics", "Neural_Engine_Load", "Power_Delivery_Sensors"
]

hidden_layer_1 = [
    "Feature_Extraction_Pipeline", "Token_Embedding_Space", "Time_Series_Analysis", 
    "Anomaly_Detection_Filter", "Packet_Deep_Inspection", "Memory_Leak_Heuristics", 
    "Contextual_Attention_Heads", "Dimensionality_Reduction", "Noise_Cancellation_Gates", 
    "Cryptographic_Entropy_Check", "Malware_Signature_Match", "Zero_Copy_Buffer_Pools", 
    "Hardware_Interrupt_Router", "Semantic_Parser", "Threat_Vector_Analysis", "Behavioral_Pattern_Matcher"
]

hidden_layer_2 = [
    "Non_Linear_Activation", "Multi_Head_Attention", "Gradient_Flow_Optimization", 
    "State_Machine_Inference", "Predictive_Execution_Model", "Vulnerability_Scoring", 
    "Resource_Allocation_Policy", "Quantum_Resistant_Filter", "Heuristic_Decision_Tree", 
    "Reinforcement_Reward_Calc", "Dynamic_Routing_Table", "Memory_Safety_Validator", 
    "Payload_Deobfuscation", "Trust_Score_Aggregator", "Logic_Synthesis_Engine", "Autonomous_Reasoning_Core"
]

output_layer = [
    "Metal_Shader_Dispatch", "Kernel_Panic_Alert", "Auto_Remediation_Trigger", 
    "Code_Generation_Output", "Network_Block_Rule", "ESP32_Firmware_Flash", 
    "Cognitive_Response_Log", "System_Halt_Command"
]

def fetch_summary(query):
    search_query = query.replace("_", " ")
    try:
        url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(search_query)}"
        req = urllib.request.Request(url, headers={"User-Agent": "LokumAI-AdvancedCrawler/2.0"})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
        return data.get("extract", f"Gelişmiş {search_query} sinir ağı modülü. (Eşzamanlı tarama ile oluşturuldu)")
    except Exception:
        return f"{search_query} işlemleri için optimize edilmiş, donanım hızlandırmalı otonom sinir ağı düğümü."

def create_node_data(name, layer_tag, forward_targets):
    content = fetch_summary(name)
    file_path = os.path.join(knowledge_dir, f"{name}.md")
    
    frontmatter = "---\n"
    frontmatter += f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
    frontmatter += "tags:\n"
    frontmatter += f"  - {layer_tag}\n"
    frontmatter += "---\n\n"
    
    body = f"# {name.replace('_', ' ')}\n\n{content}\n\n## İleri Besleme (Feed-Forward Synapses)\n"
    
    if forward_targets:
        for target in forward_targets:
            body += f"- [[{target}]]\n"
    else:
        body += "- (Output Layer - Motor/Action Terminal)\n"
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + body)
    return f"[+] Synapse forged: {name} ({layer_tag})"

def build_network():
    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for node in input_layer:
            tasks.append(executor.submit(create_node_data, node, "layer/input", hidden_layer_1))
        for node in hidden_layer_1:
            tasks.append(executor.submit(create_node_data, node, "layer/hidden_1", hidden_layer_2))
        for node in hidden_layer_2:
            tasks.append(executor.submit(create_node_data, node, "layer/hidden_2", output_layer))
        for node in output_layer:
            tasks.append(executor.submit(create_node_data, node, "layer/output", []))
            
        for future in concurrent.futures.as_completed(tasks):
            print(future.result())

if __name__ == "__main__":
    print("[*] Eşzamanlı (Concurrent) Web Crawling ve Synapse inşası başlıyor...")
    build_network()
    print("[*] Gelişmiş Sinir Ağı Topolojisi tamamlandı!")
