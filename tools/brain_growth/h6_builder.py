from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.brain_growth.common import KNOWLEDGE_DIR, assert_no_forbidden_nodes, parse_yaml_frontmatter


SECTION_HEADERS = (
    "## Orkestrasyon amacı",
    "## Yürütücü sinyaller",
    "## Orkestrasyon politikası",
    "## Besleyen H5 düğümleri",
    "## Koordine ettiği çıktı yolları",
)

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class H6Family:
    filename: str
    title: str
    tags: tuple[str, ...]
    orchestration_purpose: tuple[str, ...]
    h5_inputs: tuple[str, ...]
    orchestration_anchors: tuple[str, ...]
    executive_signals: tuple[str, ...]
    orchestration_policy: tuple[str, ...]
    coordinated_outputs: tuple[str, ...]


H6_FAMILIES: tuple[H6Family, ...] = (
    H6Family(
        filename="H6_Executive_Priority_Orchestration.md",
        title="Executive Priority Orchestration",
        tags=(
            "#layer/hidden_6_executive_orchestration",
            "#executive/priority_orchestration",
            "#domain/multi_domain",
        ),
        orchestration_purpose=(
            "Bu yürütücü orkestrasyon düğümü, birden çok H5 kontrol kararı aynı anda stratejik planlama ve çıktı montajı üzerinde baskı kurduğunda hangi iş akışının öne alınacağını belirler.",
            "Amaç, metacognitive arbitration sonuçlarını yürütme kuyruğuna düzenli biçimde aktararak stratejik öncelik, eylem formatlama ve global durum senkronunu aynı çatı altında hizalamaktır.",
        ),
        h5_inputs=(
            "H5_Metacognitive_Policy_Arbitration",
            "H5_Risk_Performance_Tradeoff_Control",
        ),
        orchestration_anchors=(
            "Attention_Routing_Metacontroller",
            "Strategic_Resource_Allocator",
        ),
        executive_signals=(
            "Bir H5 kararı kaynak daraltma isterken başka bir H5 kararı yanıt genişliği veya güvenlik teyidi talep ediyorsa",
            "Çıktı paketleme sırası değiştikçe sistemin global durumu ve kullanıcıya gösterilecek nihai eylem zinciri senkron kalmıyorsa",
            "Önceliklendirme kararları iki çevrim üst üste farklı assembly yollarına savruluyorsa",
        ),
        orchestration_policy=(
            "Güvenlik ve bütünlük etkisi taşıyan iş akışları, eşit fayda durumunda performans odaklı akışların önüne alınır.",
            "Kaynak tahsisi ile çıktı formatlaması arasında uyumsuzluk varsa önce stratejik plan sabitlenir, sonra assembly yolları kilitlenir.",
            "Global durum senkronu bozulmadan aynı anda en fazla bir yüksek etkili öncelik değişimi uygulanır.",
        ),
        coordinated_outputs=(
            "Long_Term_Strategic_Planner",
            "Executive_Action_Formatter",
            "Global_State_Consensus",
        ),
    ),
    H6Family(
        filename="H6_Retrieval_Action_Coordination.md",
        title="Retrieval Action Coordination",
        tags=(
            "#layer/hidden_6_executive_orchestration",
            "#executive/retrieval_action_coordination",
            "#domain/cognitive_graph_rag",
        ),
        orchestration_purpose=(
            "Bu düğüm, retrieval derinliği ve politika seçimi ile üretilen kararların hangi eylem çıktısına ne zaman dönüştürüleceğini orkestre eder.",
            "Amaç, semantic graph toplama maliyetini gerçek yanıt montajı ile dengeleyip gereksiz veri genişlemesini nihai execution yoluna taşımamaktır.",
        ),
        h5_inputs=(
            "H5_Retrieval_Depth_Governance",
            "H5_Metacognitive_Policy_Arbitration",
        ),
        orchestration_anchors=(
            "Semantic_Graph_Weaver",
            "Cognitive_RAG_Finalizer",
        ),
        executive_signals=(
            "Retrieval tarafı daha fazla kanıt isterken yanıt montajı karar eşiğine ulaşmış görünüyorsa",
            "Yeni kanıtlar planı anlamlı biçimde değiştirmiyor ama execution paketleme maliyeti artıyorsa",
            "Graph tabanlı bağlam ile kullanıcıya verilecek yanıt formatı arasında gecikme ve tutarlılık baskısı oluşuyorsa",
        ),
        orchestration_policy=(
            "Cevap kararlılığı korunuyorsa yeni retrieval dalı açmak yerine mevcut kanıtların execution paketlemesi tercih edilir.",
            "Semantic drift sinyali yükselirse finalizer yalnız doğrulanmış altgrafı downstream aksiyona taşır.",
            "Nihai eylem kapısı yalnız retrieval genişlemesinin marjinal katkısı düştüğünde açılır.",
        ),
        coordinated_outputs=(
            "Executive_Action_Formatter",
            "Cognitive_Response_Generator",
            "Final_Execution_Gate",
        ),
    ),
    H6Family(
        filename="H6_Global_Response_Orchestration.md",
        title="Global Response Orchestration",
        tags=(
            "#layer/hidden_6_executive_orchestration",
            "#executive/global_response_orchestration",
            "#domain/edge_security_operations",
        ),
        orchestration_purpose=(
            "Bu yürütücü düğüm, escalation, mitigation ve consensus kararlarını tek bir global response akışında birleştirir.",
            "Amaç, yerel ve sistem çapı yanıtlar arasında çakışan komut üretimini engelleyip hangi response ailesinin stratejik plana bağlanacağını merkezi olarak belirlemektir.",
        ),
        h5_inputs=(
            "H5_Global_Escalation_Gate",
            "H5_Risk_Performance_Tradeoff_Control",
        ),
        orchestration_anchors=(
            "Threat_Mitigation_Action",
            "Global_State_Consensus",
        ),
        executive_signals=(
            "Mitigation yolu hızlı aksiyon isterken escalation kapısı daha geniş koordinasyon çağırıyorsa",
            "Global consensus henüz sabitlenmeden birden çok response dalı aynı anda komut üretmeye başlıyorsa",
            "Lokal toparlama ile sistem çapı savunma adımları aynı kaynak bütçesini tüketiyorsa",
        ),
        orchestration_policy=(
            "Consensus oluşmadan geri dönüşü zor response dalları nihai yürütmeye açılmaz.",
            "Escalation maliyeti yüksek olsa bile yayılım riski baskınsa response planı merkezi akış lehine genişletilir.",
            "Aynı olay için birincil mitigation hattı seçildikten sonra ikincil aksiyonlar yalnız destekleyici rol üstlenir.",
        ),
        coordinated_outputs=(
            "Long_Term_Strategic_Planner",
            "Resource_Lifecycle_Manager",
            "Final_Execution_Gate",
        ),
    ),
    H6Family(
        filename="H6_Recovery_Execution_Sequencing.md",
        title="Recovery Execution Sequencing",
        tags=(
            "#layer/hidden_6_executive_orchestration",
            "#executive/recovery_execution_sequencing",
            "#domain/resilience_operations",
        ),
        orchestration_purpose=(
            "Bu düğüm, remediation ve yanıt adımlarının hangi sırayla güvenli biçimde yürütüleceğini belirleyen executive sequencing katmanıdır.",
            "Amaç, H5 kontrol kararlarını toparlama, kullanıcıya görünür yanıt ve son execution gate arasında deterministik bir zincire dönüştürmektir.",
        ),
        h5_inputs=(
            "H5_Global_Escalation_Gate",
            "H5_Metacognitive_Policy_Arbitration",
            "H5_Risk_Performance_Tradeoff_Control",
        ),
        orchestration_anchors=(
            "Auto_Remediation_Script",
            "Executive_Action_Formatter",
        ),
        executive_signals=(
            "Otomatik remediation hazır olsa da yürütme sırası henüz kullanıcıya açıklanabilir hale gelmemişse",
            "Risk azaltma adımı ile kullanıcıya sunulacak response arasında tutarlılık boşluğu oluşuyorsa",
            "Aynı toparlama akışında erken execution, geri alma maliyetini anlamlı biçimde yükseltiyorsa",
        ),
        orchestration_policy=(
            "Geri alınamaz komutlar, remediation doğrulaması ve kullanıcıya dönük eylem açıklaması tamamlanmadan açılmaz.",
            "Yanıt sıralaması önce sistemi güvene alır, sonra görünür response ve en sonda kalıcı execution kapısını tetikler.",
            "Sequencing kararı yalnız tekil komut başarısına değil bütün toparlama zincirinin okunabilirliğine göre verilir.",
        ),
        coordinated_outputs=(
            "Resource_Lifecycle_Manager",
            "Cognitive_Response_Generator",
            "Final_Execution_Gate",
        ),
    ),
)


