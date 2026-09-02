from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.brain_growth.common import KNOWLEDGE_DIR, assert_no_forbidden_nodes, parse_yaml_frontmatter


SECTION_HEADERS = (
    "## Yakınsama amacı",
    "## Tetikleyiciler",
    "## Karar sınırları",
    "## Besleyen sentez düğümleri",
    "## İleri yönlü etkiler",
)

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class H4Family:
    filename: str
    title: str
    tags: tuple[str, ...]
    convergence_purpose: tuple[str, ...]
    synthesis_inputs: tuple[str, ...]
    strategic_anchors: tuple[str, ...]
    triggers: tuple[str, ...]
    decision_boundaries: tuple[str, ...]
    downstream_links: tuple[str, ...]


H4_FAMILIES: tuple[H4Family, ...] = (
    H4Family(
        filename="H4_Cross_Domain_Causal_Alignment.md",
        title="Cross Domain Causal Alignment",
        tags=(
            "#layer/hidden_4_reasoning_convergence",
            "#reasoning/causal_alignment",
            "#domain/multi_domain",
        ),
        convergence_purpose=(
            "Bu yakınsama düğümü, aynı semptomun Apple Silicon, gömülü zamanlama ve graph retrieval katmanlarında farklı yüzeylerden göründüğü durumlarda ortak nedeni hizalamak için kullanılır.",
            "Amaç, eşzamanlı görünen bozulmalar arasında rastlantısal korelasyon ile gerçek paylaşılan darboğazı ayırıp tek bir açıklama hattı üretmektir.",
        ),
        synthesis_inputs=(
            "H3_Apple_Silicon_Memory_Execution_Synthesis",
            "H3_Embedded_Interrupt_DMA_Synthesis",
            "H3_Cognitive_Graph_RAG_Routing_Synthesis",
        ),
        strategic_anchors=("Causal_Inference_Engine", "Topology_Analysis"),
        triggers=(
            "Aynı anda hem hesaplama gecikmesi hem veri akışı sapması hem de retrieval kararsızlığı görünüyorsa",
            "Birden çok katmanda aday neden sayısı artmış ve gözlenen semptom tek notla açıklanamıyorsa",
            "Cross-stack latency cascade tekil hata yerine ortak neden şüphesi taşıyorsa",
        ),
        decision_boundaries=(
            "Paylaşılan neden hipotezi, bağımsız semptom açıklamalarından daha fazla kanıt taşıdığında tercih edilir.",
            "Topolojik yakınlık var ama zamanlama sırası uyuşmuyorsa korelasyon tek başına yeterli kabul edilmez.",
            "Bir katmandaki lokal optimizasyon diğer katmanlarda iyileşme üretmiyorsa kök neden yeniden açılır.",
        ),
        downstream_links=(
            "Strategic_Resource_Allocator",
            "Attention_Routing_Metacontroller",
            "Metacognitive_Reflection_Core",
        ),
    ),
    H4Family(
        filename="H4_Performance_Bottleneck_Disambiguation.md",
        title="Performance Bottleneck Disambiguation",
        tags=(
            "#layer/hidden_4_reasoning_convergence",
            "#reasoning/performance_disambiguation",
            "#domain/multi_domain",
        ),
        convergence_purpose=(
            "Bu düğüm, performans düşüşünü compute saturation, bellek baskısı, scheduler tıkanması ve retrieval genişleme maliyeti gibi rakip mekanizma aileleri arasında ayrıştırır.",
            "Hedef, semptomu yanlış katmana sabitlemeden önce hangi performans ailesinin baskın olduğunu belirleyip müdahale sırasını netleştirmektir.",
        ),
        synthesis_inputs=(
            "H3_Apple_Silicon_Memory_Execution_Synthesis",
            "H3_Embedded_Interrupt_DMA_Synthesis",
            "H3_Cognitive_Graph_RAG_Routing_Synthesis",
        ),
        strategic_anchors=("DRAM_Bandwidth_Utilization", "Context_Switch_Monitor"),
        triggers=(
            "Throughput düşüyor ama compute, memory ve scheduler sinyalleri birlikte dalgalanıyorsa",
            "Aynı iş yükü farklı donanım veya runtime yüzeylerinde farklı darboğaz imzaları veriyorsa",
            "Graph traversal bütçesi ile execution queue derinliği birbirini maskeleyen gecikmeler üretiyorsa",
        ),
        decision_boundaries=(
            "Bellek geri basıncı görünürse compute optimizasyonu birincil yanıt olarak seçilmez.",
            "Scheduler jitter baskınsa yalnız kernel ya da query plan tuning yeterli kabul edilmez.",
            "Retrieval fan-out, altyapı darboğazını açıklıyorsa önce bütçe daraltılır sonra execution tuning yapılır.",
        ),
        downstream_links=(
            "M5_Pro_Tensor_Dispatch",
            "Strategic_Resource_Allocator",
            "Semantic_Graph_Weaver",
        ),
    ),
    H4Family(
        filename="H4_Security_Failure_Mode_Arbitration.md",
        title="Security Failure Mode Arbitration",
        tags=(
            "#layer/hidden_4_reasoning_convergence",
            "#reasoning/security_arbitration",
            "#domain/security_memory",
        ),
        convergence_purpose=(
            "Bu düğüm, bellek güvenliği, kriptografik hijyen ve cihaz davranışı birlikte bozulduğunda hangi güvenlik failure mode ailesinin baskın olduğunu seçmek için kullanılır.",
            "Amaç, crash, integrity drift ve gizlilik riski sinyallerini tek bir karar sınırında toplayıp yanlış alarm ile gerçek ihlali ayırmaktır.",
        ),
        synthesis_inputs=(
            "H3_Apple_Silicon_Memory_Execution_Synthesis",
            "H3_Embedded_Interrupt_DMA_Synthesis",
            "H3_Cryptographic_Integrity_And_Memory_Safety_Synthesis",
        ),
        strategic_anchors=("Pointer_Authentication_Check", "Cryptographic_Entropy_Analysis"),
        triggers=(
            "Crash telemetrisi ile nonce, key veya witness hijyeni aynı anda bozuluyorsa",
            "Embedded uçta veri bütünlüğü sorunu ile execution anomalisi birlikte görülüyorsa",
            "Exploit olasılığı ile operasyonel gürültü arasındaki sınır belirsizleşmişse",
        ),
        decision_boundaries=(
            "Bütünlük ihlali kanıtı varsa performans gerekçesiyle risk küçültülmez.",
            "Kriptografik yüzey temiz ama pointer ve heap sinyalleri baskınsa karar memory-safety dalına kaydırılır.",
            "Tek bir savunma primitive'i tüm olayı açıklamıyorsa kompozit failure mode kabul edilir.",
        ),
        downstream_links=(
            "Threat_Mitigation_Action",
            "Hardware_Root_Of_Trust",
            "Attention_Routing_Metacontroller",
        ),
    ),
    H4Family(
        filename="H4_Cognitive_Retrieval_Policy_Selection.md",
        title="Cognitive Retrieval Policy Selection",
        tags=(
            "#layer/hidden_4_reasoning_convergence",
            "#reasoning/retrieval_policy_selection",
            "#domain/cognitive_graph_rag",
        ),
        convergence_purpose=(
            "Bu düğüm, hangi retrieval politikasının seçileceğini yalnız graph semantiğine değil, yürütme maliyeti ve güvenlik sınırlarına bakarak belirler.",
            "Amaç, çok-adımlı sorgular için doğru traversal, reranking ve context-packing stratejisini bağlama göre seçmektir.",
        ),
        synthesis_inputs=(
            "H3_Cognitive_Graph_RAG_Routing_Synthesis",
            "H3_Apple_Silicon_Memory_Execution_Synthesis",
            "H3_Cryptographic_Integrity_And_Memory_Safety_Synthesis",
        ),
        strategic_anchors=("Graph_Neural_Network_Embeddings", "Topology_Analysis"),
        triggers=(
            "Multi-hop cevap kalitesi ile latency bütçesi aynı anda baskı altındaysa",
            "Retrieval yolu kaynak limitlerini aşıyor ama bilgi kaybı kabul edilemiyorsa",
            "Context window sıkışması güvenlik veya doğruluk riski doğuruyorsa",
        ),
        decision_boundaries=(
            "Recall artışı doğruluk kazancı üretmiyorsa fan-out artırımı durdurulur.",
            "Güvenlik sınırı daraldığında düşük riskli ama daha pahalı traversal tercih edilebilir.",
            "Traversal seçimi ancak packing ve reranking maliyeti ile birlikte anlamlıdır.",
        ),
        downstream_links=(
            "Semantic_Graph_Weaver",
            "Cognitive_RAG_Finalizer",
            "Attention_Routing_Metacontroller",
        ),
    ),
    H4Family(
        filename="H4_Resource_Execution_Prioritization.md",
        title="Resource Execution Prioritization",
        tags=(
            "#layer/hidden_4_reasoning_convergence",
            "#reasoning/resource_prioritization",
            "#domain/multi_domain",
        ),
        convergence_purpose=(
            "Bu düğüm, eşzamanlı talepler arasında hangi execution hattının önce servis alacağını belirlemek için compute, memory, IO ve güvenlik önceliklerini ortak bütçede toplar.",
            "Amaç, lokal optimizasyonların sistem genelinde kuyruk şişmesi üretmesini önleyip eylem sırasını rasyonelleştirmektir.",
        ),
        synthesis_inputs=(
            "H3_Apple_Silicon_Memory_Execution_Synthesis",
            "H3_Embedded_Interrupt_DMA_Synthesis",
            "H3_Cryptographic_Integrity_And_Memory_Safety_Synthesis",
        ),
        strategic_anchors=("DRAM_Bandwidth_Utilization", "Temporal_Pattern_Recognition"),
        triggers=(
            "Birden çok iş hattı aynı anda kaynak talep edip ortak darboğaz yüzeyi oluşturuyorsa",
            "Latency kritik görevler ile güvenlik kritik görevler aynı scheduling penceresine düşüyorsa",
            "Burst yükleri mevcut sıranın sistemik kuyruk şişmesi ürettiğini gösteriyorsa",
        ),
        decision_boundaries=(
            "Güvenlik kritik yol, eşit maliyetli performans işlerinin arkasına atılmaz.",
            "Kısa vadeli throughput kazancı uzun vadeli queue instability üretirse öncelik yeniden dengelenir.",
            "Periyodik sinyal yoksa kalıcı öncelik değil, olay-temelli escalation uygulanır.",
        ),
        downstream_links=(
            "Strategic_Resource_Allocator",
            "Executive_Action_Formatter",
            "Global_State_Consensus",
        ),
    ),
    H4Family(
        filename="H4_Edge_Device_Response_Strategy.md",
        title="Edge Device Response Strategy",
        tags=(
            "#layer/hidden_4_reasoning_convergence",
            "#reasoning/edge_response_strategy",
            "#domain/edge_systems",
        ),
        convergence_purpose=(
            "Bu düğüm, uç cihazlarda gözlenen semptomlar için yerinde yanıt mı, sınırlı izolasyon mu, yoksa merkezi escalation mı uygulanacağını seçer.",
            "Amaç, gömülü kararsızlık, güvenlik şüphesi ve retrieval ihtiyacını tek bir response stratejisine bağlamaktır.",
        ),
        synthesis_inputs=(
            "H3_Embedded_Interrupt_DMA_Synthesis",
            "H3_Cryptographic_Integrity_And_Memory_Safety_Synthesis",
            "H3_Cognitive_Graph_RAG_Routing_Synthesis",
        ),
        strategic_anchors=("Context_Switch_Monitor", "Causal_Inference_Engine"),
        triggers=(
            "Edge cihaz telemetrisi hata veriyor ve güvenilir yerel teşhis yolu daralıyorsa",
            "Yerel müdahale ile merkezi rehberlik arasında maliyet ve risk dengesi bozuluyorsa",
            "Cihaz semptomu tek başına okunamıyor ve graph destekli ek bağlam gerekiyorsa",
        ),
        decision_boundaries=(
            "Güvenlik ihlali şüphesi varsa sırf uptime için agresif yerel toparlama seçilmez.",
            "Yerel teşhis yeterince belirginse gereksiz merkezileştirme yapılmaz.",
            "Bağlam eksikliği yüksekse otomatik aksiyon yerine kademeli yanıt ve ek veri toplama seçilir.",
        ),
        downstream_links=(
            "Auto_Remediation_Script",
            "Cognitive_Response_Generator",
            "Threat_Mitigation_Action",
        ),
    ),
)


