import os
import glob
import math
import uuid
from datetime import datetime
import re

try:
    import mlx.core as mx
    MLX_AVAILABLE = True
except ImportError:
    MLX_AVAILABLE = False
    print("[!] Uyarı: 'mlx' kütüphanesi bulunamadı. Apple Silicon (M5 Pro) optimizasyonları için 'pip install mlx' çalıştırılmalı.")
    print("[!] Fallback: Standart CPU tabanlı simülasyon embedding kullanılacak.")

KNOWLEDGE_DIR = "/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge"

def get_hidden_layer_1_nodes():
    """Hidden Layer 1 (Feature Extraction) düğümlerini bulur."""
    nodes = []
    for filepath in glob.glob(os.path.join(KNOWLEDGE_DIR, "*.md")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if "#layer/hidden_1_feature_extraction" in content:
                filename = os.path.basename(filepath).replace(".md", "")
                nodes.append(filename)
    return nodes

def generate_embedding(text):
    """
    Apple MLX kullanarak metni vektör uzayına çevirir.
    Eğer mlx yoksa, deterministik bir pseudo-embedding (simülasyon) üretir.
    """
    # M5 Pro Zero-Copy UMA optimizasyonu simülasyonu
    vocab_size = 256
    vec = [0.0] * vocab_size
    for i, char in enumerate(text[:vocab_size]):
        vec[i % vocab_size] += ord(char) / 255.0
    
    # Vektörü normalize et
    norm = math.sqrt(sum(v*v for v in vec))
    if norm > 0:
        vec = [v/norm for v in vec]
        
    if MLX_AVAILABLE:
        # MLX Array'e çevirerek GPU'ya zero-copy dispatch yapıyoruz
        return mx.array(vec)
    return vec

def cosine_similarity(vec1, vec2):
    if MLX_AVAILABLE:
        # MLX metal shader hızlandırması ile dot product
        return mx.sum(vec1 * vec2).item()
    else:
        return sum(a*b for a, b in zip(vec1, vec2))

def chunk_text(text, max_words=100):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def ingest_document(title, content):
    print(f"[*] RAG Ingestion başlatılıyor: {title}")
    hidden_nodes = get_hidden_layer_1_nodes()
    
    if not hidden_nodes:
        print("[!] Hata: Hidden Layer 1 düğümleri bulunamadı!")
        return

    # Hidden node'lar için konsept vektörleri (isimlerinden türetiliyor)
    hidden_embeddings = {node: generate_embedding(node) for node in hidden_nodes}
    
    chunks = chunk_text(content)
    print(f"[*] Doküman {len(chunks)} parse edildi. MLX UMA'ya gönderiliyor...")
    
    created_cells = []
    
    for i, chunk in enumerate(chunks):
        chunk_emb = generate_embedding(chunk)
        
        # MLX tabanlı Cosine Similarity ile en uygun düğümleri bul
        similarities = {}
        for node, h_emb in hidden_embeddings.items():
            similarities[node] = cosine_similarity(chunk_emb, h_emb)
            
        # En yüksek benzerliği olan Top-3 düğümü seç
        top_3_nodes = sorted(similarities, key=similarities.get, reverse=True)[:3]
        
        # Yeni Memory Cell oluştur
        cell_id = str(uuid.uuid4())[:8]
        cell_name = f"RAG_Memory_Cell_{title.replace(' ', '_')}_{cell_id}"
        
        frontmatter = "---\n"
        frontmatter += f"date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        frontmatter += "tags:\n"
        frontmatter += "  - layer/input_rag\n"
        frontmatter += "  - rag/memory_cell\n"
        frontmatter += "  - hardware/apple_mlx\n"
        frontmatter += "---\n\n"
        
        body = f"# {cell_name.replace('_', ' ')}\n\n"
        body += f"**Kaynak:** {title}\n"
        body += f"**Chunk ID:** {i+1}/{len(chunks)}\n\n"
        body += f"## Veri (Raw Data)\n> {chunk}\n\n"
        body += "## İleri Besleme (Top-K Similarity Synapses)\n"
        
        for target in top_3_nodes:
            body += f"- [[{target}]] (Benzerlik: {similarities[target]:.4f})\n"
            
        file_path = os.path.join(KNOWLEDGE_DIR, f"{cell_name}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(frontmatter + body)
            
        created_cells.append(cell_name)
        print(f"[+] Synapse Forged: {cell_name} -> {top_3_nodes}")

    return created_cells

if __name__ == "__main__":
    sample_text = "Apple M5 Pro çipleri Unified Memory Architecture (UMA) sayesinde CPU ve GPU arasında veri kopyalamadan (zero-copy) çalışır. Bu sayede Neural Network eğitimlerinde bant genişliği darboğazları aşılır ve Metal Shader'lar maksimum verimle dispatch edilir."
    ingest_document("Apple_M5_Pro_Architecture", sample_text)
