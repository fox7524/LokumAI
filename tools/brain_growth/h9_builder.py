from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.brain_growth.common import KNOWLEDGE_DIR, assert_no_forbidden_nodes, parse_yaml_frontmatter


SECTION_HEADERS = (
    "## Paketleme amacı",
    "## Source policy eşlemesi",
    "## Delivery surface sözleşmeleri",
    "## Readiness ve commit koşulları",
    "## Besleyen H8 düğümleri",
    "## Paketlenen çıktı yolları",
)

REQUIRED_TAGS = (
    "#layer/hidden_9_execution_packaging",
    "#execution/package_contract",
    "#execution/delivery_surface",
    "#policy/surface_binding",
)

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class H9Family:
    filename: str
    title: str
    tags: tuple[str, ...]
    package_mode: str
    source_policy: str
    delivery_surfaces: tuple[str, ...]
    package_contracts: tuple[str, ...]
    packaging_purpose: tuple[str, ...]
    h8_inputs: tuple[str, ...]
    source_policy_mapping: tuple[str, ...]
    delivery_contract_strategy: tuple[str, ...]
    readiness_rules: tuple[str, ...]
    downstream_outputs: tuple[str, ...]


H9_FAMILIES: tuple[H9Family, ...] = (
    H9Family(
        filename="H9_Execution_Surface_Binding.md",
        title="Execution Surface Binding",
        tags=(*REQUIRED_TAGS, "#execution/surface_binding"),
        package_mode="surface_bound_policy_delivery",
        source_policy="dominant_policy_surface_binding",
        delivery_surfaces=("Executive_Action_Formatter", "Final_Execution_Gate"),
        package_contracts=("surface_route_manifest", "policy_binding_envelope"),
        packaging_purpose=(
            "Bu düğüm, H8 karar montajında seçilen baskın policy'nin hangi execution yüzeylerine hangi bağlama sözleşmesiyle ineceğini tanımlar.",
            "Amaç, dominant thoughtseed ile gerçek execution yüzeyleri arasında deterministik bir paketleme köprüsü kurmaktır.",
        ),
        h8_inputs=("H8_Dominant_Thoughtseed_Selection",),
        source_policy_mapping=(
            "Dominant thoughtseed çıktısı önce surface-bound bir policy paketi haline getirilir.",
            "Her delivery surface aynı policy çekirdeğini paylaşır, ancak yüzey bazlı bağlama sözleşmesi ayrı korunur.",
        ),
        delivery_contract_strategy=(
            "Executive_Action_Formatter yüzeyi için paket, action formatter tarafından doğrudan okunabilir route manifest içerir.",
            "Final_Execution_Gate yüzeyi için aynı policy, commit öncesi geçit denetimini destekleyen binding envelope ile iletilir.",
        ),
        readiness_rules=(
            "En az bir H8 policy kaynağı ve iki delivery surface birlikte doğrulanmadan paket yayınlanmaz.",
            "Surface-route eşleşmesi eksikse policy öneri olarak kalır, execution paketi olarak işaretlenmez.",
        ),
        downstream_outputs=("Executive_Action_Formatter", "Final_Execution_Gate"),
    ),
    H9Family(
        filename="H9_Response_Payload_Composition.md",
        title="Response Payload Composition",
        tags=(*REQUIRED_TAGS, "#execution/payload_composition"),
        package_mode="broadcast_payload_composition",
        source_policy="global_policy_payload_alignment",
        delivery_surfaces=("Global_State_Consensus", "Executive_Action_Formatter"),
        package_contracts=("payload_shape_contract", "broadcast_delivery_manifest"),
        packaging_purpose=(
            "Bu düğüm, global policy broadcast çıktısını response ve consensus yüzeylerine uygun payload paketlerine dönüştürür.",
            "Amaç, aynı policy'nin farklı teslim yüzeylerinde biçim bozulmadan taşınmasını sağlamaktır.",
        ),
        h8_inputs=("H8_Global_Policy_Broadcast",),
        source_policy_mapping=(
            "H8 broadcast çıktısı, consensus yüzeyi ile formatter yüzeyi için ortak bir payload çekirdeğine bağlanır.",
            "Payload bileşimi policy anlamını korur, fakat teslim yüzeylerinin beklediği alan düzenini ayrı sözleşmelerle sabitler.",
        ),
        delivery_contract_strategy=(
            "Global_State_Consensus yüzeyi policy özetini ve yayın kapsamını taşıyan broadcast manifest alır.",
            "Executive_Action_Formatter yüzeyi aynı policy'yi response üretimine çevirecek payload shape contract ile beslenir.",
        ),
        readiness_rules=(
            "Payload yayınlanmadan önce broadcast hedefleri boş olmamalı ve source policy tekil olmalıdır.",
            "Consensus ve formatter için üretilen paketler aynı policy kimliğine bağlanmıyorsa yayın durdurulur.",
        ),
        downstream_outputs=("Global_State_Consensus", "Executive_Action_Formatter"),
    ),
    H9Family(
        filename="H9_Commit_Ready_Delivery_Check.md",
        title="Commit Ready Delivery Check",
        tags=(*REQUIRED_TAGS, "#execution/commit_readiness"),
        package_mode="commit_ready_gate_delivery",
        source_policy="causal_commitment_delivery_gate",
        delivery_surfaces=("Final_Execution_Gate", "Cognitive_Response_Generator"),
        package_contracts=("commit_readiness_manifest", "causal_release_contract"),
        packaging_purpose=(
            "Bu düğüm, commit eşiğini aşan kararların hangi teslim koşulları sağlandığında execution tarafına açılacağını denetler.",
            "Amaç, causal recall tamamlanmadan erken delivery yapılmasını engelleyen son paketleme kontrolünü sağlamaktır.",
        ),
        h8_inputs=("H8_Decision_Commitment_Gate",),
        source_policy_mapping=(
            "Commitment gate çıktısı önce causal zincir kapanış durumuna göre delivery-ready veya hold-state olarak sınıflandırılır.",
            "Source policy, commit-ready manifest içinde release eşiği ve bekleme gerekçesi ile birlikte paketlenir.",
        ),
        delivery_contract_strategy=(
            "Final_Execution_Gate yüzeyi yalnız causal release contract tamamlandığında yürütülebilir paket alır.",
            "Cognitive_Response_Generator yüzeyi aynı paketin bekleme veya açıklama durumunu response katmanına taşır.",
        ),
        readiness_rules=(
            "En az bir commitment kaynağı ve iki teslim yüzeyi doğrulanmadan commit_ready durumu verilemez.",
            "Partial recall veya eksik causal zincir görüldüğünde paket otomatik olarak hold-state olarak işaretlenir.",
        ),
        downstream_outputs=("Final_Execution_Gate", "Cognitive_Response_Generator"),
    ),
    H9Family(
        filename="H9_Failsafe_Action_Packaging.md",
        title="Failsafe Action Packaging",
        tags=(*REQUIRED_TAGS, "#execution/failsafe_packaging"),
        package_mode="failsafe_override_packaging",
        source_policy="override_failsafe_delivery_alignment",
        delivery_surfaces=("Working_Memory_Flush", "Final_Execution_Gate"),
        package_contracts=("failsafe_action_bundle", "override_release_contract"),
        packaging_purpose=(
            "Bu düğüm, exception override arbitration çıktısını güvenli failsafe action paketlerine dönüştürür.",
            "Amaç, yüksek riskli override kararlarının önce güvenli yüzeylere bağlanıp sonra kontrollü execution kapısına iletilmesidir.",
        ),
        h8_inputs=("H8_Exception_Override_Arbitration",),
        source_policy_mapping=(
            "Override policy önce failsafe ağırlığına göre action bundle içine toplanır, sonra release contract ile çevrelenir.",
            "Source policy sıcak bağlam yerine doğrulanmış exception arbitration sonucuna bağlanır.",
        ),
        delivery_contract_strategy=(
            "Working_Memory_Flush yüzeyi, stabil olmayan sıcak bağlamı temizlemeye yönelik failsafe action bundle alır.",
            "Final_Execution_Gate yüzeyi ise yalnız override release contract doğrulandığında paket kabul eder.",
        ),
        readiness_rules=(
            "Failsafe paketi risk sinyali ve arbitration kaynağı birlikte doğrulanmadıkça yayınlanmaz.",
            "Tek çevrimlik sapmalar override release contract üretmez ve paket yalnız bekleme durumunda kalır.",
        ),
        downstream_outputs=("Working_Memory_Flush", "Long_Term_Strategic_Planner"),
    ),
)


