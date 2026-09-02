from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.brain_growth.common import KNOWLEDGE_DIR, assert_no_forbidden_nodes, parse_yaml_frontmatter


SECTION_HEADERS = (
    "## Kontrol amacı",
    "## Arbitration sinyalleri",
    "## Karar politikası",
    "## Besleyen H4 düğümleri",
    "## Yönettiği çıktı yolları",
)

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class H5Family:
    filename: str
    title: str
    tags: tuple[str, ...]
    control_purpose: tuple[str, ...]
    h4_inputs: tuple[str, ...]
    control_anchors: tuple[str, ...]
    arbitration_signals: tuple[str, ...]
    decision_policy: tuple[str, ...]
    managed_outputs: tuple[str, ...]


H5_FAMILIES: tuple[H5Family, ...] = (
    H5Family(
        filename="H5_Metacognitive_Policy_Arbitration.md",
        title="Metacognitive Policy Arbitration",
        tags=(
            "#layer/hidden_5_metacognitive_control",
            "#control/policy_arbitration",
            "#domain/multi_domain",
        ),
        control_purpose=(
            "Bu kontrol düğümü, aynı problem anında birden çok hidden_4 politikası yarıştığında hangi karar hattının baskın çıkacağını metadüzeyde seçer.",
            "Amaç, retrieval doğruluğu, execution verimi ve güvenlik ihtiyatı arasında zikzak yapan akışı tek bir üst politika altında stabilize etmektir.",
        ),
        h4_inputs=(
            "H4_Cross_Domain_Causal_Alignment",
            "H4_Cognitive_Retrieval_Policy_Selection",
            "H4_Resource_Execution_Prioritization",
        ),
        control_anchors=(
            "Metacognitive_Reflection_Core",
            "Epistemological_Uncertainty_Calc",
        ),
        arbitration_signals=(
            "Aynı sorgu ya da olay için farklı H4 düğümleri birbirini dışlayan eylem sıraları öneriyorsa",
            "Retrieval derinliği arttıkça karar güveni artmıyor ama kaynak baskısı tırmanıyorsa",
            "Sistem son iki çevrimde farklı H4 kararlarına savrulup downstream kararlarda kararsızlık üretiyorsa",
        ),
        decision_policy=(
            "Belirsizlik yüksek ve risk asimetrikse daha ihtiyatlı H4 hattı varsayılan politika olarak seçilir.",
            "Kaynak baskısı artarken doğruluk kazanımı yatay kalıyorsa daha dar ama kararlı politika üstün gelir.",
            "Seçilen politika iki ardışık çevrim boyunca iyileşme üretmiyorsa arbitration yeniden açılır ve anchor kanıtları daha ağır basar.",
        ),
        managed_outputs=(
            "Attention_Routing_Metacontroller",
            "Strategic_Resource_Allocator",
            "Executive_Action_Formatter",
        ),
    ),
    H5Family(
        filename="H5_Risk_Performance_Tradeoff_Control.md",
        title="Risk Performance Tradeoff Control",
        tags=(
            "#layer/hidden_5_metacognitive_control",
            "#control/risk_performance_tradeoff",
            "#domain/security_execution",
        ),
        control_purpose=(
            "Bu düğüm, performans kazanımı ile güvenlik ve bütünlük riski arasındaki takası yönetir.",
            "Amaç, kısa vadeli throughput iyileştirmelerinin gizli riskleri büyütmesini önleyip sistemin hangi koşulda yavaşlamayı kabul edeceğini açıkça belirlemektir.",
        ),
        h4_inputs=(
            "H4_Performance_Bottleneck_Disambiguation",
            "H4_Security_Failure_Mode_Arbitration",
            "H4_Resource_Execution_Prioritization",
        ),
        control_anchors=(
            "Global_Risk_Assessment",
            "Metacognitive_Reflection_Core",
        ),
        arbitration_signals=(
            "Performans darboğazı çözümü güvenlik telemetrisini körleştirme veya erteleme riski taşıyorsa",
            "Kuyruk baskısını azaltan hamleler bütünlük kanıtı toplama yüzeyini daraltıyorsa",
            "Aynı olayda hem throughput düşüşü hem exploit-benzeri sinyal kuvvetlenmesi görülüyorsa",
        ),
        decision_policy=(
            "Doğrulanmış güvenlik riski varsa performans iyileştirmesi birincil karar yolu olamaz.",
            "Risk sinyali zayıf ama geri dönüş maliyeti yüksekse kademeli optimizasyon uygulanır ve ek gözlem zorunlu tutulur.",
            "Kazanç yalnız dar bir benchmark penceresinde görünüyorsa global risk profili lehine karar verilir.",
        ),
        managed_outputs=(
            "Strategic_Resource_Allocator",
            "Threat_Mitigation_Action",
            "Global_State_Consensus",
        ),
    ),
    H5Family(
        filename="H5_Retrieval_Depth_Governance.md",
        title="Retrieval Depth Governance",
        tags=(
            "#layer/hidden_5_metacognitive_control",
            "#control/retrieval_depth_governance",
            "#domain/cognitive_graph_rag",
        ),
        control_purpose=(
            "Bu düğüm, graph retrieval'ın ne kadar derine, ne kadar genişe ve hangi noktada durdurularak downstream bağlama teslim edileceğini yönetir.",
            "Amaç, recall artışı ile semantic drift, latency ve context packing maliyeti arasındaki çizgiyi operasyonel biçimde sabitlemektir.",
        ),
        h4_inputs=(
            "H4_Cognitive_Retrieval_Policy_Selection",
            "H4_Cross_Domain_Causal_Alignment",
            "H4_Performance_Bottleneck_Disambiguation",
        ),
        control_anchors=(
            "Semantic_Drift_Detector",
            "Hallucination_Detection_Filter",
        ),
        arbitration_signals=(
            "Derin graph traversal daha çok düğüm getiriyor ama cevap güveni belirgin şekilde artmıyorsa",
            "Bağlam paketleme baskısı yüzünden güçlü aday kanıtlar kırpılmaya başlıyorsa",
            "Retrieval genişlemesi farklı domain kümelerini karıştırıp semantik drift sinyali üretiyorsa",
        ),
        decision_policy=(
            "Depth artışı önce kanıt çeşitliliği sonra cevap tutarlılığı üretmiyorsa arama erken kapatılır.",
            "Hallucination riski yükselirse daha sığ ama daha doğrulanabilir altgraf tercih edilir.",
            "Çapraz domain açıklama gerekiyorsa derinlik yalnız cluster geçişleri gerekçelendirilebildiğinde artırılır.",
        ),
        managed_outputs=(
            "Semantic_Graph_Weaver",
            "Cognitive_RAG_Finalizer",
            "Attention_Routing_Metacontroller",
        ),
    ),
    H5Family(
        filename="H5_Global_Escalation_Gate.md",
        title="Global Escalation Gate",
        tags=(
            "#layer/hidden_5_metacognitive_control",
            "#control/global_escalation_gate",
            "#domain/edge_security_operations",
        ),
        control_purpose=(
            "Bu düğüm, lokal toparlama mı, kontrollü izolasyon mu, yoksa sistem çapında escalation mı uygulanacağına karar veren üst kapıdır.",
            "Amaç, yerel semptomların aslında daha geniş bir risk yayılımını işaret edip etmediğini ayırarak aceleci ya da geç escalation kararlarını azaltmaktır.",
        ),
        h4_inputs=(
            "H4_Edge_Device_Response_Strategy",
            "H4_Security_Failure_Mode_Arbitration",
            "H4_Cross_Domain_Causal_Alignment",
        ),
        control_anchors=(
            "Global_Risk_Assessment",
            "Causal_Inference_Engine",
        ),
        arbitration_signals=(
            "Yerel hata paterni başka katmanlarda eşzamanlı yankı üretiyorsa",
            "Cihaz üstü toparlama denemeleri semptomu gizliyor ama kök nedeni daraltmıyorsa",
            "Risk yayılımı kanıtı zayıf olsa bile gecikmiş escalation maliyeti çok yüksek görünüyorsa",
        ),
        decision_policy=(
            "Çapraz katman neden zinciri kurulabiliyorsa escalation eşiği düşürülür.",
            "Lokal yanıt güvenliyse ve global etki kanıtı yoksa sistem çapı alarm yerine kontrollü gözlem sürdürülür.",
            "Yanlış negatif maliyeti yanlış pozitif maliyetinden büyükse gate escalation lehine bias uygular.",
        ),
        managed_outputs=(
            "Auto_Remediation_Script",
            "Threat_Mitigation_Action",
            "Global_State_Consensus",
        ),
    ),
)


