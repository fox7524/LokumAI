from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.brain_growth.common import KNOWLEDGE_DIR, assert_no_forbidden_nodes, parse_yaml_frontmatter


SECTION_HEADERS = (
    "## Yansıma amacı",
    "## Audit signal eşlemesi",
    "## Evidence surface sözleşmeleri",
    "## İspat ve tutarlılık kuralları",
    "## Besleyen H10 düğümleri",
    "## Üretilen audit çıktıları",
)

REQUIRED_TAGS = (
    "#layer/hidden_11_reflection_audit",
    "#audit/trace_contract",
    "#audit/evidence_surface",
    "#audit/provenance_binding",
)

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class H11Family:
    filename: str
    title: str
    tags: tuple[str, ...]
    reflection_mode: str
    audit_signal: str
    audit_surfaces: tuple[str, ...]
    audit_contracts: tuple[str, ...]
    reflection_purpose: tuple[str, ...]
    h10_inputs: tuple[str, ...]
    audit_signal_mapping: tuple[str, ...]
    evidence_contract_strategy: tuple[str, ...]
    proof_rules: tuple[str, ...]
    downstream_outputs: tuple[str, ...]


H11_FAMILIES: tuple[H11Family, ...] = (
    H11Family(
        filename="H11_Trace_Provenance_Attestation.md",
        title="Trace Provenance Attestation",
        tags=(*REQUIRED_TAGS, "#audit/provenance_attestation"),
        reflection_mode="trace_provenance_attestation",
        audit_signal="supervision_trace_digest",
        audit_surfaces=("Metacognitive_Reflection_Core", "Global_State_Consensus"),
        audit_contracts=("provenance_trace_manifest", "surface_route_attestation"),
        reflection_purpose=(
            "Bu düğüm, H10 supervision çıktılarının hangi kanıtlara dayanarak üretildiğini deterministik bir provenance iziyle sabitler.",
            "Amaç, 'neden bu bağ yayınlandı?' sorusunu runtime sonrasında tekrar üretilebilir bir trace sözleşmesine bağlamaktır.",
        ),
        h10_inputs=("H10_Global_Supervision_Arbitration",),
        audit_signal_mapping=(
            "Global supervision route manifest içindeki yüzey eşleşmeleri, audit_signal içine hashlenmiş bir trace digest olarak çevrilir.",
            "Audit_signal, karar çekirdeğini değil; kararın hangi yol ve hangi sözleşmelerle aktarıldığını ispatlar.",
        ),
        evidence_contract_strategy=(
            "Metacognitive_Reflection_Core yüzeyi provenance_trace_manifest ile kanıt zincirini saklayabilir biçimde alır.",
            "Global_State_Consensus yüzeyi surface_route_attestation ile yayınlanan bağların tutarlılık ispatını alır.",
        ),
        proof_rules=(
            "Bir execution paketi audit izine alınmadan önce en az bir H10 girdisi ve iki audit surface doğrulanmalıdır.",
            "Tutarsız route veya eksik sözleşme görüldüğünde attestation üretilmez; exception olarak işaretlenir.",
        ),
        downstream_outputs=("Cognitive_Dissonance_Resolver", "Hallucination_Detection_Filter", "Global_Risk_Assessment"),
    ),
    H11Family(
        filename="H11_Outcome_Regression_Postmortem.md",
        title="Outcome Regression Postmortem",
        tags=(*REQUIRED_TAGS, "#audit/outcome_postmortem"),
        reflection_mode="outcome_regression_postmortem",
        audit_signal="long_horizon_regression_signal",
        audit_surfaces=("Long_Term_Strategic_Planner", "Global_Risk_Assessment"),
        audit_contracts=("outcome_regression_report", "payload_drift_proof"),
        reflection_purpose=(
            "Bu düğüm, H10 outcome review sonucunda ortaya çıkan hedef kaymalarını postmortem biçimde sınıflandırır ve regresyon sinyali üretir.",
            "Amaç, payload tutarlılığı bozulduysa bunun nedenini ve geri kazanım yolunu audit düzeyinde görünür kılmaktır.",
        ),
        h10_inputs=("H10_Long_Horizon_Outcome_Review",),
        audit_signal_mapping=(
            "Outcome review manifest içindeki ufuk (horizon) sınıfları, regresyon sinyalinin zaman ölçeğini belirler.",
            "Payload persistence contract sapmaları, payload_drift_proof içinde kanıt bloklarına dönüştürülür.",
        ),
        evidence_contract_strategy=(
            "Long_Term_Strategic_Planner yüzeyi outcome_regression_report ile hedef kaymasını dönemsel olarak takip eder.",
            "Global_Risk_Assessment yüzeyi payload_drift_proof ile risk artışını kanıt bağlarıyla birlikte okur.",
        ),
        proof_rules=(
            "Regresyon sinyali üretmek için en az iki ayrı ufukta (kısa/uzun) sapma kanıtı aranır.",
            "Tek çevrimlik dalgalanmalar postmortem raporu üretebilir ama 'regression' sınıfına terfi edemez.",
        ),
        downstream_outputs=("Auto_Remediation_Script", "Alert_Notification_Broadcaster", "Metacognitive_Reflection_Core"),
    ),
    H11Family(
        filename="H11_Rollback_Decision_Audit.md",
        title="Rollback Decision Audit",
        tags=(*REQUIRED_TAGS, "#audit/rollback_audit"),
        reflection_mode="rollback_decision_audit",
        audit_signal="rollback_escalation_attestation",
        audit_surfaces=("Final_Execution_Gate", "Global_Risk_Assessment"),
        audit_contracts=("rollback_decision_log", "escalation_provenance_bundle"),
        reflection_purpose=(
            "Bu düğüm, H10 rollback/escalation governance kararlarını hangi risk ve hangi geri alma sözleşmesiyle verdiğini audit log'a bağlar.",
            "Amaç, 'neden rollback oldu / neden escalation oldu?' sorusunu kanıtlanabilir bir karar günlüğüne dönüştürmektir.",
        ),
        h10_inputs=("H10_Rollback_Escalation_Governance",),
        audit_signal_mapping=(
            "Rollback readiness contract içindeki seçenekler, rollback_decision_log içinde karar ağacı olarak kaydedilir.",
            "Escalation decision manifest, escalation_provenance_bundle içinde risk kanıtlarıyla bağlanır.",
        ),
        evidence_contract_strategy=(
            "Final_Execution_Gate yüzeyi rollback_decision_log ile hangi paketin neden tutulduğunu izler.",
            "Global_Risk_Assessment yüzeyi escalation_provenance_bundle ile üst seviye müdahale gerekçesini doğrular.",
        ),
        proof_rules=(
            "Rollback kararı yazılmadan önce en az bir risk sinyali ve bir causal readiness kanıtı birlikte bulunmalıdır.",
            "Rollback yolu tanımsızsa audit kaydı 'incomplete' olarak işaretlenir ve delivery engellenir.",
        ),
        downstream_outputs=("Process_Kill_Signal", "Power_State_Adjustment", "Kernel_Panic_Trigger"),
    ),
    H11Family(
        filename="H11_Failsafe_Cost_Accounting.md",
        title="Failsafe Cost Accounting",
        tags=(*REQUIRED_TAGS, "#audit/resource_accounting"),
        reflection_mode="failsafe_cost_accounting",
        audit_signal="failsafe_cost_ledger_signal",
        audit_surfaces=("Strategic_Resource_Allocator", "Resource_Lifecycle_Manager"),
        audit_contracts=("resource_cost_ledger", "lifecycle_cleanup_receipt"),
        reflection_purpose=(
            "Bu düğüm, failsafe paketlerinin kaynak tüketimini ve yaşam döngüsü temizliğini audit düzeyinde muhasebeleştirir.",
            "Amaç, güvenli görünen failsafe akışlarının bile kaynak ve geri çekilme maliyetini deterministik biçimde görünür kılmaktır.",
        ),
        h10_inputs=("H10_Strategic_Resource_Oversight",),
        audit_signal_mapping=(
            "Resource escalation bundle içindeki kaynak kararları, resource_cost_ledger içinde maliyet satırlarına çevrilir.",
            "Failsafe capacity contract, lifecycle_cleanup_receipt içinde geri çekilme ve temizleme ispatına bağlanır.",
        ),
        evidence_contract_strategy=(
            "Strategic_Resource_Allocator yüzeyi resource_cost_ledger ile kapasite tüketimini izler.",
            "Resource_Lifecycle_Manager yüzeyi lifecycle_cleanup_receipt ile geri çekilmenin tamamlandığını doğrular.",
        ),
        proof_rules=(
            "Maliyet ledger'ı için en az bir kaynak tahsisi ve bir geri çekilme (cleanup) kanıtı birlikte aranır.",
            "Cleanup kanıtı yoksa ledger 'open' kalır ve tekrar çalıştırma için audit kilidi üretir.",
        ),
        downstream_outputs=("Memory_Deallocation_Force", "Cooling_Fan_Override", "System_Halt_Interrupt"),
    ),
)


