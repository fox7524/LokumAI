import os
import glob
import re
import random

KNOWLEDGE_DIR = "/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge"

def get_layer_idx(tag):
    if "input" in tag: return 0
    if "output" in tag: return 99 # Max layer
    match = re.search(r'hidden_(\d+)', tag)
    if match:
        return int(match.group(1))
    return -1

# 1. Tüm düğümleri ve katmanlarını haritala
files = glob.glob(os.path.join(KNOWLEDGE_DIR, "*.md"))
nodes_by_layer = {}
node_to_layer = {}

for filepath in files:
    name = os.path.basename(filepath).replace(".md", "")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        tag_match = re.search(r'(layer/[a-zA-Z0-9_]+)', content)
        if tag_match:
            tag = tag_match.group(1)
            idx = get_layer_idx(tag)
            if idx != -1:
                if idx not in nodes_by_layer:
                    nodes_by_layer[idx] = []
                nodes_by_layer[idx].append(name)
                node_to_layer[name] = idx

# Output katmanını dinamik olarak en yüksek katmanın bir fazlası yapalım (Eğer 10 varsa Output 11 olur)
max_hidden = max([k for k in nodes_by_layer.keys() if k != 99 and k != 0] + [0])
output_idx = max_hidden + 1

if 99 in nodes_by_layer:
    nodes_by_layer[output_idx] = nodes_by_layer.pop(99)
    for node in nodes_by_layer[output_idx]:
        node_to_layer[node] = output_idx

print(f"[*] Topoloji Tarama: Max Hidden Layer: {max_hidden}, Output Layer: {output_idx}")

fixed_count = 0
links_removed = 0
links_added = 0

# 2. Kaçak sinapsları temizle ve düzelt
for filepath in files:
    name = os.path.basename(filepath).replace(".md", "")
    if name not in node_to_layer:
        continue
        
    current_idx = node_to_layer[name]
    if current_idx == output_idx: 
        continue # Output'tan ileriye link gitmez
        
    target_idx = current_idx + 1
    # Eğer hedef katmanda düğüm yoksa, bir sonraki dolu katmana atla (Güvenlik)
    while target_idx not in nodes_by_layer and target_idx <= output_idx:
        target_idx += 1
        
    possible_targets = nodes_by_layer.get(target_idx, [])
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    links = re.findall(r'\[\[(.*?)\]\]', content)
    new_content = content
    needs_update = False
    valid_links_kept = 0
    
    for link in links:
        if link in node_to_layer:
            link_idx = node_to_layer[link]
            if link_idx != target_idx:
                new_content = new_content.replace(f"- [[{link}]]\n", "")
                new_content = new_content.replace(f"[[{link}]]", "")
                needs_update = True
                links_removed += 1
            else:
                valid_links_kept += 1
        else:
            new_content = new_content.replace(f"- [[{link}]]\n", "")
            new_content = new_content.replace(f"[[{link}]]", "")
            needs_update = True
            links_removed += 1
            
    if valid_links_kept == 0 and possible_targets:
        needs_update = True
        num_links = random.randint(2, 5)
        targets = random.sample(possible_targets, min(len(possible_targets), num_links))
        addition = ""
        for t in targets:
            addition += f"- [[{t}]]\n"
            links_added += 1
        new_content += "\n" + addition
        
    new_content = re.sub(r'\n\s*-\s*\n', '\n', new_content)
    if current_idx != (output_idx - 1): 
        new_content = re.sub(r'- \(Output Terminal\)', '', new_content)
        
    if needs_update:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed_count += 1
        
print(f"[*] Topoloji Fix Tamamlandı! {fixed_count} düğüm onarıldı.")
print(f"[*] {links_removed} kaçak sinaps (layer-skip) SİLİNDİ.")
print(f"[*] {links_added} yeni, kurallı sinaps (strict feed-forward) EKLENDİ.")