def clean_value(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def clean_list(values: object) -> tuple[str, ...]:
    if not isinstance(values, list):
        return ()
    return tuple(clean_value(value) for value in values if clean_value(value))


def family_output_path(family: H9Family, knowledge_dir: Path = KNOWLEDGE_DIR) -> Path:
    return knowledge_dir / family.filename


def verify_existing_targets(targets: tuple[str, ...], knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    missing = [target for target in targets if not (knowledge_dir / f"{target}.md").exists()]
    if missing:
        raise FileNotFoundError(f"Eksik hedef notlar: {', '.join(missing)}")


def render_h9_note(family: H9Family) -> str:
    purpose_text = "\n\n".join(family.packaging_purpose)
    mapping_lines = "\n".join(f"- {item}" for item in family.source_policy_mapping)
    contract_lines = "\n".join(f"- {item}" for item in family.delivery_contract_strategy)
    readiness_lines = "\n".join(f"- {item}" for item in family.readiness_rules)
    h8_lines = "\n".join(f"- [[{item}]]" for item in family.h8_inputs)
    output_lines = "\n".join(f"- [[{item}]]" for item in family.downstream_outputs)

    text = (
        "---\n"
        'date: "2026-08-30"\n'
        "tags:\n"
        + "".join(f'  - "{tag}"\n' for tag in family.tags)
        + f'package_mode: "{family.package_mode}"\n'
        + f'source_policy: "{family.source_policy}"\n'
        + "delivery_surfaces:\n"
        + "".join(f'  - "{item}"\n' for item in family.delivery_surfaces)
        + "package_contracts:\n"
        + "".join(f'  - "{item}"\n' for item in family.package_contracts)
        + "---\n\n"
        + f"# {family.title}\n\n"
        + "## Paketleme amacı\n\n"
        + f"{purpose_text}\n\n"
        + "## Source policy eşlemesi\n\n"
        + f"{mapping_lines}\n\n"
        + "## Delivery surface sözleşmeleri\n\n"
        + f"{contract_lines}\n\n"
        + "## Readiness ve commit koşulları\n\n"
        + f"{readiness_lines}\n\n"
        + "## Besleyen H8 düğümleri\n\n"
        + f"{h8_lines}\n\n"
        + "## Paketlenen çıktı yolları\n\n"
        + f"{output_lines}\n"
    )
    assert_no_forbidden_nodes(text)
    return text


def parse_section(text: str, header: str) -> str:
    pattern = re.compile(rf"{re.escape(header)}\n\n(.*?)(?=\n## |\Z)", re.S)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def verify_h9_note(path: Path, family: H9Family) -> dict[str, object]:
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

    if clean_value(frontmatter.get("package_mode", "")) != family.package_mode:
        raise ValueError(f"{path.name}: package_mode beklenen değerle uyuşmuyor")

    if clean_value(frontmatter.get("source_policy", "")) != family.source_policy:
        raise ValueError(f"{path.name}: source_policy beklenen değerle uyuşmuyor")

    if clean_list(frontmatter.get("delivery_surfaces", [])) != family.delivery_surfaces:
        raise ValueError(f"{path.name}: delivery_surfaces beklenen sırayla uyuşmuyor")

    if clean_list(frontmatter.get("package_contracts", [])) != family.package_contracts:
        raise ValueError(f"{path.name}: package_contracts beklenen sırayla uyuşmuyor")

    source_section = parse_section(text, "## Besleyen H8 düğümleri")
    source_links = WIKILINK_RE.findall(source_section)
    if tuple(source_links) != family.h8_inputs:
        raise ValueError(f"{path.name}: H8 girdileri beklenen hedeflerle uyuşmuyor")

    output_section = parse_section(text, "## Paketlenen çıktı yolları")
    output_links = WIKILINK_RE.findall(output_section)
    if tuple(output_links) != family.downstream_outputs:
        raise ValueError(f"{path.name}: çıktı yolları beklenen hedeflerle uyuşmuyor")

    return {
        "path": str(path),
        "h8_inputs": len(family.h8_inputs),
        "delivery_surfaces": len(family.delivery_surfaces),
        "package_contracts": len(family.package_contracts),
        "downstream_outputs": len(family.downstream_outputs),
        "forbidden_refs": False,
    }


def print_plan(knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    print(f"Planned hidden_9 note count: {len(H9_FAMILIES)}")
    for family in H9_FAMILIES:
        output = family_output_path(family, knowledge_dir)
        print(
            f"- {output.name}: "
            f"h8_inputs={len(family.h8_inputs)}, "
            f"delivery_surfaces={len(family.delivery_surfaces)}, "
            f"package_contracts={len(family.package_contracts)}, "
            f"downstream_outputs={len(family.downstream_outputs)}"
        )


def write_h9_notes(force: bool = False, knowledge_dir: Path = KNOWLEDGE_DIR) -> list[Path]:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for family in H9_FAMILIES:
        verify_existing_targets(family.h8_inputs, knowledge_dir)
        verify_existing_targets(family.delivery_surfaces, knowledge_dir)
        verify_existing_targets(family.downstream_outputs, knowledge_dir)
        path = family_output_path(family, knowledge_dir)
        if path.exists() and not force:
            raise FileExistsError(f"{path.name} already exists; pass force=True to overwrite")
        path.write_text(render_h9_note(family), encoding="utf-8")
        written.append(path)
    return sorted(written)


def run_checks(paths: list[Path]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    family_by_filename = {family.filename: family for family in H9_FAMILIES}
    for path in paths:
        family = family_by_filename[path.name]
        results.append(verify_h9_note(path, family))
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate hidden_9 execution packaging notes.")
    parser.add_argument("--dry-run", action="store_true", help="Plan H9 files without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite existing H9 files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.dry_run:
        print_plan()
        return 0

    written = write_h9_notes(force=args.force)
    results = run_checks(written)

    print("Write completed.")
    for result in results:
        print(
            f"CHECK PASS | {Path(str(result['path'])).name} | "
            f"h8_inputs={result['h8_inputs']} | "
            f"delivery_surfaces={result['delivery_surfaces']} | "
            f"package_contracts={result['package_contracts']} | "
            f"downstream_outputs={result['downstream_outputs']} | "
            f"forbidden_refs={result['forbidden_refs']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
