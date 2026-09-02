import os
import glob
import json
import re

KNOWLEDGE_DIR = "/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge"
OUTPUT_JSON = "/Users/fox/Documents/PROJECTS/LokumAI/web_ui/graph_data.json"
STANDALONE_HTML = "/Users/fox/Documents/PROJECTS/LokumAI/LokumAI_Graphify.html"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S | re.M)

def parse_frontmatter_block(content: str) -> str:
    match = FRONTMATTER_RE.search(content)
    return match.group(1) if match else ""

def parse_frontmatter_list(frontmatter: str, key: str) -> list[str]:
    # Minimal YAML list parser for patterns:
    # key:
    #   - "A"
    #   - "B"
    lines = frontmatter.splitlines()
    values: list[str] = []
    in_block = False
    indent_prefix = None
    for line in lines:
        if not in_block:
            if line.strip() == f"{key}:":
                in_block = True
                continue
            continue

        # Stop if another top-level key starts
        if line and not line.startswith(" ") and ":" in line:
            break

        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            raw = stripped[2:].strip().strip('"').strip("'")
            if raw:
                values.append(raw)
    return values

def generate_graph_data():
    nodes = []
    links = []
    node_ids = set()

    # Renk paleti katmanlara göre (Dinamik kısmi eşleştirme)
    def get_color(tag):
        if "input_rag" in tag: return "#facc15"
        if "input" in tag: return "#4ade80"
        if "output" in tag: return "#ff0000" # Tam kırmızı (Output)
        if "hidden_10" in tag: return "#9f1239" # Rose-800
        if "hidden_9" in tag: return "#be123c" # Rose-700
        if "hidden_8" in tag: return "#e11d48" # Rose-600
        if "hidden_7" in tag: return "#f43f5e" # Rose-500
        if "hidden_6" in tag: return "#d946ef" # Fuchsia
        if "hidden_5" in tag: return "#8b5cf6" # Purple
        if "hidden_4" in tag: return "#3b82f6" # Blue
        if "hidden_3" in tag: return "#475569"
        if "hidden_2" in tag: return "#64748b"
        if "hidden_1" in tag: return "#94a3b8"
        if "dictionary" in tag: return "#a855f7"
        return "#ffffff"

    # Önce tüm dosyaları oku ve node'ları oluştur
    for filepath in glob.glob(os.path.join(KNOWLEDGE_DIR, "*.md")):
        filename = os.path.basename(filepath).replace(".md", "")
        node_ids.add(filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            frontmatter = parse_frontmatter_block(content)
            
            # Katman tag'ini bul
            tag_match = re.search(r'(layer/[a-zA-Z0-9_]+|dictionary|index)', content)
            layer_tag = tag_match.group(1) if tag_match else "unknown"
            
            color = get_color(layer_tag)
            
            # Grup belirleme (3D force graph için)
            group = 1
            if "input" in layer_tag: group = 1
            elif "output" in layer_tag: group = 12 # 99 yapınca X ekseninde 23500'e uçuyordu
            elif "dictionary" in layer_tag or "index" in layer_tag: group = 0
            else:
                hmatch = re.search(r'hidden_(\d+)', layer_tag)
                if hmatch:
                    group = int(hmatch.group(1)) + 1

            nodes.append({
                "id": filename,
                "name": filename.replace("_", " "),
                "group": group,
                "color": color
            })

            # Direct linkleri bul [[Hedef]]
            link_matches = re.findall(r'\[\[(.*?)\]\]', content)
            for target in link_matches:
                links.append({
                    "source": filename,
                    "target": target,
                    "kind": "direct"
                })

            # RAG linkleri (frontmatter) -> ayrı hat
            rag_targets = parse_frontmatter_list(frontmatter, "rag_links")
            for target in rag_targets:
                links.append({
                    "source": filename,
                    "target": target,
                    "kind": "rag"
                })

    # Hedefi olmayan (henüz oluşturulmamış) linkleri temizle
    valid_links = [link for link in links if link["target"] in node_ids]

    graph_data = {
        "nodes": nodes,
        "links": valid_links
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2)
        
    # Standalone HTML oluştur (İçine JSON verisini gömerek)
    html_template_path = "/Users/fox/Documents/PROJECTS/LokumAI/web_ui/index.html"
    with open(html_template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    data_json_str = json.dumps(graph_data)
    
    # Doğru Javascript bloğunu oluştur
    js_replacement = f"""
        function loadGraph() {{
            const data = {data_json_str};
            document.getElementById('node-count').innerText = data.nodes.length;
            document.getElementById('link-count').innerText = data.links.length;

            if (!Graph) {{
                Graph = ForceGraph3D()(document.getElementById('graph-container'))
                    .graphData(data)
                    .nodeLabel('name')
                    .nodeColor(node => node.color)
                    .nodeRelSize(6)
                    // direct vs rag edge ayrımı
                    .linkColor(link => link.kind === 'rag'
                        ? 'rgba(34, 211, 238, 0.70)'
                        : 'rgba(148, 163, 184, 0.20)'
                    )
                    .linkWidth(link => link.kind === 'rag' ? 2.2 : 0.8)
                    .linkDirectionalParticles(link => link.kind === 'rag' ? 5 : 3)
                    .linkDirectionalParticleWidth(link => link.kind === 'rag' ? 3.4 : 3.0)
                    .linkDirectionalParticleColor(link => link.kind === 'rag' ? '#22d3ee' : '#00ffff') // Cyan (RAG) / Neon
                    .linkDirectionalParticleSpeed(d => 0.008)
                    .d3Force('charge', d3.forceManyBody().strength(-150)) // İtme gücünü artır (yeşiller ile griler girmesin)
                    .d3Force('link', d3.forceLink().distance(80)); // Linkleri uzat
                    
                Graph.d3Force('x', d3.forceX().x(d => (d.group - 5) * 250).strength(3.0)); // X ekseni ayrımı çok daha katı
                Graph.d3Force('y', d3.forceY().y(0).strength(0.2));
                if (d3.forceZ) {{
                    Graph.d3Force('z', d3.forceZ().z(0).strength(0.2));
                }}
            }} else {{
                Graph.graphData(data);
            }}
        }}
    """
    
    # Script bloğundaki eski loadGraph ve fetch kısmını temizle (re.sub kullanma, escape sorunları için regex'i düzeltelim)
    
    # Script bloğundaki loadGraph fonksiyonunu tamamen yenisiyle değiştir
    
    # Tüm function loadGraph() { ... } bloğunu yakalamak için güvenli bir yöntem
    # index.html içinden loadGraph'ı söküp alalım
    parts = html_content.split("function loadGraph() {")
    if len(parts) > 1:
        before_func = parts[0]
        after_func_start = parts[1]
        
        # after_func_start içinde loadGraph'ın bittiği yeri bulalım
        # Basitçe "// İlk yükleme" yorumuna kadar olan kısmı kesebiliriz
        end_parts = after_func_start.split("// İlk yükleme")
        if len(end_parts) > 1:
            after_func = "\n        // İlk yükleme" + end_parts[1]
            html_content = before_func + js_replacement + after_func
            
    # setInterval kısmını (Live Refresh) kaldır (Standalone olduğu için gerek yok)
    html_content = re.sub(r"// Her 5 saniyede bir verileri yenile[\s\S]*?setInterval\(loadGraph, 5000\);", "", html_content)
    
    with open(STANDALONE_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"[*] Graphify verisi üretildi: {len(nodes)} Node, {len(valid_links)} Link")
    print(f"[*] Standalone HTML Oluşturuldu: {STANDALONE_HTML}")

if __name__ == "__main__":
    generate_graph_data()