def clean_tag(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def family_output_path(family: H6Family, knowledge_dir: Path = KNOWLEDGE_DIR) -> Path:
    return knowledge_dir / family.filename


def verify_existing_targets(targets: tuple[str, ...], knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    missing = [target for target in targets if not (knowledge_dir / f"{target}.md").exists()]
    if missing:
        raise FileNotFoundError(f"Eksik hedef notlar: {', '.join(missing)}")


def render_h6_note(family: H6Family) -> str:
    purpose_text = "\n\n".join(family.orchestration_purpose)
    signal_lines = "\n".join(f"- {item}" for item in family.executive_signals)
    policy_lines = "\n".join(f"- {item}" for item in family.orchestration_policy)
    h5_lines = "\n".join(f"- [[{item}]]" for item in family.h5_inputs)
    anchor_lines = "\n".join(f"- [[{item}]]" for item in family.orchestration_anchors)
    output_lines = "\n".join(f"- [[{item}]]" for item in family.coordinated_outputs)

    text = (
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        + "".join(f'  - "{tag}"\n' for tag in family.tags)
        + "---\n\n"
        f"# {family.title}\n\n"
        "## Orkestrasyon amacı\n\n"
        f"{purpose_text}\n\n"
        "## Yürütücü sinyaller\n\n"
        f"{signal_lines}\n\n"
        "## Orkestrasyon politikası\n\n"
        f"{policy_lines}\n\n"
        "## Besleyen H5 düğümleri\n\n"
        "### Hidden_5 executive girdileri\n\n"
        f"{h5_lines}\n\n"
        "### Executive orchestration anchor düğümleri\n\n"
        f"{anchor_lines}\n\n"
        "## Koordine ettiği çıktı yolları\n\n"
        f"{output_lines}\n"
    )
    assert_no_forbidden_nodes(text)
    return text


def parse_section(text: str, header: str) -> str:
    pattern = re.compile(rf"{re.escape(header)}\n\n(.*?)(?=\n## |\Z)", re.S)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def verify_h6_note(path: Path, family: H6Family) -> dict[str, object]:
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

    source_section = parse_section(text, "## Besleyen H5 düğümleri")
    source_links = WIKILINK_RE.findall(source_section)
    expected_source_links = [*family.h5_inputs, *family.orchestration_anchors]
    if source_links != expected_source_links:
        raise ValueError(f"{path.name}: kaynak bağlantılar beklenen sırayla uyuşmuyor")

    output_section = parse_section(text, "## Koordine ettiği çıktı yolları")
    output_links = WIKILINK_RE.findall(output_section)
    if tuple(output_links) != family.coordinated_outputs:
        raise ValueError(f"{path.name}: çıktı yolları beklenen hedeflerle uyuşmuyor")

    return {
        "path": str(path),
        "h5_inputs": len(family.h5_inputs),
        "anchors": len(family.orchestration_anchors),
        "coordinated_outputs": len(family.coordinated_outputs),
        "forbidden_refs": False,
    }


def print_plan(knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    print(f"Planned hidden_6 note count: {len(H6_FAMILIES)}")
    for family in H6_FAMILIES:
        output = family_output_path(family, knowledge_dir)
        print(
            f"- {output.name}: "
            f"h5_inputs={len(family.h5_inputs)}, "
            f"anchors={len(family.orchestration_anchors)}, "
            f"coordinated_outputs={len(family.coordinated_outputs)}"
        )


def write_h6_notes(force: bool = False, knowledge_dir: Path = KNOWLEDGE_DIR) -> list[Path]:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for family in H6_FAMILIES:
        verify_existing_targets(family.h5_inputs, knowledge_dir)
        verify_existing_targets(family.orchestration_anchors, knowledge_dir)
        verify_existing_targets(family.coordinated_outputs, knowledge_dir)
        path = family_output_path(family, knowledge_dir)
        if path.exists() and not force:
            raise FileExistsError(f"{path.name} already exists; pass force=True to overwrite")
        path.write_text(render_h6_note(family), encoding="utf-8")
        written.append(path)
    return sorted(written)


def run_checks(paths: list[Path]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    family_by_filename = {family.filename: family for family in H6_FAMILIES}
    for path in paths:
        family = family_by_filename[path.name]
        results.append(verify_h6_note(path, family))
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate hidden_6 executive orchestration notes.")
    parser.add_argument("--dry-run", action="store_true", help="Plan H6 files without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite existing H6 files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.dry_run:
        print_plan()
        return 0

    written = write_h6_notes(force=args.force)
    results = run_checks(written)

    print("Write completed.")
    for result in results:
        print(
            f"CHECK PASS | {Path(str(result['path'])).name} | "
            f"h5_inputs={result['h5_inputs']} | "
            f"anchors={result['anchors']} | "
            f"coordinated_outputs={result['coordinated_outputs']} | "
            f"forbidden_refs={result['forbidden_refs']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
