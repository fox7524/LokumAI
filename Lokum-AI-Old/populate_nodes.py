import os
import urllib.request
import urllib.parse
import json
import ssl
from datetime import datetime
import random

ssl._create_default_https_context = ssl._create_unverified_context

knowledge_dir = "/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge"

categories = {
    "AI_and_ML": ["Large_language_model", "Transformer_model", "Quantization", "Apple_M1", "Neural_network", "Self-attention", "Machine_learning", "Deep_learning", "Generative_pre-trained_transformer", "Ollama", "Apple_MLX", "Tensor", "Vector_database"],
    "Hardware_and_Embedded": ["Microcontroller", "ESP32", "FreeRTOS", "Direct_memory_access", "I2C", "Serial_Peripheral_Interface", "System_on_a_chip", "Interrupt", "Computer_architecture", "Assembly_language", "Low-level_programming_language", "Memory_management"],
    "Security_and_Crypto": ["Public-key_cryptography", "Zero-knowledge_proof", "End-to-end_encryption", "Memory_safety", "Rust_(programming_language)", "Buffer_overflow", "Cybersecurity", "Transport_Layer_Security", "Cryptographic_hash_function", "Man-in-the-middle_attack", "Digital_signature"]
}

all_topics = [topic for sublist in categories.values() for topic in sublist]

def fetch_summary(query):
    try:
        url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={"User-Agent": "LokumAI-Crawler/1.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        return data.get("title", query), data.get("extract", "Bu konu Wikipedia'da tam eşleşmedi, ancak Sentetik Beyin tarafından ağa bir kavramsal düğüm olarak eklendi.")
    except Exception:
        return query.replace("_", " "), "İçerik çekilemedi, ancak ağın bütünlüğü için bir düğüm olarak eklendi."

def save_node(title, content, category, links):
    file_path = os.path.join(knowledge_dir, f"{title.replace(' ', '_').replace('/', '_')}.md")
    tags = ["research", "node", category]
    
    frontmatter = "---\n"
    frontmatter += f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
    frontmatter += "tags:\n"
    for tag in tags:
        frontmatter += f"  - {tag}\n"
    frontmatter += "---\n\n"
    
    body = f"# {title}\n\n{content}\n\n## İlgili Kavramlar (Semantic Links)\n"
    body += "- [[LokumAI-1.0]]\n"
    for link in links:
        body += f"- [[{link.replace('_', ' ')}]]\n"
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + body)
    print(f"[+] Node created: {title}")

for cat in categories.keys():
    save_node(cat, f"{cat} alanındaki tüm araştırmaların merkez düğümü.", "hub", categories[cat][:5])

for cat, topics in categories.items():
    for topic in topics:
        title, content = fetch_summary(topic)
        same_cat_links = random.sample([t for t in topics if t != topic], min(5, len(topics)-1))
        other_cat_links = random.sample([t for t in all_topics if t not in topics], 3)
        all_links = same_cat_links + other_cat_links + [cat]
        save_node(title, content, cat, all_links)
