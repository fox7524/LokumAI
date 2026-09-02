import os
import glob
import random
from datetime import datetime

KNOWLEDGE_DIR = "/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge"

# Trae Work Ajanı Tarafından Bulunan Deep Research Yeni Düğümler (40+ Node)
new_nodes = {
    "layer/hidden_1_feature_extraction": ["Quantum_Noise_Reduction", "Thermal_Throttling_Heuristics", "CPU_Microcode_Telemetry", "L3_Cache_Snooping", "DMA_Ring_Buffer_Analysis"],
    "layer/hidden_2_pattern_recognition": ["Non_Euclidean_Manifolds", "Hyperbolic_Embeddings", "Tensor_Core_Scheduling", "Neuromorphic_Spike_Trains", "Hopfield_Energy_Minimization"],
    "layer/hidden_3_logic_synthesis": ["Abstract_Syntax_Tree_Eval", "Def_Use_Chain_Analysis", "Cyber_Kill_Chain_Modeling", "Advanced_Persistent_Threat_Sim", "Cryptographic_Nonce_Validation"],
    "layer/hidden_4_decision_making": ["Deep_Deterministic_Policy_Grad", "Multi_Agent_RL_Coordinator", "Swarm_Intelligence_Routing", "Bayesian_Optimization_Oracle", "Markov_Decision_Process_Solver"],
    "layer/hidden_5_advanced_synthesis": ["Zero_Knowledge_Rollups", "Fully_Homomorphic_Encryption", "Post_Quantum_Cryptography", "Lattice_Based_Crypto", "Hardware_Root_Of_Trust"],
    "layer/hidden_6_meta_cognition": ["Epistemological_Uncertainty_Calc", "Ontological_Graph_Mapper", "Semantic_Drift_Detector", "Cognitive_Dissonance_Resolver", "Heuristic_Bias_Filter"],
    "layer/hidden_7_strategic_planning": ["Game_Theoretic_Threat_Model", "Nash_Equilibrium_Enforcer", "Byzantine_Fault_Tolerance", "Asymmetric_Warfare_Sim", "Strategic_Resource_Allocator"],
    "layer/hidden_8_decision_assembly": ["Final_Execution_Gate", "Moral_Turing_Test", "Fail_Deadly_Switch", "Autonomous_Kill_Chain_Auth", "God_Mode_Overrides"]
}

# Var olan düğümleri katmanlarına göre bul (Hedef linkler için)
existing_nodes = {}
for filepath in glob.glob(os.path.join(KNOWLEDGE_DIR, "*.md")):
    name = os.path.basename(filepath).replace(".md", "")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        if "layer/hidden_2" in content: existing_nodes.setdefault("h2", []).append(name)
        elif "layer/hidden_3" in content: existing_nodes.setdefault("h3", []).append(name)
        elif "layer/hidden_4" in content: existing_nodes.setdefault("h4", []).append(name)
        elif "layer/hidden_5" in content: existing_nodes.setdefault("h5", []).append(name)
        elif "layer/hidden_6" in content: existing_nodes.setdefault("h6", []).append(name)
        elif "layer/hidden_7" in content: existing_nodes.setdefault("h7", []).append(name)
        elif "layer/hidden_8" in content: existing_nodes.setdefault("h8", []).append(name)
        elif "layer/output" in content: existing_nodes.setdefault("out", []).append(name)

# Hangi katmanın nereye besleneceği (Feed-Forward)
next_layer_map = {
    "layer/hidden_1_feature_extraction": "h2",
    "layer/hidden_2_pattern_recognition": "h3",
    "layer/hidden_3_logic_synthesis": "h4",
    "layer/hidden_4_decision_making": "h5",
    "layer/hidden_5_advanced_synthesis": "h6",
    "layer/hidden_6_meta_cognition": "h7",
    "layer/hidden_7_strategic_planning": "h8",
    "layer/hidden_8_decision_assembly": "out"
}

print("[*] Side-by-Side Trae Agent Deep Research Entegrasyonu Başlatılıyor...")
nodes_added = 0
links_added = 0

for layer_tag, nodes in new_nodes.items():
    next_key = next_layer_map[layer_tag]
    possible_targets = existing_nodes.get(next_key, [])
    
    for node in nodes:
        file_path = os.path.join(KNOWLEDGE_DIR, f"{node}.md")
        frontmatter = f"---\ndate: {datetime.now().strftime('%Y-%m-%d')}\ntags:\n  - {layer_tag}\n---\n\n"
        body = f"# {node.replace('_', ' ')}\n\n"
        body += f"**[!] Trae Side-by-Side Agent Eklemesi:** Bu düğüm, `{layer_tag}` katmanının derinleştirilmesi için otonom araştırma ajanı (Trae Work) tarafından ağa dahil edilmiştir. \n\n"
        body += f"Bu modül {node.replace('_', ' ')} üzerine yüksek yoğunluklu matematiksel ve sistemsel işlemler yaparak veriyi bir sonraki katmana rafine edilmiş (distilled) olarak iletir.\n\n"
        body += "## İleri Besleme (Feed-Forward Synapses)\n\n"
        
        if possible_targets:
            # 3 ila 6 arası hedef düğüme (sinaps) bağlan
            num_links = random.randint(3, 6)
            targets = random.sample(possible_targets, min(len(possible_targets), num_links))
            for t in targets:
                body += f"- [[{t}]]\n"
                links_added += 1
        else:
            body += "- (Output Terminal)\n"
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(frontmatter + body)
        print(f"[+] Düğüm eklendi: {node} ({layer_tag})")
        nodes_added += 1

print(f"[*] İşlem Tamamlandı. {nodes_added} yeni düğüm, {links_added} yeni sinaps ağa entegre edildi.")