def clean_tag(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def family_output_path(family: H5Family, knowledge_dir: Path = KNOWLEDGE_DIR) -> Path:
    return knowledge_dir / family.filename


def verify_existing_targets(targets: tuple[str, ...], knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    missing = [target for target in targets if not (knowledge_dir / f"{target}.md").exists()]
    if missing:
        raise FileNotFoundError(f"Eksik hedef notlar: {', '.join(missing)}")


def render_h5_note(family: H5Family) -> str:
    purpose_text = "\n\n".join(family.control_purpose)
    arbitration_lines = "\n".join(f"- {item}" for item in family.arbitration_signals)
    policy_lines = "\n".join(f"- {item}" for item in family.decision_policy)
    h4_lines = "\n".join(f"- [[{item}]]" for item in family.h4_inputs)
    anchor_lines = "\n".join(f"- [[{item}]]" for item in family.control_anchors)
    output_lines = "\n".join(f"- [[{item}]]" for item in family.managed_outputs)

    text = (
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        + "".join(f'  - "{tag}"\n' for tag in family.tags)
        + "---\n\n"
        f"# {family.title}\n\n"
        "## Kontrol amacı\n\n"
        f"{purpose_text}\n\n"
        "## Arbitration sinyalleri\n\n"
        f"{arbitration_lines}\n\n"
        "## Karar politikası\n\n"
        f"{policy_lines}\n\n"
        "## Besleyen H4 düğümleri\n\n"
        "### Hidden_4 arbitration girdileri\n\n"
        f"{h4_lines}\n\n"
        "### Metacognitive control anchor düğümleri\n\n"
        f"{anchor_lines}\n\n"
        "## Yönettiği çıktı yolları\n\n"
        f"{output_lines}\n"
    )
    assert_no_forbidden_nodes(text)
    return text


def parse_section(text: str, header: str) -> str:
    pattern = re.compile(rf"{re.escape(header)}\n\n(.*?)(?=\n## |\Z)", re.S)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def verify_h5_note(path: Path, family: H5Family) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_yaml_frontmatter(text)
    tags = {clean_tag(tag) for tag in frontmatter.get("tags", []) if str(tag).strip()}
    assert_no_forbidden_nodes(text)

    missing_sections = [header for header in SECTION_HEADERS if header not in text]
    if missing_sections:
        raise ValueError(f"{path.name}: eksik bölümler: {', '.join(missing_sections)}")

    title_line = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), "")
    if title_line != family.title:
        raise ValueError(f"{path.name}: başlık beklenen değerle uyuşmuyor")

    for tag in family.tags:
        if tag not in tags:
            raise ValueError(f"{path.name}: etiket eksik: {tag}")

    source_section = parse_section(text, "## Besleyen H4 düğümleri")
    source_links = WIKILINK_RE.findall(source_section)
    expected_source_links = [*family.h4_inputs, *family.control_anchors]
    if source_links != expected_source_links:
        raise ValueError(f"{path.name}: kaynak bağlantılar beklenen sırayla uyuşmuyor")

    output_section = parse_section(text, "## Yönettiği çıktı yolları")
    output_links = WIKILINK_RE.findall(output_section)
    if tuple(output_links) != family.managed_outputs:
        raise ValueError(f"{path.name}: çıktı yolları beklenen hedeflerle uyuşmuyor")

    return {
        "path": str(path),
        "h4_inputs": len(family.h4_inputs),
        "control_anchors": len(family.control_anchors),
        "managed_outputs": len(family.managed_outputs),
        "forbidden_refs": False,
    }