def clean_value(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def clean_list(values: object) -> tuple[str, ...]:
    if not isinstance(values, list):
        return ()
    return tuple(clean_value(value) for value in values if clean_value(value))


def family_output_path(family: H11Family, knowledge_dir: Path = KNOWLEDGE_DIR) -> Path:
    return knowledge_dir / family.filename


def verify_existing_targets(targets: tuple[str, ...], knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    missing = [target for target in targets if not (knowledge_dir / f"{target}.md").exists()]
    if missing:
        raise FileNotFoundError(f"Eksik hedef notlar: {', '.join(missing)}")


def render_h11_note(family: H11Family) -> str:
    purpose_text = "\n\n".join(family.reflection_purpose)
    mapping_lines = "\n".join(f"- {item}" for item in family.audit_signal_mapping)
    contract_lines = "\n".join(f"- {item}" for item in family.evidence_contract_strategy)
    proof_lines = "\n".join(f"- {item}" for item in family.proof_rules)
    h10_lines = "\n".join(f"- [[{item}]]" for item in family.h10_inputs)
    output_lines = "\n".join(f"- [[{item}]]" for item in family.downstream_outputs)

    text = (
        "---\n"
        'date: "2026-08-31"\n'
        "tags:\n"
        + "".join(f'  - "{tag}"\n' for tag in family.tags)
        + f'reflection_mode: "{family.reflection_mode}"\n'
        + f'audit_signal: "{family.audit_signal}"\n'
        + "audit_surfaces:\n"
        + "".join(f'  - "{item}"\n' for item in family.audit_surfaces)
        + "audit_contracts:\n"
        + "".join(f'  - "{item}"\n' for item in family.audit_contracts)
        + "---\n\n"
        + f"# {family.title}\n\n"
        + "## Yansıma amacı\n\n"
        + f"{purpose_text}\n\n"
        + "## Audit signal eşlemesi\n\n"
        + f"{mapping_lines}\n\n"
        + "## Evidence surface sözleşmeleri\n\n"
        + f"{contract_lines}\n\n"
        + "## İspat ve tutarlılık kuralları\n\n"
        + f"{proof_lines}\n\n"
        + "## Besleyen H10 düğümleri\n\n"
        + f"{h10_lines}\n\n"
        + "## Üretilen audit çıktıları\n\n"
        + f"{output_lines}\n"
    )
    assert_no_forbidden_nodes(text)
    return text


def parse_section(text: str, header: str) -> str:
    pattern = re.compile(rf"{re.escape(header)}\n\n(.*?)(?=\n## |\Z)", re.S)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def verify_h11_note(path: Path, family: H11Family) -> dict[str, object]:
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

    if clean_value(frontmatter.get("reflection_mode", "")) != family.reflection_mode:
        raise ValueError(f"{path.name}: reflection_mode beklenen değerle uyuşmuyor")
    if clean_value(frontmatter.get("audit_signal", "")) != family.audit_signal:
        raise ValueError(f"{path.name}: audit_signal beklenen değerle uyuşmuyor")
    if clean_list(frontmatter.get("audit_surfaces", [])) != family.audit_surfaces:
        raise ValueError(f"{path.name}: audit_surfaces beklenen sırayla uyuşmuyor")
    if clean_list(frontmatter.get("audit_contracts", [])) != family.audit_contracts:
        raise ValueError(f"{path.name}: audit_contracts beklenen sırayla uyuşmuyor")

    source_section = parse_section(text, "## Besleyen H10 düğümleri")
    source_links = WIKILINK_RE.findall(source_section)
    if tuple(source_links) != family.h10_inputs:
        raise ValueError(f"{path.name}: H10 girdileri beklenen hedeflerle uyuşmuyor")

    output_section = parse_section(text, "## Üretilen audit çıktıları")
    output_links = WIKILINK_RE.findall(output_section)
    if tuple(output_links) != family.downstream_outputs:
        raise ValueError(f"{path.name}: audit çıktıları beklenen hedeflerle uyuşmuyor")

    return {
        "path": str(path),
        "h10_inputs": len(source_links),
        "audit_surfaces": len(family.audit_surfaces),
        "audit_contracts": len(family.audit_contracts),
        "downstream_outputs": len(output_links),
        "forbidden_refs": False,
    }


def write_h11_notes(*, force: bool = False, knowledge_dir: Path = KNOWLEDGE_DIR) -> list[Path]:
    targets = set()
    for family in H11_FAMILIES:
        targets.update(family.h10_inputs)
        targets.update(family.audit_surfaces)
        targets.update(family.downstream_outputs)
    verify_existing_targets(tuple(sorted(targets)), knowledge_dir)

    written: list[Path] = []
    for family in H11_FAMILIES:
        path = family_output_path(family, knowledge_dir=knowledge_dir)
        if path.exists() and not force:
            continue
        text = render_h11_note(family)
        path.write_text(text, encoding="utf-8")
        written.append(path)
    return sorted(written, key=lambda item: item.name)


def run_checks(paths: list[Path]) -> list[dict[str, object]]:
    lookup = {family.filename: family for family in H11_FAMILIES}
    results: list[dict[str, object]] = []
    for path in paths:
        family = lookup.get(path.name)
        if family is None:
            continue
        results.append(verify_h11_note(path, family))
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Wave 11 H11 reflection/audit notlarını üretir.")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--knowledge-dir", type=Path, default=KNOWLEDGE_DIR)
    args = parser.parse_args(argv)

    written = write_h11_notes(force=args.force, knowledge_dir=args.knowledge_dir)
    for path in written:
        print(path.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