def clean_tag(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def family_output_path(family: H4Family, knowledge_dir: Path = KNOWLEDGE_DIR) -> Path:
    return knowledge_dir / family.filename


def verify_existing_targets(targets: tuple[str, ...], knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    missing = [target for target in targets if not (knowledge_dir / f"{target}.md").exists()]
    if missing:
        raise FileNotFoundError(f"Eksik hedef notlar: {', '.join(missing)}")


def render_h4_note(family: H4Family) -> str:
    purpose_text = "\n\n".join(family.convergence_purpose)
    trigger_lines = "\n".join(f"- {item}" for item in family.triggers)
    boundary_lines = "\n".join(f"- {item}" for item in family.decision_boundaries)
    synthesis_lines = "\n".join(f"- [[{item}]]" for item in family.synthesis_inputs)
    anchor_lines = "\n".join(f"- [[{item}]]" for item in family.strategic_anchors)
    downstream_lines = "\n".join(f"- [[{item}]]" for item in family.downstream_links)

    text = (
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        + "".join(f'  - "{tag}"\n' for tag in family.tags)
        + "---\n\n"
        f"# {family.title}\n\n"
        "## Yakınsama amacı\n\n"
        f"{purpose_text}\n\n"
        "## Tetikleyiciler\n\n"
        f"{trigger_lines}\n\n"
        "## Karar sınırları\n\n"
        f"{boundary_lines}\n\n"
        "## Besleyen sentez düğümleri\n\n"
        "### Hidden_3 sentez girdileri\n\n"
        f"{synthesis_lines}\n\n"
        "### Stratejik anchor düğümler\n\n"
        f"{anchor_lines}\n\n"
        "## İleri yönlü etkiler\n\n"
        f"{downstream_lines}\n"
    )
    assert_no_forbidden_nodes(text)
    return text


def parse_section(text: str, header: str) -> str:
    pattern = re.compile(rf"{re.escape(header)}\n\n(.*?)(?=\n## |\Z)", re.S)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def verify_h4_note(path: Path, family: H4Family) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_yaml_frontmatter(text)
    tags = {clean_tag(tag) for tag in frontmatter.get("tags", []) if str(tag).strip()}
    assert_no_forbidden_nodes(text)

    missing_sections = [header for header in SECTION_HEADERS if header not in text]
    if missing_sections:
        raise ValueError(f"{path.name}: eksik bölümler: {', '.join(missing_sections)}")

    expected_title = family.title
    title_line = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), "")
    if title_line != expected_title:
        raise ValueError(f"{path.name}: başlık beklenen değerle uyuşmuyor")

    for tag in family.tags:
        if tag not in tags:
            raise ValueError(f"{path.name}: etiket eksik: {tag}")

    source_section = parse_section(text, "## Besleyen sentez düğümleri")
    source_links = WIKILINK_RE.findall(source_section)
    expected_source_links = [*family.synthesis_inputs, *family.strategic_anchors]
    if source_links != expected_source_links:
        raise ValueError(f"{path.name}: kaynak bağlantılar beklenen sırayla uyuşmuyor")

    downstream_section = parse_section(text, "## İleri yönlü etkiler")
    downstream_links = WIKILINK_RE.findall(downstream_section)
    if tuple(downstream_links) != family.downstream_links:
        raise ValueError(f"{path.name}: ileri yönlü etkiler beklenen hedeflerle uyuşmuyor")

    return {
        "path": str(path),
        "synthesis_inputs": len(family.synthesis_inputs),
        "anchors": len(family.strategic_anchors),
        "downstream_links": len(family.downstream_links),
        "forbidden_refs": False,
    }