def print_plan(knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    print(f"Planned hidden_5 note count: {len(H5_FAMILIES)}")
    for family in H5_FAMILIES:
        output = family_output_path(family, knowledge_dir)
        print(
            f"- {output.name}: "
            f"h4_inputs={len(family.h4_inputs)}, "
            f"control_anchors={len(family.control_anchors)}, "
            f"managed_outputs={len(family.managed_outputs)}"
        )


def write_h5_notes(force: bool = False, knowledge_dir: Path = KNOWLEDGE_DIR) -> list[Path]:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for family in H5_FAMILIES:
        verify_existing_targets(family.h4_inputs, knowledge_dir)
        verify_existing_targets(family.control_anchors, knowledge_dir)
        verify_existing_targets(family.managed_outputs, knowledge_dir)
        path = family_output_path(family, knowledge_dir)
        if path.exists() and not force:
            raise FileExistsError(f"{path.name} already exists; pass force=True to overwrite")
        path.write_text(render_h5_note(family), encoding="utf-8")
        written.append(path)
    return sorted(written)


def run_checks(paths: list[Path]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    family_by_filename = {family.filename: family for family in H5_FAMILIES}
    for path in paths:
        family = family_by_filename[path.name]
        results.append(verify_h5_note(path, family))
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate hidden_5 metacognitive control notes.")
    parser.add_argument("--dry-run", action="store_true", help="Plan H5 files without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite existing H5 files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.dry_run:
        print_plan()
        return 0

    written = write_h5_notes(force=args.force)
    results = run_checks(written)

    print("Write completed.")
    for result in results:
        print(
            f"CHECK PASS | {Path(str(result['path'])).name} | "
            f"h4_inputs={result['h4_inputs']} | "
            f"control_anchors={result['control_anchors']} | "
            f"managed_outputs={result['managed_outputs']} | "
            f"forbidden_refs={result['forbidden_refs']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
