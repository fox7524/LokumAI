from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.brain_growth.common import KNOWLEDGE_DIR, assert_no_forbidden_nodes, parse_yaml_frontmatter


SECTION_HEADERS = (
    "## Stratejik denetim amacı",
    "## Governing signal eşlemesi",
    "## Oversight surface sözleşmeleri",
    "## Escalation ve rollback kuralları",
    "## Besleyen H9 düğümleri",
    "## Denetlenen çıktı yolları",
)

REQUIRED_TAGS = (
    "#layer/hidden_10_strategic_supervision",
    "#strategy/supervision_contract",
    "#strategy/oversight_surface",
    "#execution/governance_binding",
)

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class H10Family:
    filename: str
    title: str
    tags: tuple[str, ...]
    supervision_mode: str
    governing_signal: str
    oversight_surfaces: tuple[str, ...]
    supervision_contracts: tuple[str, ...]
    supervision_purpose: tuple[str, ...]
    h9_inputs: tuple[str, ...]
    governing_signal_mapping: tuple[str, ...]
    oversight_contract_strategy: tuple[str, ...]
    escalation_rules: tuple[str, ...]
    downstream_outputs: tuple[str, ...]


H10_FAMILIES: tuple[H10Family, ...] = (
    H10Family(
        filename="H10_Global_Supervision_Arbitration.md",
        title="Global Supervision Arbitration",
        tags=(*REQUIRED_TAGS, "#strategy/global_supervision"),
        supervision_mode="global_supervision_arbitration",
        governing_signal="surface_alignment_supervision",
        oversight_surfaces=("Global_State_Consensus", "Long_Term_Strategic_Planner"),
        supervision_contracts=("supervision_route_manifest", "strategic_alignment_contract"),
        supervision_purpose=(
            "Bu düğüm, H9 execution surface binding ile execution yüzeylerine inen paketleri üst denetim perspektifiyle arbitre eder.",
            "Amaç, yüzey bağlaması tamamlanan paketlerin global consensus ve uzun vadeli strateji ile uyumunu tek bir supervision katmanında sabitlemektir.",
        ),
        h9_inputs=("H9_Execution_Surface_Binding",),
        governing_signal_mapping=(
            "Surface binding çıktısı önce global supervision sinyaline çevrilir ve her yüzeyin aynı stratejik karar çekirdeğine bağlı kalması sağlanır.",
            "Governing signal, execution'a giden bağların yalnız anlık teslim başarısını değil, üst düzey yönetişim tutarlılığını da ölçer.",
        ),
        oversight_contract_strategy=(
            "Global_State_Consensus yüzeyi supervision route manifest ile hangi bağların sistem geneline açıklandığını izler.",
            "Long_Term_Strategic_Planner yüzeyi aynı paketi strategic alignment contract ile uzun erimli hedeflere bağlar.",
        ),
        escalation_rules=(
            "Consensus ile stratejik plan arasında sapma görülürse paket yeni arbitration çevrimine geri alınır.",
            "Execution yüzeyleri aynı governing signal kimliğini taşımıyorsa denetim katmanı release izni vermez.",
        ),
        downstream_outputs=("Global_State_Consensus", "Final_Execution_Gate"),
    ),
    H10Family(
        filename="H10_Long_Horizon_Outcome_Review.md",
        title="Long Horizon Outcome Review",
        tags=(*REQUIRED_TAGS, "#strategy/outcome_review"),
        supervision_mode="long_horizon_outcome_review",
        governing_signal="payload_persistence_review",
        oversight_surfaces=("Long_Term_Strategic_Planner", "Global_State_Consensus"),
        supervision_contracts=("outcome_review_manifest", "payload_persistence_contract"),
        supervision_purpose=(
            "Bu düğüm, H9 response payload composition ile farklı yüzeylere dağıtılan payload'ların uzun vadeli sonuç izini denetler.",
            "Amaç, kısa vadede tutarlı görünen payload bileşiminin uzun erimli hedeflerde anlam kaybı üretmemesini sağlamaktır.",
        ),
        h9_inputs=("H9_Response_Payload_Composition",),
        governing_signal_mapping=(
            "Payload bileşimi önce outcome review manifest içine alınır ve hangi stratejik ufukta değerlendirileceği açıkça işaretlenir.",
            "Governing signal, consensus katmanında görülen response biçiminin uzun vadeli planlayıcıdaki hedeflerle aynı semantiği koruduğunu doğrular.",
        ),
        oversight_contract_strategy=(
            "Long_Term_Strategic_Planner yüzeyi payload persistence contract ile uzun vadeli hedef kaymasını izler.",
            "Global_State_Consensus yüzeyi aynı paketin sistem geneline nasıl yayıldığını outcome review manifest üzerinden denetler.",
        ),
        escalation_rules=(
            "Uzun vadeli hedeflerle uyumsuz payload kalıpları bulunduğunda paket yeniden bileşim için geri çevrilir.",
            "Consensus görünümü ile stratejik review sonucu ayrışırsa outcome review katmanı escalation işaretler.",
        ),
        downstream_outputs=("Long_Term_Strategic_Planner", "Strategic_Resource_Allocator"),
    ),
    H10Family(
        filename="H10_Rollback_Escalation_Governance.md",
        title="Rollback Escalation Governance",
        tags=(*REQUIRED_TAGS, "#strategy/rollback_governance"),
        supervision_mode="rollback_escalation_governance",
        governing_signal="commit_readiness_escalation",
        oversight_surfaces=("Final_Execution_Gate", "Global_Risk_Assessment"),
        supervision_contracts=("rollback_readiness_contract", "escalation_decision_manifest"),
        supervision_purpose=(
            "Bu düğüm, H9 commit ready delivery check ile execution eşiğine gelen paketlerin geri alma ve yükseltme kurallarını stratejik düzeyde yönetir.",
            "Amaç, commit-ready görünen paketlerin risk profili bozulduğunda güvenli rollback ya da escalation yolunu belirlemektir.",
        ),
        h9_inputs=("H9_Commit_Ready_Delivery_Check",),
        governing_signal_mapping=(
            "Commit-ready manifest önce risk ve geri alma seçenekleriyle zenginleştirilir, sonra rollback-readiness contract içine yerleştirilir.",
            "Governing signal, causal zincirin kapanmış olmasını yeterli saymaz; stratejik risk değerlendirmesiyle birlikte okunmasını zorunlu kılar.",
        ),
        oversight_contract_strategy=(
            "Final_Execution_Gate yüzeyi rollback readiness contract ile paketin durdurulabilirliğini izler.",
            "Global_Risk_Assessment yüzeyi escalation decision manifest üzerinden hangi durumda üst seviye müdahale gerektiğini hesaplar.",
        ),
        escalation_rules=(
            "Risk eşiği commit-ready seviyesini aşarsa paket execution kapısından çekilir ve escalation akışına taşınır.",
            "Rollback yolu tanımlı değilse supervision katmanı paketi nihai teslim yerine bekleme kuyruğuna alır.",
        ),
        downstream_outputs=("Global_Risk_Assessment", "Long_Term_Strategic_Planner"),
    ),
    H10Family(
        filename="H10_Strategic_Resource_Oversight.md",
        title="Strategic Resource Oversight",
        tags=(*REQUIRED_TAGS, "#strategy/resource_oversight"),
        supervision_mode="strategic_resource_oversight",
        governing_signal="failsafe_resource_governance",
        oversight_surfaces=("Strategic_Resource_Allocator", "Resource_Lifecycle_Manager"),
        supervision_contracts=("resource_escalation_bundle", "failsafe_capacity_contract"),
        supervision_purpose=(
            "Bu düğüm, H9 failsafe action packaging ile hazırlanan güvenli aksiyon paketlerinin hangi kaynak bütçesiyle yürütüleceğini stratejik düzeyde denetler.",
            "Amaç, failsafe paketlerinin yalnız güvenli değil aynı zamanda kaynak ve yaşam döngüsü açısından sürdürülebilir olmasını sağlamaktır.",
        ),
        h9_inputs=("H9_Failsafe_Action_Packaging",),
        governing_signal_mapping=(
            "Failsafe action bundle önce kaynak baskısı ve yaşam döngüsü etkileriyle birlikte okunur, sonra governing signal içine çevrilir.",
            "Governing signal, emergency override paketlerinin sınırsız kaynak tüketmesini engelleyip kontrollü kapasiteyle ilerlemesini sağlar.",
        ),
        oversight_contract_strategy=(
            "Strategic_Resource_Allocator yüzeyi resource escalation bundle ile hangi kaynakların önceliklendirileceğini belirler.",
            "Resource_Lifecycle_Manager yüzeyi failsafe capacity contract ile geçici override kaynaklarının ne zaman geri çekileceğini denetler.",
        ),
        escalation_rules=(
            "Kaynak bütçesi sürdürülebilir değilse failsafe paketi doğrudan execution'a açılmaz, stratejik yeniden tahsise yönlendirilir.",
            "Aynı paket yaşam döngüsü temizliği olmadan tekrar çalıştırılacaksa supervision katmanı zorunlu rollback ister.",
        ),
        downstream_outputs=("Strategic_Resource_Allocator", "Global_Risk_Assessment"),
    ),
)