def print_plan(knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    print(f"Planned hidden_4 note count: {len(H4_FAMILIES)}")
    for family in H4_FAMILIES:
        output = family_output_path(family, knowledge_dir)
        print(
            f"- {output.name}: "
            f"synthesis_inputs={len(family.synthesis_inputs)}, "
            f"anchors={len(family.strategic_anchors)}, "
            f"downstream_links={len(family.downstream_links)}"
        )


def write_h4_notes(force: bool = False, knowledge_dir: Path = KNOWLEDGE_DIR) -> list[Path]:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for family in H4_FAMILIES:
        verify_existing_targets(family.synthesis_inputs, knowledge_dir)
        verify_existing_targets(family.strategic_anchors, knowledge_dir)
        verify_existing_targets(family.downstream_links, knowledge_dir)
        path = family_output_path(family, knowledge_dir)
        if path.exists() and not force:
            raise FileExistsError(f"{path.name} already exists; pass force=True to overwrite")
        path.write_text(render_h4_note(family), encoding="utf-8")
        written.append(path)
    return sorted(written)


def run_checks(paths: list[Path]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    family_by_filename = {family.filename: family for family in H4_FAMILIES}
    for path in paths:
        family = family_by_filename[path.name]
        results.append(verify_h4_note(path, family))
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate hidden_4 reasoning/convergence notes.")
    parser.add_argument("--dry-run", action="store_true", help="Plan H4 files without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite existing H4 files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.dry_run:
        print_plan()
        return 0

    written = write_h4_notes(force=args.force)
    results = run_checks(written)

    print("Write completed.")
    for result in results:
        print(
            f"CHECK PASS | {Path(str(result['path'])).name} | "
            f"synthesis_inputs={result['synthesis_inputs']} | "
            f"anchors={result['anchors']} | "
            f"downstream_links={result['downstream_links']} | "
            f"forbidden_refs={result['forbidden_refs']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
