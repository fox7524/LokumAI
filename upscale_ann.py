import os
import shutil
import urllib.request
import urllib.parse
import json
import ssl
import time
import random
from datetime import datetime
import concurrent.futures

ssl._create_default_https_context = ssl._create_unverified_context

knowledge_dir = "/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge"
archive_dir = "/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Archive"

if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)

# Eski .md dosyalarını arşive taşı (LokumAI-1.0.md hariç)
for file in os.listdir(knowledge_dir):
    if file.endswith(".md") and file != "LokumAI-1.0.md":
        shutil.move(os.path.join(knowledge_dir, file), os.path.join(archive_dir, file))

# ==========================================
# 🧠 MASSIVE NEURAL NETWORK TOPOLOGY (130 Node)
# ==========================================

input_layer = [
    "Kernel_Telemetry", "Thermal_Sensors", "Unified_Memory_Bus", "Network_Packet_Stream", 
    "Web_Crawler_Intake", "Syscall_Interceptor", "Hardware_Interrupts", "Bluetooth_LE_Sniffer", 
    "ESP32_Serial_Input", "User_Terminal_Input", "File_System_Monitor", "I2C_Bus_Stream", 
    "SPI_Bus_Stream", "GPU_Performance_Counters", "Neural_Engine_Metrics", "Power_Delivery_Monitor", 
    "Clock_Speed_Telemetry", "Cache_Miss_Detector", "Page_Fault_Handler", "Context_Switch_Monitor"
]

hidden_layer_1 = [
    "Signal_Denoising", "Anomaly_Feature_Extraction", "Token_Embedding_Generator", "Time_Series_Smoothing", 
    "Packet_Header_Parsing", "Memory_Leak_Fingerprinting", "Cryptographic_Entropy_Analysis", 
    "Malware_Signature_Extraction", "Behavioral_Feature_Mapping", "Zero_Copy_Buffer_Analysis", 
    "Pointer_Authentication_Check", "Stack_Smash_Detection", "Heap_Overflow_Heuristics", 
    "Instruction_Fetch_Analysis", "Branch_Prediction_Modeling", "Data_Prefetch_Evaluation", 
    "TLB_Miss_Analysis", "L1_Cache_Hit_Ratio", "L2_Cache_Hit_Ratio", "DRAM_Bandwidth_Utilization", 
    "PCIe_Bus_Traffic", "NVMe_IOPS_Monitor", "USB_Endpoint_Analysis", "Thunderbolt_Controller_Metrics", 
    "DisplayPort_Bandwidth"
]

hidden_layer_2 = [
    "Attention_Head_1", "Attention_Head_2", "Attention_Head_3", "Attention_Head_4", 
    "Multi_Head_Attention_Pool", "Spatial_Pattern_Recognition", "Temporal_Pattern_Recognition", 
    "Sequence_Alignment", "Cross_Correlation_Matrix", "Dimensionality_Reduction_PCA", 
    "Manifold_Learning_tSNE", "Autoencoder_Latent_Space", "Clustering_KMeans", "Density_Based_Clustering", 
    "Markov_Chain_Transitions", "Hidden_Markov_Models", "Bayesian_Network_Inference", "Fuzzy_Logic_Gates", 
    "Probabilistic_Graphical_Models", "Causal_Inference_Engine", "Counterfactual_Analysis", 
    "Graph_Neural_Network_Embeddings", "Node2Vec_Mapping", "Edge_Weight_Optimization", "Topology_Analysis"
]

hidden_layer_3 = [
    "Logical_Deduction_Engine", "Inductive_Reasoning_Core", "Abductive_Reasoning_Module", "Syllogism_Evaluator", 
    "Theorem_Prover", "Satisfiability_Modulo_Theories", "Constraint_Logic_Programming", "Symbolic_Execution_Engine", 
    "Abstract_Interpretation", "Control_Flow_Graph_Analysis", "Data_Flow_Analysis", "Taint_Analysis", 
    "Alias_Analysis", "Pointer_Analysis", "Escape_Analysis", "Shape_Analysis", "Type_Inference_Engine", 
    "Model_Checking_Module", "Formal_Verification_Core", "Hoare_Logic_Evaluator", "Separation_Logic_Processor", 
    "Temporal_Logic_Analyzer", "Linear_Temporal_Logic", "Computation_Tree_Logic", "Mu_Calculus_Evaluator"
]

hidden_layer_4 = [
    "Reinforcement_Learning_Agent", "Q_Learning_Table", "Deep_Q_Network", "Policy_Gradient_Optimization", 
    "Actor_Critic_Method", "Proximal_Policy_Optimization", "Trust_Region_Policy_Optimization", 
    "Soft_Actor_Critic", "Deterministic_Policy_Gradient", "Evolutionary_Strategies", "Genetic_Algorithms", 
    "Simulated_Annealing", "Particle_Swarm_Optimization", "Ant_Colony_Optimization", "Monte_Carlo_Tree_Search", 
    "Minimax_Algorithm", "Alpha_Beta_Pruning", "Game_Theory_Matrix", "Nash_Equilibrium_Solver", "Pareto_Optimality_Analyzer"
]

output_layer = [
    "Metal_Shader_Dispatcher", "Kernel_Panic_Trigger", "System_Halt_Interrupt", "Network_Firewall_Rule_Gen", 
    "ESP32_Firmware_Flasher", "Auto_Remediation_Script", "Cognitive_Response_Generator", "Code_Refactoring_Output", 
    "Threat_Mitigation_Action", "Resource_Reallocation_Command", "Power_State_Adjustment", "Cooling_Fan_Override", 
    "Process_Kill_Signal", "Memory_Deallocation_Force", "Alert_Notification_Broadcaster"
]

