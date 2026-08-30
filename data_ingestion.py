import os
import subprocess
import json
import urllib.request
import urllib.parse
import ssl
from datetime import datetime

# SSL Sertifika hatasını bypass etmek için
ssl._create_default_https_context = ssl._create_unverified_context

class HybridIngestionEngine:
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.knowledge_dir = os.path.join(vault_path, "Knowledge")
        
    def fetch_curated_data(self, url: str, topic: str):
        # Güvenilir kaynaklardan (örn. GitHub raw, arXiv) veri çeker
        pass
        
    def autonomous_search(self, query: str):
        """Wikipedia API üzerinden otonom arama simülasyonu"""
        print(f"[*] Arastiriliyor: {query}")
        try:
            url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'LokumAI-Crawler/1.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
            title = data.get("title", query)
            extract = data.get("extract", "İçerik bulunamadı.")
            
            # Obsidian'a kaydet
            self.save_as_obsidian_node(
                title=title, 
                content=extract, 
                links=["Araştırma", "Cognitive_Core"], 
                tags=["research", query.replace(" ", "_")]
            )
            print(f"[+] '{title}' graph'a eklendi.")
        except Exception as e:
            print(f"[-] Hata ({query}): {e}")

    def save_as_obsidian_node(self, title: str, content: str, links: list, tags: list):
        file_path = os.path.join(self.knowledge_dir, f"{title.replace(' ', '_').replace('/', '_')}.md")
        
        frontmatter = "---\n"
        frontmatter += f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
        frontmatter += "tags:\n"
        for tag in tags:
            frontmatter += f"  - {tag}\n"
        frontmatter += "---\n\n"
        
        body = f"# {title}\n\n{content}\n\n## İlgili Kavramlar (Semantic Links)\n"
        for link in links:
            body += f"- [[{link}]]\n"
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + body)
        return file_path

if __name__ == "__main__":
    vault = "/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0"
    engine = HybridIngestionEngine(vault)
    
    topics = [
        "Siber_güvenlik", 
        "Kriptografi", 
        "Gömülü_sistemler",
        "Yapay_zeka"
    ]
    
    for topic in topics:
        engine.autonomous_search(topic)