def clean_value(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def clean_list(values: object) -> tuple[str, ...]:
    if not isinstance(values, list):
        return ()
    return tuple(clean_value(value) for value in values if clean_value(value))


def family_output_path(family: H10Family, knowledge_dir: Path = KNOWLEDGE_DIR) -> Path:
    return knowledge_dir / family.filename


def verify_existing_targets(targets: tuple[str, ...], knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    missing = [target for target in targets if not (knowledge_dir / f"{target}.md").exists()]
    if missing:
        raise FileNotFoundError(f"Eksik hedef notlar: {', '.join(missing)}")


def render_h10_note(family: H10Family) -> str:
    purpose_text = "\n\n".join(family.supervision_purpose)
    mapping_lines = "\n".join(f"- {item}" for item in family.governing_signal_mapping)
    contract_lines = "\n".join(f"- {item}" for item in family.oversight_contract_strategy)
    escalation_lines = "\n".join(f"- {item}" for item in family.escalation_rules)
    h9_lines = "\n".join(f"- [[{item}]]" for item in family.h9_inputs)
    output_lines = "\n".join(f"- [[{item}]]" for item in family.downstream_outputs)

    text = (
        "---\n"
        'date: "2026-08-30"\n'
        "tags:\n"
        + "".join(f'  - "{tag}"\n' for tag in family.tags)
        + f'supervision_mode: "{family.supervision_mode}"\n'
        + f'governing_signal: "{family.governing_signal}"\n'
        + "oversight_surfaces:\n"
        + "".join(f'  - "{item}"\n' for item in family.oversight_surfaces)
        + "supervision_contracts:\n"
        + "".join(f'  - "{item}"\n' for item in family.supervision_contracts)
        + "---\n\n"
        + f"# {family.title}\n\n"
        + "## Stratejik denetim amacı\n\n"
        + f"{purpose_text}\n\n"
        + "## Governing signal eşlemesi\n\n"
        + f"{mapping_lines}\n\n"
        + "## Oversight surface sözleşmeleri\n\n"
        + f"{contract_lines}\n\n"
        + "## Escalation ve rollback kuralları\n\n"
        + f"{escalation_lines}\n\n"
        + "## Besleyen H9 düğümleri\n\n"
        + f"{h9_lines}\n\n"
        + "## Denetlenen çıktı yolları\n\n"
        + f"{output_lines}\n"
    )
    assert_no_forbidden_nodes(text)
    return text


def parse_section(text: str, header: str) -> str:
    pattern = re.compile(rf"{re.escape(header)}\n\n(.*?)(?=\n## |\Z)", re.S)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def verify_h10_note(path: Path, family: H10Family) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_yaml_frontmatter(text)
    tags = clean_list(frontmatter.get("tags", []))
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

    if clean_value(frontmatter.get("supervision_mode", "")) != family.supervision_mode:
        raise ValueError(f"{path.name}: supervision_mode beklenen değerle uyuşmuyor")

    if clean_value(frontmatter.get("governing_signal", "")) != family.governing_signal:
        raise ValueError(f"{path.name}: governing_signal beklenen değerle uyuşmuyor")

    if clean_list(frontmatter.get("oversight_surfaces", [])) != family.oversight_surfaces:
        raise ValueError(f"{path.name}: oversight_surfaces beklenen sırayla uyuşmuyor")

    if clean_list(frontmatter.get("supervision_contracts", [])) != family.supervision_contracts:
        raise ValueError(f"{path.name}: supervision_contracts beklenen sırayla uyuşmuyor")

    source_section = parse_section(text, "## Besleyen H9 düğümleri")
    source_links = WIKILINK_RE.findall(source_section)
    if tuple(source_links) != family.h9_inputs:
        raise ValueError(f"{path.name}: H9 girdileri beklenen hedeflerle uyuşmuyor")

    output_section = parse_section(text, "## Denetlenen çıktı yolları")
    output_links = WIKILINK_RE.findall(output_section)
    if tuple(output_links) != family.downstream_outputs:
        raise ValueError(f"{path.name}: çıktı yolları beklenen hedeflerle uyuşmuyor")

    return {
        "path": str(path),
        "h9_inputs": len(family.h9_inputs),
        "oversight_surfaces": len(family.oversight_surfaces),
        "supervision_contracts": len(family.supervision_contracts),
        "downstream_outputs": len(family.downstream_outputs),
        "forbidden_refs": False,
    }


def print_plan(knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    print(f"Planned hidden_10 note count: {len(H10_FAMILIES)}")
    for family in H10_FAMILIES:
        output = family_output_path(family, knowledge_dir)
        print(
            f"- {output.name}: "
            f"h9_inputs={len(family.h9_inputs)}, "
            f"oversight_surfaces={len(family.oversight_surfaces)}, "
            f"supervision_contracts={len(family.supervision_contracts)}, "
            f"downstream_outputs={len(family.downstream_outputs)}"
        )


def write_h10_notes(force: bool = False, knowledge_dir: Path = KNOWLEDGE_DIR) -> list[Path]:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for family in H10_FAMILIES:
        verify_existing_targets(family.h9_inputs, knowledge_dir)
        verify_existing_targets(family.oversight_surfaces, knowledge_dir)
        verify_existing_targets(family.downstream_outputs, knowledge_dir)
        path = family_output_path(family, knowledge_dir)
        if path.exists() and not force:
            raise FileExistsError(f"{path.name} already exists; pass force=True to overwrite")
        path.write_text(render_h10_note(family), encoding="utf-8")
        written.append(path)
    return sorted(written)


def run_checks(paths: list[Path]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    family_by_filename = {family.filename: family for family in H10_FAMILIES}
    for path in paths:
        family = family_by_filename[path.name]
        results.append(verify_h10_note(path, family))
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate hidden_10 strategic supervision notes.")
    parser.add_argument("--dry-run", action="store_true", help="Plan H10 files without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite existing H10 files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.dry_run:
        print_plan()
        return 0

    written = write_h10_notes(force=args.force)
    results = run_checks(written)

    print("Write completed.")
    for result in results:
        print(
            f"CHECK PASS | {Path(str(result['path'])).name} | "
            f"h9_inputs={result['h9_inputs']} | "
            f"oversight_surfaces={result['oversight_surfaces']} | "
            f"supervision_contracts={result['supervision_contracts']} | "
            f"downstream_outputs={result['downstream_outputs']} | "
            f"forbidden_refs={result['forbidden_refs']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