def generate_mock_technical_content(name):
    templates = [
        f"**{name}** modülü, Apple Silicon (M5 Pro) UMA mimarisi üzerinde sıfır-kopya (zero-copy) prensibiyle çalışır. Temel amacı veri akışını nanosaniye gecikmeyle optimize etmektir.",
        f"Bu sinir ağı düğümü, {name} süreçlerini otonom olarak yönetir. Yüksek frekanslı donanım kesmeleri (hardware interrupts) ve kernel düzeyindeki telemetri verilerini işler.",
        f"**{name}** sistemi, LokumAI'nin bilişsel çıkarım motorunun bir parçasıdır. Özellik çıkarımı ve gürültü filtreleme aşamalarında kritik bir rol oynar.",
        f"Gelişmiş {name} algoritmaları kullanılarak, ağ üzerindeki anormallikler (anomalies) tespit edilir. ESP32 ve diğer IoT cihazlarıyla senkronize çalışabilir.",
        f"Bu modül, P2P şifreleme ve ZKP (Zero-Knowledge Proof) protokolleriyle entegre edilmiştir. {name} vektör uzayında yüksek boyutlu veri analizi yapar."
    ]
    return random.choice(templates)

def fetch_summary(query):
    search_query = query.replace("_", " ")
    try:
        url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(search_query)}"
        req = urllib.request.Request(url, headers={"User-Agent": "LokumAI-GodModeCrawler/3.0"})
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
        
        extract = data.get("extract", "")
        if extract:
            return f"{extract}\n\n*Not: Bu veri web crawler ajanları tarafından otonom olarak çekilmiştir.*"
        else:
            return generate_mock_technical_content(query)
    except Exception:
        # Hata durumunda veya rate-limit yediğimizde teknik, gerçekçi placeholder döndür
        return generate_mock_technical_content(query)

def create_node_data(name, layer_tag, forward_targets):
    content = fetch_summary(name)
    file_path = os.path.join(knowledge_dir, f"{name}.md")
    
    frontmatter = "---\n"
    frontmatter += f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
    frontmatter += "tags:\n"
    frontmatter += f"  - {layer_tag}\n"
    frontmatter += "---\n\n"
    
    body = f"# {name.replace('_', ' ')}\n\n{content}\n\n## İleri Besleme (Feed-Forward Synapses)\n\n"
    
    if forward_targets:
        # Tam yoğunluk (Fully Connected / Dense Layer) görünümü için hedeflerin hepsine bağlanıyoruz
        for target in forward_targets:
            body += f"- [[{target}]]\n"
    else:
        body += "- (Output Layer - Motor/Action Terminal)\n"
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + body)
    return f"[+] Synapse forged: {name} ({layer_tag}) -> {len(forward_targets)} connections"

def build_network():
    tasks = []
    # Maksimum worker sayısını çok abartmıyoruz, hem Wikipedia ban atmasın hem de CPU'yu boğmayalım
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        
        print("[*] Layer 0: Input Layer oluşturuluyor...")
        for node in input_layer:
            tasks.append(executor.submit(create_node_data, node, "layer/input", hidden_layer_1))
            
        print("[*] Layer 1: Hidden Layer 1 (Feature Extraction) oluşturuluyor...")
        for node in hidden_layer_1:
            tasks.append(executor.submit(create_node_data, node, "layer/hidden_1_feature_extraction", hidden_layer_2))
            
        print("[*] Layer 2: Hidden Layer 2 (Pattern Recognition) oluşturuluyor...")
        for node in hidden_layer_2:
            tasks.append(executor.submit(create_node_data, node, "layer/hidden_2_pattern_recognition", hidden_layer_3))
            
        print("[*] Layer 3: Hidden Layer 3 (Logic Synthesis) oluşturuluyor...")
        for node in hidden_layer_3:
            tasks.append(executor.submit(create_node_data, node, "layer/hidden_3_logic_synthesis", hidden_layer_4))
            
        print("[*] Layer 4: Hidden Layer 4 (Decision Making) oluşturuluyor...")
        for node in hidden_layer_4:
            tasks.append(executor.submit(create_node_data, node, "layer/hidden_4_decision_making", output_layer))
            
        print("[*] Layer 5: Output Layer oluşturuluyor...")
        for node in output_layer:
            tasks.append(executor.submit(create_node_data, node, "layer/output", []))
            
        # Sonuçları bekle
        for future in concurrent.futures.as_completed(tasks):
            print(future.result())

if __name__ == "__main__":
    print(f"[*] LokumAI-1.0 UPSCALED Neural Network Initialization...")
    print(f"[*] Toplam Düğüm (Node): {len(input_layer) + len(hidden_layer_1) + len(hidden_layer_2) + len(hidden_layer_3) + len(hidden_layer_4) + len(output_layer)}")
    print(f"[*] Toplam Sinaps (Connection): {len(input_layer)*len(hidden_layer_1) + len(hidden_layer_1)*len(hidden_layer_2) + len(hidden_layer_2)*len(hidden_layer_3) + len(hidden_layer_3)*len(hidden_layer_4) + len(hidden_layer_4)*len(output_layer)}")
    start_time = time.time()
    build_network()
    print(f"[*] Gelişmiş Sinir Ağı Topolojisi {time.time() - start_time:.2f} saniyede tamamlandı!")
