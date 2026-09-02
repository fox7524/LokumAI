from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.brain_growth.common import (
    KNOWLEDGE_DIR,
    assert_no_forbidden_nodes,
    build_note_filename,
    parse_yaml_frontmatter,
)


SECTION_HEADERS = (
    "## Soyutlama",
    "## İnvariantlar",
    "## Retrieval yönlendirme anlamı",
    "## Besleyen düğümler",
    "## İleri besleme",
)

RAW_LINK_RE = re.compile(r"\[\[(RAG_Memory_Cell_(\d+)[^\]]*)\]\]")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class FamilySpec:
    title: str
    domain_tag: str
    raw_indices: tuple[int, ...]
    anchor_inputs: tuple[str, ...]
    forward_links: tuple[str, ...]
    abstraction: tuple[str, ...]
    invariants: tuple[str, ...]
    retrieval_meaning: tuple[str, ...]


FAMILIES: tuple[FamilySpec, ...] = (
    FamilySpec(
        title="Apple Silicon Memory Execution Synthesis",
        domain_tag="#domain/apple_silicon_mlx",
        raw_indices=(13, 14, 15, 16, 17, 18, 19, 20),
        anchor_inputs=("Zero_Copy_Buffer_Analysis", "DRAM_Bandwidth_Utilization"),
        forward_links=("Semantic_Graph_Weaver", "Mixture_Of_Experts_Gate", "Strategic_Resource_Allocator"),
        abstraction=(
            "Bu sentez, Apple Silicon üzerinde hesaplama maliyetinin yalnızca FLOP sayısından değil realization sınırları, unified memory baskısı ve dispatch yüzeyi koordinasyonundan doğduğunu toparlar.",
            "RAG_Memory_Cell_13-20 aralığındaki notlar birlikte okunduğunda MLX/Metal hattında aynı semptomun bazen lazy evaluation barrier'ı, bazen heap alias yaşam döngüsü, bazen de command-buffer paketleme hatası olarak ortaya çıktığı görülür.",
        ),
        invariants=(
            "Gerçek darboğaz çoğu zaman kopyanın kendisi değil, görünür hale gelmemiş senkronizasyon ve resource-hazard sınırıdır.",
            "UMA kapasitesi, locality bozulduğunda teorik ortak bellek avantajını pratikte commit gecikmesine ve cache thrash'e dönüştürebilir.",
            "Execution surface seçimi ancak buffer sahipliği, kernel fusion kırılma noktası ve hızlandırıcı yerleşimi birlikte okunursa anlamlıdır.",
        ),
        retrieval_meaning=(
            "Sorgu performans sapması, beklenmeyen barrier maliyeti veya Apple GPU iş hattında submit/commit dengesizliği anlatıyorsa bu düğüm seçilmelidir.",
            "Bu düğüm, alt düzey bellek/dispatch notlarını tek tek açmadan önce hangi mekanizma ailesine inilmesi gerektiğini belirleyen bir hidden_3 kapısı gibi davranır.",
        ),
    ),
    FamilySpec(
        title="Embedded Interrupt DMA Synthesis",
        domain_tag="#domain/embedded_interrupt_dma",
        raw_indices=(26, 27, 28, 29, 30, 31, 32, 33),
        anchor_inputs=("Context_Switch_Monitor", "Temporal_Pattern_Recognition"),
        forward_links=("Strategic_Resource_Allocator", "Metacognitive_Reflection_Core", "Attention_Routing_Metacontroller"),
        abstraction=(
            "Bu sentez, ESP32/FreeRTOS hattında gerçek zamanlı davranışın tek bir ISR optimizasyonuna değil, kesme tahsisi, cache disable pencereleri, çevrebirim DMA halkaları ve scheduler starvation zincirine bağlı olduğunu sıkıştırır.",
            "RAG_Memory_Cell_26-33 kümesi birlikte ele alındığında interrupt gecikmesi ile veri yolu doyumu aynı sistem davranışının iki yüzü haline gelir.",
        ),
        invariants=(
            "ISR güvenliği, yalnız ISR içeriğiyle değil ISR öncesi bellek yerleşimi ve flash/PSRAM erişim disipliniyle belirlenir.",
            "DMA buffer tasarımı kopuk değil; burst hizası, descriptor ring derinliği ve kullanıcı task tüketim hızı aynı zincirin parçalarıdır.",
            "Çok çekirdekli ya da yüksek çevrebirim yükünde görülen jitter çoğu zaman tek bir bug değil, scheduling ve buffering uyumsuzluğudur.",
        ),
        retrieval_meaning=(
            "Sorgu watchdog reset, underrun, UART kaybı, SPI throughput düşüşü veya yük altında jitter anlatıyorsa bu sentez önce çağrılmalıdır.",
            "Bu düğüm, alt katmandaki gömülü notları hata imzasına göre dallandırmak için yönlendirici bir hidden_3 özet görevi görür.",
        ),
    ),
    FamilySpec(
        title="Cryptographic Integrity and Memory Safety Synthesis",
        domain_tag="#domain/cryptographic_integrity_memory_safety",
        raw_indices=(39, 40, 41, 42, 43, 44, 45, 46),
        anchor_inputs=("Pointer_Authentication_Check", "Cryptographic_Entropy_Analysis"),
        forward_links=("Hardware_Root_Of_Trust", "Attention_Routing_Metacontroller", "Threat_Mitigation_Action"),
        abstraction=(
            "Bu sentez, bellek güvenliği ve kriptografik bütünlük savunmalarını ayrı güvenlik folkloru olarak değil, aynı failure-surface ailesinin tamamlayıcı katmanları olarak birleştirir.",
            "RAG_Memory_Cell_39-46 aralığı birlikte okunduğunda pointer signing, crash clustering, enclave sınırları ve nonce/witness hijyeni aynı kök soruya bağlanır: hangi gizli durum hangi gözlemlenebilir yüzeyden sızıyor?",
        ),
        invariants=(
            "Savunma primitive'leri kapsamı eşit değildir; PAC, CFI, AEAD ve enclave izolasyonu farklı ihlal sınıflarını kapatır.",
            "Bir hata ailesi çoğu zaman hem bütünlük ihlali hem sızıntı sinyali üretir; crash imzası ile gizlilik yüzeyi birlikte okunmalıdır.",
            "Güven zinciri yalnız çekirdek primitive'e değil, onu çevreleyen telemetry, loglama ve anahtar/nonce/witness operasyonlarına bağlıdır.",
        ),
        retrieval_meaning=(
            "Sorgu exploit yüzeyi, crash triage, anahtar sınırı ya da kanıt bütünlüğü tartışıyorsa bu düğüm alt güvenlik notlarına iniş noktası olmalıdır.",
            "Bu düğüm, memory-safety semptomlarını kriptografik risklerle ilişkilendiren bir hidden_3 köprü görevi görür.",
        ),
    ),
    FamilySpec(
        title="Cognitive Graph RAG Routing Synthesis",
        domain_tag="#domain/cognitive_graph_rag_routing",
        raw_indices=(52, 53, 54, 55, 56, 57, 58, 59),
        anchor_inputs=("Graph_Neural_Network_Embeddings", "Topology_Analysis"),
        forward_links=("Semantic_Graph_Weaver", "Cognitive_RAG_Finalizer", "Metacognitive_Reflection_Core"),
        abstraction=(
            "Bu sentez, Graph RAG içinde iyi cevabın yalnız iyi komşu bulmaktan değil, bütçeli genişleme, çok-adımlı sorgu kırılımı, temporal kenarlar ve reranking paketlemesinden doğduğunu toparlar.",
            "RAG_Memory_Cell_52-59 kümesi birlikte okunduğunda traversal, weighting ve context packing tek bir routing ekonomisi olarak görünür.",
        ),
        invariants=(
            "Graph traversal kalitesi, expansion budget olmadan ölçeklenmez; recall artışı kontrolsüz fan-out ile kolayca gürültüye dönüşür.",
            "Entity resolution ve temporal edge disiplini kurulmadan çok-hop reasoning doğru zinciri taşıyamaz.",
            "Traversal sonrası reranking ve subgraph packing, retrieval'in cevap kalitesine dönüşmesinde zorunlu ikinci aşamadır.",
        ),
        retrieval_meaning=(
            "Sorgu multi-hop, beam budget, reranking, graph drift veya context-window sıkışması içeriyorsa bu sentez ilk yönlendirme düğümü olmalıdır.",
            "Bu düğüm, graph_rag alanındaki alt notları hangi traversal ve packing stratejisinin baskın olduğuna göre dallandırır.",
        ),
    ),
)


def extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("Note title not found")


def clean_tag(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def family_output_path(spec: FamilySpec) -> Path:
    return KNOWLEDGE_DIR / build_note_filename("H3", spec.title)


def note_path_for_index(index: int) -> Path:
    matches = sorted(KNOWLEDGE_DIR.glob(f"RAG_Memory_Cell_{index:02d}_*.md"))
    if not matches:
        raise FileNotFoundError(f"RAG_Memory_Cell_{index:02d}_*.md bulunamadı")
    return matches[0]


def verify_existing_targets(targets: tuple[str, ...]) -> None:
    missing = [target for target in targets if not (KNOWLEDGE_DIR / f"{target}.md").exists()]
    if missing:
        raise FileNotFoundError(f"Eksik hedef notlar: {', '.join(missing)}")


def collect_raw_inputs(spec: FamilySpec) -> list[tuple[int, str]]:
    selected: list[tuple[int, str]] = []
    for index in spec.raw_indices:
        path = note_path_for_index(index)
        selected.append((index, path.stem))
    return selected


def build_source_block(raw_inputs: list[tuple[int, str]], anchors: tuple[str, ...]) -> str:
    raw_lines = "\n".join(f"- [[{stem}]]" for _, stem in raw_inputs)
    anchor_lines = "\n".join(f"- [[{anchor}]]" for anchor in anchors)
    return (
        "### RAG_Memory_Cell_13+ girdileri\n\n"
        f"{raw_lines}\n\n"
        "### Mevcut anchor düğümler\n\n"
        f"{anchor_lines}"
    )


def render_note(spec: FamilySpec) -> str:
    raw_inputs = collect_raw_inputs(spec)
    source_block = build_source_block(raw_inputs, spec.anchor_inputs)
    invariant_lines = "\n".join(f"- {line}" for line in spec.invariants)
    retrieval_lines = "\n".join(f"- {line}" for line in spec.retrieval_meaning)
    forward_lines = "\n".join(f"- [[{target}]]" for target in spec.forward_links)
    abstraction_text = "\n\n".join(spec.abstraction)

    text = f"""---
date: 2026-08-30
tags:
  - "#layer/hidden_3_logic_synthesis"
  - "{spec.domain_tag}"
---

# {spec.title}

## Soyutlama

{abstraction_text}

## İnvariantlar

{invariant_lines}

## Retrieval yönlendirme anlamı

{retrieval_lines}

## Besleyen düğümler

{source_block}

## İleri besleme

{forward_lines}
"""
    assert_no_forbidden_nodes(text)
    return text


def parse_section(text: str, header: str) -> str:
    pattern = re.compile(rf"{re.escape(header)}\n\n(.*?)(?=\n## |\Z)", re.S)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def verify_note(path: Path, spec: FamilySpec) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_yaml_frontmatter(text)
    tags = {clean_tag(tag) for tag in frontmatter.get("tags", []) if str(tag).strip()}
    assert_no_forbidden_nodes(text)

    missing_sections = [header for header in SECTION_HEADERS if header not in text]
    if missing_sections:
        raise ValueError(f"{path.name}: eksik bölümler: {', '.join(missing_sections)}")

    if "#layer/hidden_3_logic_synthesis" not in tags:
        raise ValueError(f"{path.name}: hidden_3 etiketi eksik")
    if spec.domain_tag not in tags:
        raise ValueError(f"{path.name}: domain etiketi eksik")

    source_section = parse_section(text, "## Besleyen düğümler")
    source_links = WIKILINK_RE.findall(source_section)
    raw_links = []
    raw_indices = []
    for target, index in RAW_LINK_RE.findall(source_section):
        raw_links.append(target)
        raw_indices.append(int(index))

    if len(raw_links) < 8:
        raise ValueError(f"{path.name}: 8'den az RAG_Memory_Cell girdisi var")
    if any(index < 13 for index in raw_indices):
        raise ValueError(f"{path.name}: 13 altı RAG girdisi kullanılmış")
    if tuple(raw_indices) != spec.raw_indices:
        raise ValueError(f"{path.name}: beklenen RAG giriş aralığı ile uyuşmuyor")

    anchor_count = len(source_links) - len(raw_links)
    if anchor_count != len(spec.anchor_inputs):
        raise ValueError(f"{path.name}: anchor sayısı beklenen değerle uyuşmuyor")

    forward_section = parse_section(text, "## İleri besleme")
    forward_links = WIKILINK_RE.findall(forward_section)
    if tuple(forward_links) != spec.forward_links:
        raise ValueError(f"{path.name}: ileri besleme hedefleri beklenen değerle uyuşmuyor")
    if len(forward_links) > 3:
        raise ValueError(f"{path.name}: ileri besleme sınırı aşıldı")

    return {
        "path": str(path),
        "raw_inputs": len(raw_links),
        "anchors": anchor_count,
        "forward_links": len(forward_links),
        "tags_ok": True,
        "forbidden_refs": False,
    }


def print_plan() -> None:
    print(f"Planned synthesis note count: {len(FAMILIES)}")
    for spec in FAMILIES:
        output = family_output_path(spec)
        print(
            f"- {output.name}: "
            f"{len(spec.raw_indices)} raw input, "
            f"{len(spec.anchor_inputs)} anchor, "
            f"{len(spec.forward_links)} ileri besleme"
        )


def write_notes(force: bool) -> list[Path]:
    written: list[Path] = []
    for spec in FAMILIES:
        verify_existing_targets(spec.anchor_inputs)
        verify_existing_targets(spec.forward_links)
        path = family_output_path(spec)
        if path.exists() and not force:
            raise FileExistsError(f"Refusing to overwrite existing synthesis file: {path.name}")
        path.write_text(render_note(spec), encoding="utf-8")
        written.append(path)
    return written


def run_checks(paths: list[Path]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for spec, path in zip(FAMILIES, paths, strict=True):
        results.append(verify_note(path, spec))
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Phase 2 hidden_3 synthesis notes.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Plan synthesis files without writing")
    mode.add_argument("--write", action="store_true", help="Write synthesis markdown files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing H3 files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.dry_run:
        print_plan()
        return 0

    written = write_notes(force=args.force)
    results = run_checks(written)

    print("Write completed.")
    for result in results:
        print(
            f"CHECK PASS | {Path(str(result['path'])).name} | "
            f"raw_inputs={result['raw_inputs']} | "
            f"anchors={result['anchors']} | "
            f"forward_links={result['forward_links']} | "
            f"forbidden_refs={result['forbidden_refs']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
