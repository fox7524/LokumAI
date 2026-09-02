from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.brain_growth.common import (
    KNOWLEDGE_DIR,
    PROJECT_ROOT,
    allowed_forward_targets,
    assert_link_target_layer_membership,
    assert_no_forbidden_nodes,
    build_note_filename,
    parse_wikilinks,
    parse_yaml_frontmatter,
)
from tools.brain_growth.h3_synthesis import (
    FAMILIES,
    SECTION_HEADERS as SYNTHESIS_REQUIRED_SECTIONS,
    family_output_path,
    parse_section,
    verify_note as verify_synthesis_family_note,
)
from tools.brain_growth.h5_builder import (
    H5_FAMILIES,
    SECTION_HEADERS as H5_REQUIRED_SECTIONS,
    family_output_path as h5_family_output_path,
    parse_section as parse_h5_section,
    verify_h5_note,
)
from tools.brain_growth.h6_builder import (
    H6_FAMILIES,
    SECTION_HEADERS as H6_REQUIRED_SECTIONS,
    family_output_path as h6_family_output_path,
    parse_section as parse_h6_section,
    verify_h6_note,
)
from tools.brain_growth.h7_builder import (
    H7_FAMILIES,
    SECTION_HEADERS as H7_REQUIRED_SECTIONS,
    family_output_path as h7_family_output_path,
    parse_section as parse_h7_section,
    verify_h7_note,
)
from tools.brain_growth.h8_builder import (
    H8_FAMILIES,
    SECTION_HEADERS as H8_REQUIRED_SECTIONS,
    family_output_path as h8_family_output_path,
    parse_section as parse_h8_section,
    verify_h8_note,
)
from tools.brain_growth.h9_builder import (
    H9_FAMILIES,
    SECTION_HEADERS as H9_REQUIRED_SECTIONS,
    family_output_path as h9_family_output_path,
    parse_section as parse_h9_section,
    verify_h9_note,
)
from tools.brain_growth.h10_builder import (
    H10_FAMILIES,
    SECTION_HEADERS as H10_REQUIRED_SECTIONS,
    family_output_path as h10_family_output_path,
    parse_section as parse_h10_section,
    verify_h10_note,
)
from tools.brain_growth.h11_builder import (
    H11_FAMILIES,
    SECTION_HEADERS as H11_REQUIRED_SECTIONS,
    family_output_path as h11_family_output_path,
    parse_section as parse_h11_section,
    verify_h11_note,
)
from tools.brain_growth.content_quality import classify_note_depth, compute_quality_score, required_sections_for_kind


RAW_FILENAME_RE = re.compile(r"^RAG_Memory_Cell_(\d{2})_([A-Za-z0-9_]+)\.md$")
SYNTHESIS_FILENAME_RE = re.compile(r"^H3_([A-Za-z0-9_]+)\.md$")
H4_FILENAME_RE = re.compile(r"^H4_([A-Za-z0-9_]+)\.md$")
H5_FILENAME_RE = re.compile(r"^H5_([A-Za-z0-9_]+)\.md$")
H6_FILENAME_RE = re.compile(r"^H6_([A-Za-z0-9_]+)\.md$")
H7_FILENAME_RE = re.compile(r"^H7_([A-Za-z0-9_]+)\.md$")
H8_FILENAME_RE = re.compile(r"^H8_([A-Za-z0-9_]+)\.md$")
H9_FILENAME_RE = re.compile(r"^H9_([A-Za-z0-9_]+)\.md$")
H10_FILENAME_RE = re.compile(r"^H10_([A-Za-z0-9_]+)\.md$")
H11_FILENAME_RE = re.compile(r"^H11_([A-Za-z0-9_]+)\.md$")
INDEX_FILENAME_RE = re.compile(r"^(Brain_Growth_Index|Index_[A-Za-z0-9_]+)\.md$")
TITLE_RE = re.compile(r"^# (.+)$", re.M)
PLACEHOLDER_PATTERNS = (
    re.compile(r"\bTBD\b", re.I),
    re.compile(r"\bTODO\b", re.I),
    re.compile(r"\bFIXME\b", re.I),
    re.compile(r"\bplaceholder\b", re.I),
)
RAW_REQUIRED_SECTIONS = (
    "## Teknik çekirdek",
    "## Doğrulanmış bulgular",
    "## LokumAI için çıkarım",
    "## Sorgu ipuçları",
    "## Kaynaklar",
)
INDEX_REQUIRED_SECTIONS = (
    "## Alanlar",
    "## Fazlar",
    "## Kullanım",
)
H4_REQUIRED_SECTIONS = (
    "## Yakınsama amacı",
    "## Tetikleyiciler",
    "## Karar sınırları",
    "## Besleyen sentez düğümleri",
    "## İleri yönlü etkiler",
)
REPORTS_DIR = PROJECT_ROOT / "docs" / "brain_growth" / "reports"
REPORT_FILENAME_STEM = "brain_growth_validation"
REPORT_KIND_ORDER = ("raw", "synthesis", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "h11", "index")
REQUIRED_SECTIONS_BY_KIND = {
    "raw": RAW_REQUIRED_SECTIONS,
    "synthesis": SYNTHESIS_REQUIRED_SECTIONS,
    "h4": H4_REQUIRED_SECTIONS,
    "h5": H5_REQUIRED_SECTIONS,
    "h6": H6_REQUIRED_SECTIONS,
    "h7": H7_REQUIRED_SECTIONS,
    "h8": H8_REQUIRED_SECTIONS,
    "h9": H9_REQUIRED_SECTIONS,
    "h10": H10_REQUIRED_SECTIONS,
    "h11": H11_REQUIRED_SECTIONS,
    "index": INDEX_REQUIRED_SECTIONS,
}
LINK_COMPLIANCE_ISSUE_CODES = {
    "invalid_target_layer",
    "insufficient_forward_links",
    "too_many_forward_links",
    "missing_target_note",
    "missing_h3_input",
    "missing_h4_input",
    "missing_h5_input",
    "missing_h6_input",
    "missing_h8_input",
    "missing_h9_input",
    "missing_h10_input",
}
REMEDIATION_GUIDANCE_BY_CODE: dict[str, dict[str, Any]] = {
    "missing_frontmatter": {
        "repair_class": "frontmatter_structure_repair",
        "summary": "YAML frontmatter bloğunu ekleyip not metadatasını şemaya geri taşı.",
        "recommended_actions": [
            "Notun başına --- ile başlayan geçerli YAML frontmatter ekle.",
            "date ve tags alanlarını ilgili katman şemasına göre doldur.",
        ],
    },
    "missing_tags": {
        "repair_class": "frontmatter_taxonomy_repair",
        "summary": "Boş veya eksik tags alanını katman taksonomisine göre tamamla.",
        "recommended_actions": [
            "tags alanını liste biçiminde tanımla.",
            "Katman ve domain etiketlerini quoted tag formatıyla ekle.",
        ],
    },
    "unquoted_tag": {
        "repair_class": "frontmatter_taxonomy_repair",
        "summary": "Tag değerlerini quoted YAML string formatına çevir.",
        "recommended_actions": [
            "Her tag satırını çift tırnak içinde sakla.",
            "Fix sonrası parse_yaml_frontmatter ile yeniden doğrula.",
        ],
    },
    "missing_tag": {
        "repair_class": "frontmatter_taxonomy_repair",
        "summary": "Katman için zorunlu tagleri frontmatter içine geri ekle.",
        "recommended_actions": [
            "İlgili layer tagini ekle.",
            "Domain veya aile tagleri eksikse note ailesi şemasıyla hizala.",
        ],
    },
    "missing_section": {
        "repair_class": "section_structure_repair",
        "summary": "Zorunlu başlıkları ve minimum içerik bloklarını yeniden yerleştir.",
        "recommended_actions": [
            "Eksik ## başlıklarını note şemasındaki sırayla ekle.",
            "Her yeni başlığın altına en az bir anlamlı açıklama veya madde yaz.",
        ],
    },
    "placeholder_phrase": {
        "repair_class": "content_completion_repair",
        "summary": "Placeholder metinleri gerçek içerikle değiştir.",
        "recommended_actions": [
            "TBD/TODO/FIXME benzeri yer tutucuları kaldır.",
            "İlgili bölümün gerçek karar, bulgu veya yönlendirme içeriğini yaz.",
        ],
    },
    "thin_note": {
        "repair_class": "content_depth_repair",
        "summary": "Raw note'u minimum içerik yoğunluğunu karşılayacak şekilde genişlet.",
        "recommended_actions": [
            "Teknik çekirdek ve çıkarım bölümlerine anlamlı açıklamalar ekle.",
            "Notu yalnız başlık seviyesinde bırakma; mekanizma, sınırlama ve örnek detayları yaz.",
        ],
    },
    "missing_sources": {
        "repair_class": "source_grounding_repair",
        "summary": "Kaynaklar bölümünü doğrulanabilir dış bağlantılarla tamamla.",
        "recommended_actions": [
            "Kaynaklar bölümüne en az bir geçerli http/https referansı ekle.",
            "Kaynakların nottaki iddiaları gerçekten desteklediğini kontrol et.",
        ],
    },
    "filename_mismatch": {
        "repair_class": "filename_title_alignment_repair",
        "summary": "Dosya adı ile başlığı aynı şemaya hizala.",
        "recommended_actions": [
            "Başlıktan beklenen slug'ı türet.",
            "Dosya adını veya başlığı aynı normalize edilmiş isimde buluştur.",
        ],
    },
    "forbidden_node_reference": {
        "repair_class": "forbidden_reference_cleanup",
        "summary": "Yasaklı düğüm referanslarını semantik grafikten çıkar.",
        "recommended_actions": [
            "LokumAI-1.0 ve benzeri yasaklı referansları kaldır.",
            "Gerekliyse izinli katman düğümlerinden eşdeğer hedef seç.",
        ],
    },
    "invalid_target_layer": {
        "repair_class": "graph_link_target_repair",
        "summary": "Wikilink hedeflerini izinli katman üyelerine döndür.",
        "recommended_actions": [
            "İleri linklerin allowed_forward_targets kümesine ait olduğunu doğrula.",
            "Yanlış katman veya serbest metin hedeflerini gerçek note düğümleriyle değiştir.",
        ],
    },
    "insufficient_source_inputs": {
        "repair_class": "graph_input_coverage_repair",
        "summary": "Kaynak giriş sayısını katman minimumuna yükselt.",
        "recommended_actions": [
            "Eksik upstream note bağlantılarını ekle.",
            "Girdi sayısını ilgili validator metriğinin minimumuna getir.",
        ],
    },
    "insufficient_forward_links": {
        "repair_class": "graph_output_coverage_repair",
        "summary": "Downstream çıktı veya ileri bağlantı sayısını asgari seviyeye çıkar.",
        "recommended_actions": [
            "İlgili note için gereken minimum ileri wikilink sayısını ekle.",
            "Bağlantıları gerçekten var olan downstream note'lara yönlendir.",
        ],
    },
    "too_many_forward_links": {
        "repair_class": "graph_output_coverage_repair",
        "summary": "İleri link hacmini katman sınırına indir.",
        "recommended_actions": [
            "Gereksiz downstream linkleri kaldır.",
            "Sadece note ailesi şemasında izin verilen kadar hedef bırak.",
        ],
    },
    "missing_target_note": {
        "repair_class": "graph_target_existence_repair",
        "summary": "Eksik hedef notları oluştur veya referansları mevcut notlarla değiştir.",
        "recommended_actions": [
            "Her wikilink hedefi için karşılık gelen .md notunun varlığını doğrula.",
            "Yoksa hedef notu üret ya da bağlantıyı mevcut notla değiştir.",
        ],
    },
    "missing_h3_input": {
        "repair_class": "graph_input_coverage_repair",
        "summary": "H4 notuna en az bir H3 girişi bağla.",
        "recommended_actions": [
            "Besleyen sentez düğümleri bölümüne H3_* wikilink ekle.",
        ],
    },
    "missing_h4_input": {
        "repair_class": "graph_input_coverage_repair",
        "summary": "H5 notuna en az bir H4 girişi bağla.",
        "recommended_actions": [
            "Besleyen H4 düğümleri bölümüne H4_* wikilink ekle.",
        ],
    },
    "missing_h5_input": {
        "repair_class": "graph_input_coverage_repair",
        "summary": "H6 notuna birden fazla H5 girişi bağla.",
        "recommended_actions": [
            "Besleyen H5 düğümleri bölümüne en az iki H5_* wikilink ekle.",
            "Tek girişli executive note'ları çoklu H5 koordinasyon şemasına yükselt.",
        ],
    },
    "missing_h6_input": {
        "repair_class": "graph_input_coverage_repair",
        "summary": "H7 notuna en az bir H6 girişi bağla.",
        "recommended_actions": [
            "Besleyen H6 düğümleri bölümüne en az bir H6_* wikilink ekle.",
            "Episodik notun upstream executive orkestrasyon kaynağını açıkça bağla.",
        ],
    },
    "missing_h7_input": {
        "repair_class": "graph_input_coverage_repair",
        "summary": "H8 notuna en az bir H7 girişi bağla.",
        "recommended_actions": [
            "Besleyen H7 düğümleri bölümüne en az bir H7_* wikilink ekle.",
            "Karar montaj notunu episodik-temporal kaynağa açıkça bağla.",
        ],
    },
    "missing_temporal_relation": {
        "repair_class": "temporal_edge_schema_repair",
        "summary": "Temporal edge şemasını en az bir açık ilişkiyle tamamla.",
        "recommended_actions": [
            "Frontmatter içindeki temporal_relations alanına en az bir ilişki ekle.",
            "before/after/co_occurs gibi H7 episodik modeline uygun ilişki adları kullan.",
        ],
    },
    "missing_entity_event_binding": {
        "repair_class": "entity_event_binding_repair",
        "summary": "Entity-event bağlama stratejisini açık, anlamlı içerikle tamamla.",
        "recommended_actions": [
            "Entity-event bağlama stratejisi bölümüne en az bir açıklama veya madde ekle.",
            "Bağların hangi entity ve event kümelerini nasıl ilişkilendirdiğini belirt.",
        ],
    },
    "invalid_episode_mode": {
        "repair_class": "episodic_frontmatter_repair",
        "summary": "episode_mode alanını desteklenen H7 episodik modlarından biriyle hizala.",
        "recommended_actions": [
            "Frontmatter içindeki episode_mode değerini H7 builder ailesindeki geçerli modlardan biriyle değiştir.",
            "Episode kipini temporal_relations ve episodik amaç içeriğiyle tutarlı seç.",
        ],
    },
    "missing_primary_entities": {
        "repair_class": "episodic_frontmatter_repair",
        "summary": "primary_entities alanını episodik aktör setiyle doldur.",
        "recommended_actions": [
            "Frontmatter içindeki primary_entities listesine en az bir entity ekle.",
            "Entity isimlerini episode_mode ve bağlama stratejisiyle uyumlu tut.",
        ],
    },
    "missing_primary_events": {
        "repair_class": "episodic_frontmatter_repair",
        "summary": "primary_events alanını episodik olay setiyle doldur.",
        "recommended_actions": [
            "Frontmatter içindeki primary_events listesine en az bir event ekle.",
            "Event isimlerini temporal_relations ve entity binding kurgusuyla uyumlu seç.",
        ],
    },
    "invalid_workspace_mode": {
        "repair_class": "workspace_frontmatter_repair",
        "summary": "workspace_mode alanını desteklenen H8 workspace kiplerinden biriyle hizala.",
        "recommended_actions": [
            "Frontmatter içindeki workspace_mode değerini H8 builder ailesindeki geçerli kiplerle değiştir.",
            "Workspace kipini dominant_thoughtseed ve policy broadcast içeriğiyle tutarlı seç.",
        ],
    },
    "missing_dominant_thoughtseed": {
        "repair_class": "workspace_frontmatter_repair",
        "summary": "dominant_thoughtseed alanını boş bırakma; karar çekirdeğini açıkça tanımla.",
        "recommended_actions": [
            "Frontmatter içine en az bir dominant_thoughtseed değeri yaz.",
            "Thoughtseed adını candidate_policies ve commitment mantığıyla uyumlu seç.",
        ],
    },
    "missing_candidate_policy": {
        "repair_class": "policy_broadcast_repair",
        "summary": "Aday policy listesini karar montajına uygun şekilde doldur.",
        "recommended_actions": [
            "candidate_policies listesine en az bir policy ekle.",
            "Policy adlarını downstream broadcast ve thoughtseed seçimiyle uyumlu tut.",
        ],
    },
    "missing_broadcast_target": {
        "repair_class": "policy_broadcast_repair",
        "summary": "Broadcast hedeflerini açık hedef notlara bağla.",
        "recommended_actions": [
            "broadcast_targets listesine en az bir mevcut note hedefi ekle.",
            "Hedeflerin execution veya consensus yüzeylerine işaret ettiğini doğrula.",
        ],
    },
    "missing_policy_broadcast_strategy": {
        "repair_class": "policy_broadcast_repair",
        "summary": "Policy broadcast stratejisi bölümünü anlamlı içerikle doldur.",
        "recommended_actions": [
            "Policy broadcast stratejisi bölümüne en az bir açıklama veya madde ekle.",
            "Policy seçimi ile hedef yayın sırasını açıkça belirt.",
        ],
    },
    "missing_commitment_rule": {
        "repair_class": "decision_commitment_repair",
        "summary": "Commitment kurallarını açık, test edilebilir koşullarla yaz.",
        "recommended_actions": [
            "Commitment kuralları bölümüne en az bir karar eşiği veya koşulu ekle.",
            "Policy commit ile H7 kanıtı arasındaki ilişkiyi somutlaştır.",
        ],
    },
    "synthesis_spec_violation": {
        "repair_class": "family_spec_alignment_repair",
        "summary": "H3 aile notunu builder spesifikasyonuyla yeniden hizala.",
        "recommended_actions": [
            "İlgili H3 family tanımındaki giriş/çıkış sırasını uygula.",
        ],
    },
    "h5_spec_violation": {
        "repair_class": "family_spec_alignment_repair",
        "summary": "H5 aile notunu builder spesifikasyonuyla yeniden hizala.",
        "recommended_actions": [
            "İlgili H5 family tanımındaki giriş/çıkış sırasını uygula.",
        ],
    },
    "h6_spec_violation": {
        "repair_class": "family_spec_alignment_repair",
        "summary": "H6 aile notunu builder spesifikasyonuyla yeniden hizala.",
        "recommended_actions": [
            "İlgili H6 family tanımındaki giriş/çıkış sırasını uygula.",
        ],
    },
    "h7_spec_violation": {
        "repair_class": "family_spec_alignment_repair",
        "summary": "H7 aile notunu builder spesifikasyonuyla yeniden hizala.",
        "recommended_actions": [
            "İlgili H7 family tanımındaki episodik frontmatter ve giriş/çıkış sırasını uygula.",
        ],
    },
    "h8_spec_violation": {
        "repair_class": "family_spec_alignment_repair",
        "summary": "H8 aile notunu builder spesifikasyonuyla yeniden hizala.",
        "recommended_actions": [
            "İlgili H8 family tanımındaki workspace frontmatter ve giriş/çıkış sırasını uygula.",
        ],
    },
    "invalid_package_mode": {
        "repair_class": "package_frontmatter_repair",
        "summary": "package_mode alanını desteklenen H9 paketleme kiplerinden biriyle hizala.",
        "recommended_actions": [
            "Frontmatter içindeki package_mode değerini H9 builder ailesindeki geçerli kiplerle değiştir.",
            "Paketleme kipini source_policy ve delivery surface sözleşmeleriyle tutarlı seç.",
        ],
    },
    "missing_source_policy": {
        "repair_class": "package_frontmatter_repair",
        "summary": "source_policy alanını boş bırakma; paketlenen policy kaynağını açıkça tanımla.",
        "recommended_actions": [
            "Frontmatter içine en az bir source_policy değeri yaz.",
            "Source policy adını package_mode ve package_contracts ile uyumlu seç.",
        ],
    },
    "missing_delivery_surface": {
        "repair_class": "delivery_surface_contract_repair",
        "summary": "delivery_surfaces alanını geçerli teslim yüzeyleriyle doldur.",
        "recommended_actions": [
            "delivery_surfaces listesine en az bir mevcut note hedefi ekle.",
            "Surface isimlerinin paketlenen çıktı yolları ve sözleşme metniyle uyumlu olduğunu doğrula.",
        ],
    },
    "missing_package_contract": {
        "repair_class": "package_contract_repair",
        "summary": "package_contracts alanını paketleme sözleşmeleriyle doldur.",
        "recommended_actions": [
            "package_contracts listesine en az bir paket sözleşmesi ekle.",
            "Sözleşme isimlerini delivery surface ve readiness kurallarıyla uyumlu tut.",
        ],
    },
    "missing_h8_input": {
        "repair_class": "graph_input_coverage_repair",
        "summary": "H9 notuna en az bir H8 girişi bağla.",
        "recommended_actions": [
            "Besleyen H8 düğümleri bölümüne en az bir H8_* wikilink ekle.",
            "Paketleme notunu karar montaj kaynağına açıkça bağla.",
        ],
    },
    "missing_source_policy_mapping": {
        "repair_class": "source_policy_mapping_repair",
        "summary": "Source policy eşlemesi bölümünü anlamlı içerikle doldur.",
        "recommended_actions": [
            "Source policy eşlemesi bölümüne en az bir açıklama veya madde ekle.",
            "Policy kaynağının paketleme moduna nasıl dönüştüğünü açıkça belirt.",
        ],
    },
    "missing_delivery_surface_contract": {
        "repair_class": "delivery_surface_contract_repair",
        "summary": "Delivery surface sözleşmeleri bölümünü yüzey bazlı kontratlarla tamamla.",
        "recommended_actions": [
            "Delivery surface sözleşmeleri bölümüne en az bir açıklama veya madde ekle.",
            "Her surface için beklenen paket veya kontrat davranışını belirt.",
        ],
    },
    "missing_readiness_rule": {
        "repair_class": "packaging_readiness_repair",
        "summary": "Readiness ve commit koşulları bölümünü test edilebilir paketleme eşiğiyle tamamla.",
        "recommended_actions": [
            "Readiness ve commit koşulları bölümüne en az bir koşul veya eşik ekle.",
            "Paketin hangi durumda yayınlanacağı veya hold-state'te kalacağı bilgisini açıkça yaz.",
        ],
    },
    "h9_spec_violation": {
        "repair_class": "family_spec_alignment_repair",
        "summary": "H9 aile notunu builder spesifikasyonuyla yeniden hizala.",
        "recommended_actions": [
            "İlgili H9 family tanımındaki paketleme frontmatter ve giriş/çıkış sırasını uygula.",
        ],
    },
    "invalid_supervision_mode": {
        "repair_class": "supervision_frontmatter_repair",
        "summary": "supervision_mode alanını desteklenen H10 supervision kiplerinden biriyle hizala.",
        "recommended_actions": [
            "Frontmatter içindeki supervision_mode değerini H10 builder ailesindeki geçerli kiplerle değiştir.",
            "Supervision kipini governing_signal ve oversight contracts ile tutarlı seç.",
        ],
    },
    "missing_governing_signal": {
        "repair_class": "supervision_frontmatter_repair",
        "summary": "governing_signal alanını boş bırakma; stratejik denetim sinyalini açıkça tanımla.",
        "recommended_actions": [
            "Frontmatter içine en az bir governing_signal değeri yaz.",
            "Sinyal adını supervision_mode ve supervision_contracts ile uyumlu seç.",
        ],
    },
    "missing_oversight_surface": {
        "repair_class": "oversight_surface_contract_repair",
        "summary": "oversight_surfaces alanını geçerli stratejik yüzeylerle doldur.",
        "recommended_actions": [
            "oversight_surfaces listesine en az bir mevcut note hedefi ekle.",
            "Surface isimlerinin supervised output ve oversight sözleşmesiyle uyumlu olduğunu doğrula.",
        ],
    },
    "missing_supervision_contract": {
        "repair_class": "supervision_contract_repair",
        "summary": "supervision_contracts alanını stratejik denetim sözleşmeleriyle doldur.",
        "recommended_actions": [
            "supervision_contracts listesine en az bir supervision sözleşmesi ekle.",
            "Sözleşme isimlerini oversight yüzeyleri ve escalation kurallarıyla uyumlu tut.",
        ],
    },
    "missing_h9_input": {
        "repair_class": "graph_input_coverage_repair",
        "summary": "H10 notuna en az bir H9 girişi bağla.",
        "recommended_actions": [
            "Besleyen H9 düğümleri bölümüne en az bir H9_* wikilink ekle.",
            "Supervision notunu execution packaging kaynağına açıkça bağla.",
        ],
    },
    "missing_governing_signal_mapping": {
        "repair_class": "governing_signal_mapping_repair",
        "summary": "Governing signal eşlemesi bölümünü anlamlı içerikle doldur.",
        "recommended_actions": [
            "Governing signal eşlemesi bölümüne en az bir açıklama veya madde ekle.",
            "Signal'in supervision katmanına nasıl dönüştüğünü açıkça belirt.",
        ],
    },
    "missing_oversight_surface_contract": {
        "repair_class": "oversight_surface_contract_repair",
        "summary": "Oversight surface sözleşmeleri bölümünü yüzey bazlı stratejik kontratlarla tamamla.",
        "recommended_actions": [
            "Oversight surface sözleşmeleri bölümüne en az bir açıklama veya madde ekle.",
            "Her oversight surface için beklenen denetim davranışını belirt.",
        ],
    },
    "missing_escalation_rule": {
        "repair_class": "strategic_escalation_repair",
        "summary": "Escalation ve rollback kuralları bölümünü test edilebilir stratejik eşiklerle tamamla.",
        "recommended_actions": [
            "Escalation ve rollback kuralları bölümüne en az bir koşul veya eşik ekle.",
            "Paketin hangi durumda geri alınacağı veya üst seviyeye taşınacağı bilgisini açıkça yaz.",
        ],
    },
    "h10_spec_violation": {
        "repair_class": "family_spec_alignment_repair",
        "summary": "H10 aile notunu builder spesifikasyonuyla yeniden hizala.",
        "recommended_actions": [
            "İlgili H10 family tanımındaki supervision frontmatter ve giriş/çıkış sırasını uygula.",
        ],
    },
}
SECTION_FIX_CONTENT: dict[str, dict[str, str]] = {
    "raw": {
        "## Teknik çekirdek": "Bu bölüm validator --fix modu tarafından yapısal bütünlük için eklendi.",
        "## Doğrulanmış bulgular": "- Doğrulanmış bulgu satırı eklenmelidir.",
        "## LokumAI için çıkarım": "Bu bölüm validator --fix modu tarafından yapısal bütünlük için eklendi.",
        "## Sorgu ipuçları": "- Sorgu ipucu eklenmelidir.",
        "## Kaynaklar": "- Kaynak bağlantısı eklenmelidir.",
    },
    "synthesis": {
        "## Soyutlama": "Bu bölüm validator --fix modu tarafından yapısal bütünlük için eklendi.",
        "## İnvariantlar": "- İnvariant satırı eklenmelidir.",
        "## Retrieval yönlendirme anlamı": "- Retrieval yönlendirme notu eklenmelidir.",
        "## Besleyen düğümler": "### RAG_Memory_Cell_13+ girdileri\n\n- Girdi bağlantıları elle eklenmelidir.\n\n### Mevcut anchor düğümler\n\n- Anchor bağlantıları elle eklenmelidir.",
        "## İleri besleme": "- İleri besleme bağlantıları elle eklenmelidir.",
    },
    "h4": {
        "## Yakınsama amacı": "Bu bölüm validator --fix modu tarafından yapısal bütünlük için eklendi.",
        "## Tetikleyiciler": "- Tetikleyici satırı eklenmelidir.",
        "## Karar sınırları": "- Karar sınırı satırı eklenmelidir.",
        "## Besleyen sentez düğümleri": "### Hidden_3 sentez girdileri\n\n- H3 bağlantıları elle eklenmelidir.\n\n### Stratejik anchor düğümler\n\n- Anchor bağlantıları elle eklenmelidir.",
        "## İleri yönlü etkiler": "- İleri yönlü etki bağlantıları elle eklenmelidir.",
    },
    "h5": {
        "## Kontrol amacı": "Bu bölüm validator --fix modu tarafından yapısal bütünlük için eklendi.",
        "## Arbitration sinyalleri": "- Arbitration sinyali satırı eklenmelidir.",
        "## Karar politikası": "- Karar politikası satırı eklenmelidir.",
        "## Besleyen H4 düğümleri": "### Hidden_4 arbitration girdileri\n\n- H4 bağlantıları elle eklenmelidir.\n\n### Metacognitive control anchor düğümleri\n\n- Anchor bağlantıları elle eklenmelidir.",
        "## Yönettiği çıktı yolları": "- Çıktı yolu bağlantıları elle eklenmelidir.",
    },
    "h6": {
        "## Orkestrasyon amacı": "Bu bölüm validator --fix modu tarafından yapısal bütünlük için eklendi.",
        "## Yürütücü sinyaller": "- Yürütücü sinyali eklenmelidir.",
        "## Orkestrasyon politikası": "- Orkestrasyon politikası eklenmelidir.",
        "## Besleyen H5 düğümleri": "### Hidden_5 executive girdileri\n\n- H5 bağlantıları elle eklenmelidir.\n\n### Executive orchestration anchor düğümleri\n\n- Anchor bağlantıları elle eklenmelidir.",
        "## Koordine ettiği çıktı yolları": "- Koordine edilen çıktı bağlantıları elle eklenmelidir.",
    },
    "h8": {
        "## Karar montaj amacı": "Bu bölüm validator --fix modu tarafından yapısal bütünlük için eklendi.",
        "## Dominant thoughtseed sinyalleri": "- Dominant thoughtseed sinyali eklenmelidir.",
        "## Policy broadcast stratejisi": "- Policy broadcast stratejisi elle eklenmelidir.",
        "## Commitment kuralları": "- Commitment kuralı elle eklenmelidir.",
        "## Besleyen H7 düğümleri": "- H7 bağlantıları elle eklenmelidir.",
        "## Yayınlanan çıktı yolları": "- Yayınlanan çıktı bağlantıları elle eklenmelidir.",
    },
    "h9": {
        "## Paketleme amacı": "Bu bölüm validator --fix modu tarafından yapısal bütünlük için eklendi.",
        "## Source policy eşlemesi": "- Source policy eşlemesi elle eklenmelidir.",
        "## Delivery surface sözleşmeleri": "- Delivery surface sözleşmesi elle eklenmelidir.",
        "## Readiness ve commit koşulları": "- Readiness ve commit kuralı elle eklenmelidir.",
        "## Besleyen H8 düğümleri": "- H8 bağlantıları elle eklenmelidir.",
        "## Paketlenen çıktı yolları": "- Paketlenen çıktı bağlantıları elle eklenmelidir.",
    },
    "h10": {
        "## Stratejik denetim amacı": "Bu bölüm validator --fix modu tarafından yapısal bütünlük için eklendi.",
        "## Governing signal eşlemesi": "- Governing signal eşlemesi elle eklenmelidir.",
        "## Oversight surface sözleşmeleri": "- Oversight surface sözleşmesi elle eklenmelidir.",
        "## Escalation ve rollback kuralları": "- Escalation ve rollback kuralı elle eklenmelidir.",
        "## Besleyen H9 düğümleri": "- H9 bağlantıları elle eklenmelidir.",
        "## Denetlenen çıktı yolları": "- Denetlenen çıktı bağlantıları elle eklenmelidir.",
    },
    "index": {
        "## Alanlar": "- Alan girdileri eklenmelidir.",
        "## Fazlar": "- Faz özeti eklenmelidir.",
        "## Kullanım": "- Kullanım yönergesi eklenmelidir.",
    },
}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str


@dataclass
class FileReport:
    path: str
    kind: str
    title: str | None
    ok: bool
    issues: list[ValidationIssue] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)


def clean_tag(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def build_issue(code: str, message: str) -> ValidationIssue:
    return ValidationIssue(code=code, message=message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_frontmatter(text: str) -> bool:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return False
    return "---" in {line.strip() for line in lines[1:]}


def extract_title(text: str) -> str | None:
    match = TITLE_RE.search(text)
    return match.group(1).strip() if match else None


def quoted_tag_values(frontmatter: dict[str, object]) -> list[str]:
    tags = frontmatter.get("tags", [])
    if not isinstance(tags, list):
        return []
    return [str(tag).strip() for tag in tags if str(tag).strip()]


def raw_note_paths(knowledge_dir: Path) -> list[Path]:
    selected: list[tuple[int, Path]] = []
    for path in knowledge_dir.glob("RAG_Memory_Cell_*.md"):
        match = RAW_FILENAME_RE.match(path.name)
        if not match:
            continue
        index = int(match.group(1))
        if index >= 13:
            selected.append((index, path))
    return [path for _, path in sorted(selected, key=lambda item: item[0])]


def synthesis_note_paths(knowledge_dir: Path) -> list[Path]:
    return sorted(knowledge_dir.glob("H3_*.md"))


def h4_note_paths(knowledge_dir: Path) -> list[Path]:
    return sorted(knowledge_dir.glob("H4_*.md"))


def h5_note_paths(knowledge_dir: Path) -> list[Path]:
    return sorted(knowledge_dir.glob("H5_*.md"))


def h6_note_paths(knowledge_dir: Path) -> list[Path]:
    return sorted(knowledge_dir.glob("H6_*.md"))


def h7_note_paths(knowledge_dir: Path) -> list[Path]:
    return sorted(knowledge_dir.glob("H7_*.md"))


def h8_note_paths(knowledge_dir: Path) -> list[Path]:
    return sorted(knowledge_dir.glob("H8_*.md"))


def h9_note_paths(knowledge_dir: Path) -> list[Path]:
    return sorted(knowledge_dir.glob("H9_*.md"))


def h10_note_paths(knowledge_dir: Path) -> list[Path]:
    return sorted(knowledge_dir.glob("H10_*.md"))


def h11_note_paths(knowledge_dir: Path) -> list[Path]:
    return sorted(knowledge_dir.glob("H11_*.md"))


def index_note_paths(knowledge_dir: Path) -> list[Path]:
    selected = [path for path in knowledge_dir.glob("*.md") if INDEX_FILENAME_RE.match(path.name)]
    return sorted(selected)


def collect_paths(scope: str, knowledge_dir: Path) -> dict[str, list[Path]]:
    if scope == "raw":
        return {"raw": raw_note_paths(knowledge_dir)}
    if scope == "synthesis":
        return {"synthesis": synthesis_note_paths(knowledge_dir)}
    if scope == "h4":
        return {"h4": h4_note_paths(knowledge_dir)}
    if scope == "h5":
        return {"h5": h5_note_paths(knowledge_dir)}
    if scope == "h6":
        return {"h6": h6_note_paths(knowledge_dir)}
    if scope == "h7":
        return {"h7": h7_note_paths(knowledge_dir)}
    if scope == "h8":
        return {"h8": h8_note_paths(knowledge_dir)}
    if scope == "h9":
        return {"h9": h9_note_paths(knowledge_dir)}
    if scope == "h10":
        return {"h10": h10_note_paths(knowledge_dir)}
    if scope == "h11":
        return {"h11": h11_note_paths(knowledge_dir)}
    if scope == "index":
        return {"index": index_note_paths(knowledge_dir)}
    return {
        "raw": raw_note_paths(knowledge_dir),
        "synthesis": synthesis_note_paths(knowledge_dir),
        "h4": h4_note_paths(knowledge_dir),
        "h5": h5_note_paths(knowledge_dir),
        "h6": h6_note_paths(knowledge_dir),
        "h7": h7_note_paths(knowledge_dir),
        "h8": h8_note_paths(knowledge_dir),
        "h9": h9_note_paths(knowledge_dir),
        "h10": h10_note_paths(knowledge_dir),
        "h11": h11_note_paths(knowledge_dir),
        "index": index_note_paths(knowledge_dir),
    }


def missing_sections(text: str, required_sections: tuple[str, ...]) -> list[str]:
    return [section for section in required_sections if section not in text]


def placeholder_hits(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in PLACEHOLDER_PATTERNS:
        hits.extend(sorted({match.group(0) for match in pattern.finditer(text)}))
    return hits


def content_quality_metrics(kind: str, text: str, *, inbound_links: int = 0, outbound_links: int = 0) -> dict[str, Any]:
    required_sections = required_sections_for_kind(kind) or REQUIRED_SECTIONS_BY_KIND.get(kind, ())
    note_depth = classify_note_depth(text, required_section_count=len(required_sections))
    content_quality = compute_quality_score(
        text=text,
        required_sections=required_sections,
        inbound_links=inbound_links,
        outbound_links=outbound_links,
    )
    if kind == "raw" and note_depth == "medium":
        if content_quality["technical_depth_score"] < 0.08 and content_quality["structure_score"] < 0.5:
            note_depth = "thin"
    return {
        "note_depth": note_depth,
        "content_quality": content_quality,
    }


def validate_common_shape(
    path: Path,
    text: str,
    required_sections: tuple[str, ...],
    required_tags: tuple[str, ...],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if not has_frontmatter(text):
        issues.append(build_issue("missing_frontmatter", f"{path.name}: YAML frontmatter eksik"))
        frontmatter: dict[str, object] = {}
        tag_values: list[str] = []
        cleaned_tags: set[str] = set()
    else:
        frontmatter = parse_yaml_frontmatter(text)
        tag_values = quoted_tag_values(frontmatter)
        cleaned_tags = {clean_tag(tag) for tag in tag_values}

        if not tag_values:
            issues.append(build_issue("missing_tags", f"{path.name}: tags frontmatter alanı eksik"))
        elif any(not ((tag.startswith('"') and tag.endswith('"')) or (tag.startswith("'") and tag.endswith("'"))) for tag in tag_values):
            issues.append(build_issue("unquoted_tag", f"{path.name}: quoted tag kuralı ihlal edilmiş"))

        for tag in required_tags:
            if tag not in cleaned_tags:
                issues.append(build_issue("missing_tag", f"{path.name}: gerekli tag eksik: {tag}"))

    sections = missing_sections(text, required_sections)
    if sections:
        issues.append(build_issue("missing_section", f"{path.name}: eksik bölümler: {', '.join(sections)}"))

    try:
        assert_no_forbidden_nodes(text)
    except ValueError as exc:
        issues.append(build_issue("forbidden_node_reference", str(exc)))

    hits = placeholder_hits(text)
    if hits:
        issues.append(build_issue("placeholder_phrase", f"{path.name}: placeholder ifadesi bulundu: {', '.join(hits)}"))

    return issues


def validate_raw_note(path: Path, knowledge_dir: Path = KNOWLEDGE_DIR) -> FileReport:
    text = read_text(path)
    title = extract_title(text)
    issues = validate_common_shape(
        path=path,
        text=text,
        required_sections=RAW_REQUIRED_SECTIONS,
        required_tags=("#rag/memory_cell", "#rag/training"),
    )

    match = RAW_FILENAME_RE.match(path.name)
    if not match:
        issues.append(build_issue("filename_mismatch", f"{path.name}: raw note dosya adı deseni geçersiz"))
        index = None
    else:
        index = int(match.group(1))
        expected_name = build_note_filename("RAG_Memory_Cell", title or "", index=index) if title else None
        if expected_name is not None and path.name != expected_name:
            issues.append(
                build_issue(
                    "filename_mismatch",
                    f"{path.name}: başlık dosya adıyla uyuşmuyor (beklenen dosya adı: {expected_name})",
                )
            )

    links = parse_wikilinks(text)
    quality_metrics = content_quality_metrics("raw", text, outbound_links=len(links))
    quality_scores = quality_metrics["content_quality"]

    if quality_metrics["note_depth"] == "thin":
        issues.append(build_issue("thin_note", f"{path.name}: raw note içerik derinliği çok düşük"))
    if quality_scores["source_grounding_score"] == 0.0:
        issues.append(build_issue("missing_sources", f"{path.name}: kaynaklar bölümü doğrulanmış dış kaynak içermiyor"))

    if len(links) < 4:
        issues.append(build_issue("insufficient_forward_links", f"{path.name}: en az 4 ileri wikilink gerekli"))

    try:
        assert_link_target_layer_membership(links, allowed_targets=allowed_forward_targets(knowledge_dir))
    except ValueError as exc:
        issues.append(build_issue("invalid_target_layer", str(exc)))

    return FileReport(
        path=str(path),
        kind="raw",
        title=title,
        ok=not issues,
        issues=issues,
        metrics={
            "index": index,
            "wikilink_count": len(links),
            **quality_metrics,
        },
    )


def synthesis_family_lookup() -> dict[str, Any]:
    return {family_output_path(spec).name: spec for spec in FAMILIES}


def validate_synthesis_note(path: Path, knowledge_dir: Path = KNOWLEDGE_DIR) -> FileReport:
    text = read_text(path)
    title = extract_title(text)
    issues = validate_common_shape(
        path=path,
        text=text,
        required_sections=SYNTHESIS_REQUIRED_SECTIONS,
        required_tags=("#layer/hidden_3_logic_synthesis",),
    )

    if not SYNTHESIS_FILENAME_RE.match(path.name):
        issues.append(build_issue("filename_mismatch", f"{path.name}: synthesis dosya adı deseni geçersiz"))
    elif title:
        expected_name = build_note_filename("H3", title)
        if path.name != expected_name:
            issues.append(
                build_issue(
                    "filename_mismatch",
                    f"{path.name}: başlık dosya adıyla uyuşmuyor (beklenen dosya adı: {expected_name})",
                )
            )

    source_section = parse_section(text, "## Besleyen düğümler")
    forward_section = parse_section(text, "## İleri besleme")
    source_links = parse_wikilinks(source_section)
    forward_links = parse_wikilinks(forward_section)
    raw_inputs = [target for target in source_links if target.startswith("RAG_Memory_Cell_")]
    anchor_inputs = [target for target in source_links if not target.startswith("RAG_Memory_Cell_")]

    if len(raw_inputs) < 8:
        issues.append(build_issue("insufficient_source_inputs", f"{path.name}: en az 8 raw girdi gerekli"))
    if len(forward_links) < 1:
        issues.append(build_issue("insufficient_forward_links", f"{path.name}: en az 1 ileri besleme linki gerekli"))
    if len(forward_links) > 3:
        issues.append(build_issue("too_many_forward_links", f"{path.name}: en fazla 3 ileri besleme linki olmalı"))

    existing_stems = {candidate.stem for candidate in knowledge_dir.glob("*.md")}
    for target in raw_inputs + anchor_inputs + forward_links:
        if target not in existing_stems:
            issues.append(build_issue("missing_target_note", f"{path.name}: hedef not bulunamadı: {target}"))

    spec = synthesis_family_lookup().get(path.name)
    if spec is not None:
        try:
            verify_synthesis_family_note(path, spec)
        except ValueError as exc:
            issues.append(build_issue("synthesis_spec_violation", str(exc)))

    return FileReport(
        path=str(path),
        kind="synthesis",
        title=title,
        ok=not issues,
        issues=issues,
        metrics={
            "raw_inputs": len(raw_inputs),
            "anchor_inputs": len(anchor_inputs),
            "forward_links": len(forward_links),
        },
    )


def validate_h4_note(path: Path, knowledge_dir: Path = KNOWLEDGE_DIR) -> FileReport:
    text = read_text(path)
    title = extract_title(text)
    issues = validate_common_shape(
        path=path,
        text=text,
        required_sections=H4_REQUIRED_SECTIONS,
        required_tags=("#layer/hidden_4_reasoning_convergence",),
    )

    if not H4_FILENAME_RE.match(path.name):
        issues.append(build_issue("filename_mismatch", f"{path.name}: hidden_4 dosya adı deseni geçersiz"))

    source_section = parse_section(text, "## Besleyen sentez düğümleri")
    forward_section = parse_section(text, "## İleri yönlü etkiler")
    source_links = parse_wikilinks(source_section)
    forward_links = parse_wikilinks(forward_section)
    h3_inputs = [target for target in source_links if target.startswith("H3_")]
    anchor_inputs = [target for target in source_links if not target.startswith("H3_")]

    if len(h3_inputs) < 1:
        issues.append(build_issue("missing_h3_input", f"{path.name}: en az bir H3 girdi linki gerekli"))
    if len(forward_links) < 1:
        issues.append(build_issue("insufficient_forward_links", f"{path.name}: en az 1 ileri yönlü etki linki gerekli"))

    existing_stems = {candidate.stem for candidate in knowledge_dir.glob("*.md")}
    for target in h3_inputs + anchor_inputs + forward_links:
        if target not in existing_stems:
            issues.append(build_issue("missing_target_note", f"{path.name}: hedef not bulunamadı: {target}"))

    return FileReport(
        path=str(path),
        kind="h4",
        title=title,
        ok=not issues,
        issues=issues,
        metrics={
            "h3_inputs": len(h3_inputs),
            "anchor_inputs": len(anchor_inputs),
            "forward_links": len(forward_links),
            "wikilink_count": len(parse_wikilinks(text)),
        },
    )


def h5_family_lookup() -> dict[str, Any]:
    return {h5_family_output_path(family).name: family for family in H5_FAMILIES}


def validate_h5_note(path: Path, knowledge_dir: Path = KNOWLEDGE_DIR) -> FileReport:
    text = read_text(path)
    title = extract_title(text)
    issues = validate_common_shape(
        path=path,
        text=text,
        required_sections=H5_REQUIRED_SECTIONS,
        required_tags=("#layer/hidden_5_metacognitive_control",),
    )

    if not H5_FILENAME_RE.match(path.name):
        issues.append(build_issue("filename_mismatch", f"{path.name}: hidden_5 dosya adı deseni geçersiz"))

    source_section = parse_h5_section(text, "## Besleyen H4 düğümleri")
    output_section = parse_h5_section(text, "## Yönettiği çıktı yolları")
    source_links = parse_wikilinks(source_section)
    output_links = parse_wikilinks(output_section)
    h4_inputs = [target for target in source_links if target.startswith("H4_")]
    control_anchors = [target for target in source_links if not target.startswith("H4_")]

    if len(h4_inputs) < 1:
        issues.append(build_issue("missing_h4_input", f"{path.name}: en az bir H4 girdi linki gerekli"))
    if len(output_links) < 1:
        issues.append(build_issue("insufficient_forward_links", f"{path.name}: en az 1 yönetilen çıktı linki gerekli"))

    existing_stems = {candidate.stem for candidate in knowledge_dir.glob("*.md")}
    for target in h4_inputs + control_anchors + output_links:
        if target not in existing_stems:
            issues.append(build_issue("missing_target_note", f"{path.name}: hedef not bulunamadı: {target}"))

    family = h5_family_lookup().get(path.name)
    if family is not None:
        try:
            verify_h5_note(path, family)
        except ValueError as exc:
            issues.append(build_issue("h5_spec_violation", str(exc)))

    return FileReport(
        path=str(path),
        kind="h5",
        title=title,
        ok=not issues,
        issues=issues,
        metrics={
            "h4_inputs": len(h4_inputs),
            "control_anchors": len(control_anchors),
            "managed_outputs": len(output_links),
            "wikilink_count": len(parse_wikilinks(text)),
        },
    )


def h6_family_lookup() -> dict[str, Any]:
    return {h6_family_output_path(family).name: family for family in H6_FAMILIES}


def validate_h6_note(path: Path, knowledge_dir: Path = KNOWLEDGE_DIR) -> FileReport:
    text = read_text(path)
    title = extract_title(text)
    issues = validate_common_shape(
        path=path,
        text=text,
        required_sections=H6_REQUIRED_SECTIONS,
        required_tags=("#layer/hidden_6_executive_orchestration",),
    )

    if not H6_FILENAME_RE.match(path.name):
        issues.append(build_issue("filename_mismatch", f"{path.name}: hidden_6 dosya adı deseni geçersiz"))

    source_section = parse_h6_section(text, "## Besleyen H5 düğümleri")
    output_section = parse_h6_section(text, "## Koordine ettiği çıktı yolları")
    source_links = parse_wikilinks(source_section)
    output_links = parse_wikilinks(output_section)
    h5_inputs = [target for target in source_links if target.startswith("H5_")]
    orchestration_anchors = [target for target in source_links if not target.startswith("H5_")]

    if len(h5_inputs) < 2:
        issues.append(build_issue("missing_h5_input", f"{path.name}: en az iki H5 girdi linki gerekli"))
    if len(output_links) < 1:
        issues.append(build_issue("insufficient_forward_links", f"{path.name}: en az 1 koordine edilen çıktı linki gerekli"))

    existing_stems = {candidate.stem for candidate in knowledge_dir.glob("*.md")}
    for target in h5_inputs + orchestration_anchors + output_links:
        if target not in existing_stems:
            issues.append(build_issue("missing_target_note", f"{path.name}: hedef not bulunamadı: {target}"))

    family = h6_family_lookup().get(path.name)
    if family is not None:
        try:
            verify_h6_note(path, family)
        except ValueError as exc:
            issues.append(build_issue("h6_spec_violation", str(exc)))

    return FileReport(
        path=str(path),
        kind="h6",
        title=title,
        ok=not issues,
        issues=issues,
        metrics={
            "h5_inputs": len(h5_inputs),
            "orchestration_anchors": len(orchestration_anchors),
            "coordinated_outputs": len(output_links),
            "wikilink_count": len(parse_wikilinks(text)),
        },
    )


def clean_list_field(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    return [clean_tag(value) for value in values if clean_tag(value)]


def h7_family_lookup() -> dict[str, Any]:
    return {h7_family_output_path(family).name: family for family in H7_FAMILIES}


def h8_family_lookup() -> dict[str, Any]:
    return {h8_family_output_path(family).name: family for family in H8_FAMILIES}


def h9_family_lookup() -> dict[str, Any]:
    return {h9_family_output_path(family).name: family for family in H9_FAMILIES}


def h10_family_lookup() -> dict[str, Any]:
    return {h10_family_output_path(family).name: family for family in H10_FAMILIES}


def h11_family_lookup() -> dict[str, Any]:
    return {h11_family_output_path(family).name: family for family in H11_FAMILIES}


def supported_episode_modes() -> set[str]:
    return {clean_tag(family.episode_mode) for family in H7_FAMILIES}


def supported_workspace_modes() -> set[str]:
    return {clean_tag(family.workspace_mode) for family in H8_FAMILIES}


def supported_package_modes() -> set[str]:
    return {clean_tag(family.package_mode) for family in H9_FAMILIES}


def supported_supervision_modes() -> set[str]:
    return {clean_tag(family.supervision_mode) for family in H10_FAMILIES}


def supported_reflection_modes() -> set[str]:
    return {clean_tag(family.reflection_mode) for family in H11_FAMILIES}


def validate_h7_note(path: Path, knowledge_dir: Path = KNOWLEDGE_DIR) -> FileReport:
    text = read_text(path)
    title = extract_title(text)
    issues = validate_common_shape(
        path=path,
        text=text,
        required_sections=H7_REQUIRED_SECTIONS,
        required_tags=("#layer/hidden_7_episodic_temporal_memory",),
    )

    if not H7_FILENAME_RE.match(path.name):
        issues.append(build_issue("filename_mismatch", f"{path.name}: hidden_7 dosya adı deseni geçersiz"))

    frontmatter = parse_yaml_frontmatter(text) if has_frontmatter(text) else {}
    episode_mode = clean_tag(frontmatter.get("episode_mode", ""))
    temporal_relations = clean_list_field(frontmatter.get("temporal_relations", []))
    primary_entities = clean_list_field(frontmatter.get("primary_entities", []))
    primary_events = clean_list_field(frontmatter.get("primary_events", []))

    binding_section = parse_h7_section(text, "## Entity-event bağlama stratejisi")
    source_section = parse_h7_section(text, "## Besleyen H6 düğümleri")
    output_section = parse_h7_section(text, "## Hafıza çıktıları")
    source_links = parse_wikilinks(source_section)
    output_links = parse_wikilinks(output_section)
    h6_inputs = [target for target in source_links if target.startswith("H6_")]
    episodic_anchors = [target for target in source_links if not target.startswith("H6_")]

    if not episode_mode or episode_mode not in supported_episode_modes():
        issues.append(build_issue("invalid_episode_mode", f"{path.name}: geçersiz episode_mode: {episode_mode or '<empty>'}"))
    if not temporal_relations:
        issues.append(build_issue("missing_temporal_relation", f"{path.name}: en az bir temporal relation gerekli"))
    if not primary_entities:
        issues.append(build_issue("missing_primary_entities", f"{path.name}: en az bir primary entity gerekli"))
    if not primary_events:
        issues.append(build_issue("missing_primary_events", f"{path.name}: en az bir primary event gerekli"))
    if not binding_section.strip():
        issues.append(build_issue("missing_entity_event_binding", f"{path.name}: entity-event bağlama stratejisi boş"))
    if len(h6_inputs) < 1:
        issues.append(build_issue("missing_h6_input", f"{path.name}: en az bir H6 girdi linki gerekli"))
    if len(output_links) < 1:
        issues.append(build_issue("insufficient_forward_links", f"{path.name}: en az 1 hafıza çıktısı linki gerekli"))

    existing_stems = {candidate.stem for candidate in knowledge_dir.glob("*.md")}
    for target in h6_inputs + episodic_anchors + output_links:
        if target not in existing_stems:
            issues.append(build_issue("missing_target_note", f"{path.name}: hedef not bulunamadı: {target}"))

    family = h7_family_lookup().get(path.name)
    if family is not None:
        try:
            verify_h7_note(path, family)
        except ValueError as exc:
            issues.append(build_issue("h7_spec_violation", str(exc)))

    return FileReport(
        path=str(path),
        kind="h7",
        title=title,
        ok=not issues,
        issues=issues,
        metrics={
            "h6_inputs": len(h6_inputs),
            "episodic_anchors": len(episodic_anchors),
            "temporal_relation_count": len(temporal_relations),
            "entity_count": len(primary_entities),
            "event_count": len(primary_events),
            "memory_outputs": len(output_links),
            "wikilink_count": len(parse_wikilinks(text)),
        },
    )


def validate_h8_note(path: Path, knowledge_dir: Path = KNOWLEDGE_DIR) -> FileReport:
    text = read_text(path)
    title = extract_title(text)
    issues = validate_common_shape(
        path=path,
        text=text,
        required_sections=H8_REQUIRED_SECTIONS,
        required_tags=("#layer/hidden_8_decision_assembly",),
    )

    if not H8_FILENAME_RE.match(path.name):
        issues.append(build_issue("filename_mismatch", f"{path.name}: hidden_8 dosya adı deseni geçersiz"))

    frontmatter = parse_yaml_frontmatter(text) if has_frontmatter(text) else {}
    workspace_mode = clean_tag(frontmatter.get("workspace_mode", ""))
    dominant_thoughtseed = clean_tag(frontmatter.get("dominant_thoughtseed", ""))
    candidate_policies = clean_list_field(frontmatter.get("candidate_policies", []))
    broadcast_targets = clean_list_field(frontmatter.get("broadcast_targets", []))

    strategy_section = parse_h8_section(text, "## Policy broadcast stratejisi")
    commitment_section = parse_h8_section(text, "## Commitment kuralları")
    source_section = parse_h8_section(text, "## Besleyen H7 düğümleri")
    output_section = parse_h8_section(text, "## Yayınlanan çıktı yolları")
    source_links = parse_wikilinks(source_section)
    output_links = parse_wikilinks(output_section)
    h7_inputs = [target for target in source_links if target.startswith("H7_")]
    workspace_anchors = [target for target in source_links if not target.startswith("H7_")]

    if not workspace_mode or workspace_mode not in supported_workspace_modes():
        issues.append(build_issue("invalid_workspace_mode", f"{path.name}: geçersiz workspace_mode: {workspace_mode or '<empty>'}"))
    if not dominant_thoughtseed:
        issues.append(build_issue("missing_dominant_thoughtseed", f"{path.name}: dominant_thoughtseed boş"))
    if not candidate_policies:
        issues.append(build_issue("missing_candidate_policy", f"{path.name}: en az bir candidate policy gerekli"))
    if not broadcast_targets:
        issues.append(build_issue("missing_broadcast_target", f"{path.name}: en az bir broadcast target gerekli"))
    if not strategy_section.strip():
        issues.append(build_issue("missing_policy_broadcast_strategy", f"{path.name}: policy broadcast stratejisi boş"))
    if not commitment_section.strip():
        issues.append(build_issue("missing_commitment_rule", f"{path.name}: commitment kuralları boş"))
    if len(h7_inputs) < 1:
        issues.append(build_issue("missing_h7_input", f"{path.name}: en az bir H7 girdi linki gerekli"))
    if len(output_links) < 1:
        issues.append(build_issue("insufficient_forward_links", f"{path.name}: en az 1 yayınlanan çıktı linki gerekli"))

    existing_stems = {candidate.stem for candidate in knowledge_dir.glob("*.md")}
    for target in h7_inputs + workspace_anchors + broadcast_targets + output_links:
        if target not in existing_stems:
            issues.append(build_issue("missing_target_note", f"{path.name}: hedef not bulunamadı: {target}"))

    family = h8_family_lookup().get(path.name)
    if family is not None:
        try:
            verify_h8_note(path, family)
        except ValueError as exc:
            issues.append(build_issue("h8_spec_violation", str(exc)))

    return FileReport(
        path=str(path),
        kind="h8",
        title=title,
        ok=not issues,
        issues=issues,
        metrics={
            "h7_inputs": len(h7_inputs),
            "workspace_anchors": len(workspace_anchors),
            "candidate_policy_count": len(candidate_policies),
            "broadcast_target_count": len(broadcast_targets),
            "downstream_output_count": len(output_links),
            "wikilink_count": len(parse_wikilinks(text)),
        },
    )


def validate_h9_note(path: Path, knowledge_dir: Path = KNOWLEDGE_DIR) -> FileReport:
    text = read_text(path)
    title = extract_title(text)
    issues = validate_common_shape(
        path=path,
        text=text,
        required_sections=H9_REQUIRED_SECTIONS,
        required_tags=("#layer/hidden_9_execution_packaging",),
    )

    if not H9_FILENAME_RE.match(path.name):
        issues.append(build_issue("filename_mismatch", f"{path.name}: hidden_9 dosya adı deseni geçersiz"))

    frontmatter = parse_yaml_frontmatter(text) if has_frontmatter(text) else {}
    package_mode = clean_tag(frontmatter.get("package_mode", ""))
    source_policy = clean_tag(frontmatter.get("source_policy", ""))
    delivery_surfaces = clean_list_field(frontmatter.get("delivery_surfaces", []))
    package_contracts = clean_list_field(frontmatter.get("package_contracts", []))

    mapping_section = parse_h9_section(text, "## Source policy eşlemesi")
    contract_section = parse_h9_section(text, "## Delivery surface sözleşmeleri")
    readiness_section = parse_h9_section(text, "## Readiness ve commit koşulları")
    source_section = parse_h9_section(text, "## Besleyen H8 düğümleri")
    output_section = parse_h9_section(text, "## Paketlenen çıktı yolları")
    source_links = parse_wikilinks(source_section)
    output_links = parse_wikilinks(output_section)
    h8_inputs = [target for target in source_links if target.startswith("H8_")]
    packaging_anchors = [target for target in source_links if not target.startswith("H8_")]

    if not package_mode or package_mode not in supported_package_modes():
        issues.append(build_issue("invalid_package_mode", f"{path.name}: geçersiz package_mode: {package_mode or '<empty>'}"))
    if not source_policy:
        issues.append(build_issue("missing_source_policy", f"{path.name}: source_policy boş"))
    if not delivery_surfaces:
        issues.append(build_issue("missing_delivery_surface", f"{path.name}: en az bir delivery surface gerekli"))
    if not package_contracts:
        issues.append(build_issue("missing_package_contract", f"{path.name}: en az bir package contract gerekli"))
    if not mapping_section.strip():
        issues.append(build_issue("missing_source_policy_mapping", f"{path.name}: source policy eşlemesi boş"))
    if not contract_section.strip():
        issues.append(
            build_issue("missing_delivery_surface_contract", f"{path.name}: delivery surface sözleşmeleri boş")
        )
    if not readiness_section.strip():
        issues.append(build_issue("missing_readiness_rule", f"{path.name}: readiness ve commit koşulları boş"))
    if len(h8_inputs) < 1:
        issues.append(build_issue("missing_h8_input", f"{path.name}: en az bir H8 girdi linki gerekli"))
    if len(output_links) < 1:
        issues.append(build_issue("insufficient_forward_links", f"{path.name}: en az 1 paketlenen çıktı linki gerekli"))

    existing_stems = {candidate.stem for candidate in knowledge_dir.glob("*.md")}
    for target in h8_inputs + packaging_anchors + delivery_surfaces + output_links:
        if target not in existing_stems:
            issues.append(build_issue("missing_target_note", f"{path.name}: hedef not bulunamadı: {target}"))

    family = h9_family_lookup().get(path.name)
    if family is not None:
        try:
            verify_h9_note(path, family)
        except ValueError as exc:
            issues.append(build_issue("h9_spec_violation", str(exc)))

    return FileReport(
        path=str(path),
        kind="h9",
        title=title,
        ok=not issues,
        issues=issues,
        metrics={
            "h8_inputs": len(h8_inputs),
            "packaging_anchors": len(packaging_anchors),
            "delivery_surface_count": len(delivery_surfaces),
            "package_contract_count": len(package_contracts),
            "packaged_output_count": len(output_links),
            "wikilink_count": len(parse_wikilinks(text)),
        },
    )


def validate_h10_note(path: Path, knowledge_dir: Path = KNOWLEDGE_DIR) -> FileReport:
    text = read_text(path)
    title = extract_title(text)
    issues = validate_common_shape(
        path=path,
        text=text,
        required_sections=H10_REQUIRED_SECTIONS,
        required_tags=("#layer/hidden_10_strategic_supervision",),
    )

    if not H10_FILENAME_RE.match(path.name):
        issues.append(build_issue("filename_mismatch", f"{path.name}: hidden_10 dosya adı deseni geçersiz"))

    frontmatter = parse_yaml_frontmatter(text) if has_frontmatter(text) else {}
    supervision_mode = clean_tag(frontmatter.get("supervision_mode", ""))
    governing_signal = clean_tag(frontmatter.get("governing_signal", ""))
    oversight_surfaces = clean_list_field(frontmatter.get("oversight_surfaces", []))
    supervision_contracts = clean_list_field(frontmatter.get("supervision_contracts", []))

    mapping_section = parse_h10_section(text, "## Governing signal eşlemesi")
    contract_section = parse_h10_section(text, "## Oversight surface sözleşmeleri")
    escalation_section = parse_h10_section(text, "## Escalation ve rollback kuralları")
    source_section = parse_h10_section(text, "## Besleyen H9 düğümleri")
    output_section = parse_h10_section(text, "## Denetlenen çıktı yolları")
    source_links = parse_wikilinks(source_section)
    output_links = parse_wikilinks(output_section)
    h9_inputs = [target for target in source_links if target.startswith("H9_")]
    supervision_anchors = [target for target in source_links if not target.startswith("H9_")]

    if not supervision_mode or supervision_mode not in supported_supervision_modes():
        issues.append(
            build_issue("invalid_supervision_mode", f"{path.name}: geçersiz supervision_mode: {supervision_mode or '<empty>'}")
        )
    if not governing_signal:
        issues.append(build_issue("missing_governing_signal", f"{path.name}: governing_signal boş"))
    if not oversight_surfaces:
        issues.append(build_issue("missing_oversight_surface", f"{path.name}: en az bir oversight surface gerekli"))
    if not supervision_contracts:
        issues.append(
            build_issue("missing_supervision_contract", f"{path.name}: en az bir supervision contract gerekli")
        )
    if not mapping_section.strip():
        issues.append(
            build_issue("missing_governing_signal_mapping", f"{path.name}: governing signal eşlemesi boş")
        )
    if not contract_section.strip():
        issues.append(
            build_issue("missing_oversight_surface_contract", f"{path.name}: oversight surface sözleşmeleri boş")
        )
    if not escalation_section.strip():
        issues.append(build_issue("missing_escalation_rule", f"{path.name}: escalation ve rollback kuralları boş"))
    if len(h9_inputs) < 1:
        issues.append(build_issue("missing_h9_input", f"{path.name}: en az bir H9 girdi linki gerekli"))
    if len(output_links) < 1:
        issues.append(build_issue("insufficient_forward_links", f"{path.name}: en az 1 denetlenen çıktı linki gerekli"))

    existing_stems = {candidate.stem for candidate in knowledge_dir.glob("*.md")}
    for target in h9_inputs + supervision_anchors + oversight_surfaces + output_links:
        if target not in existing_stems:
            issues.append(build_issue("missing_target_note", f"{path.name}: hedef not bulunamadı: {target}"))

    family = h10_family_lookup().get(path.name)
    if family is not None:
        try:
            verify_h10_note(path, family)
        except ValueError as exc:
            issues.append(build_issue("h10_spec_violation", str(exc)))

    return FileReport(
        path=str(path),
        kind="h10",
        title=title,
        ok=not issues,
        issues=issues,
        metrics={
            "h9_inputs": len(h9_inputs),
            "supervision_anchors": len(supervision_anchors),
            "oversight_surface_count": len(oversight_surfaces),
            "supervision_contract_count": len(supervision_contracts),
            "supervised_output_count": len(output_links),
            "wikilink_count": len(parse_wikilinks(text)),
        },
    )


def validate_h11_note(path: Path, knowledge_dir: Path = KNOWLEDGE_DIR) -> FileReport:
    text = read_text(path)
    title = extract_title(text)
    issues = validate_common_shape(
        path=path,
        text=text,
        required_sections=H11_REQUIRED_SECTIONS,
        required_tags=("#layer/hidden_11_reflection_audit",),
    )

    if not H11_FILENAME_RE.match(path.name):
        issues.append(build_issue("filename_mismatch", f"{path.name}: hidden_11 dosya adı deseni geçersiz"))

    frontmatter = parse_yaml_frontmatter(text) if has_frontmatter(text) else {}
    reflection_mode = clean_tag(frontmatter.get("reflection_mode", ""))
    audit_signal = clean_tag(frontmatter.get("audit_signal", ""))
    audit_surfaces = clean_list_field(frontmatter.get("audit_surfaces", []))
    audit_contracts = clean_list_field(frontmatter.get("audit_contracts", []))

    mapping_section = parse_h11_section(text, "## Audit signal eşlemesi")
    contract_section = parse_h11_section(text, "## Evidence surface sözleşmeleri")
    proof_section = parse_h11_section(text, "## İspat ve tutarlılık kuralları")
    source_section = parse_h11_section(text, "## Besleyen H10 düğümleri")
    output_section = parse_h11_section(text, "## Üretilen audit çıktıları")
    source_links = parse_wikilinks(source_section)
    output_links = parse_wikilinks(output_section)
    h10_inputs = [target for target in source_links if target.startswith("H10_")]
    audit_anchors = [target for target in source_links if not target.startswith("H10_")]

    if not reflection_mode or reflection_mode not in supported_reflection_modes():
        issues.append(
            build_issue(
                "invalid_reflection_mode",
                f"{path.name}: geçersiz reflection_mode: {reflection_mode or '<empty>'}",
            )
        )
    if not audit_signal:
        issues.append(build_issue("missing_audit_signal", f"{path.name}: audit_signal boş"))
    if not audit_surfaces:
        issues.append(build_issue("missing_audit_surface", f"{path.name}: en az bir audit surface gerekli"))
    if not audit_contracts:
        issues.append(build_issue("missing_audit_contract", f"{path.name}: en az bir audit contract gerekli"))
    if not mapping_section.strip():
        issues.append(build_issue("missing_audit_signal_mapping", f"{path.name}: audit signal eşlemesi boş"))
    if not contract_section.strip():
        issues.append(build_issue("missing_evidence_surface_contract", f"{path.name}: evidence surface sözleşmeleri boş"))
    if not proof_section.strip():
        issues.append(build_issue("missing_proof_rule", f"{path.name}: ispat ve tutarlılık kuralları boş"))
    if len(h10_inputs) < 1:
        issues.append(build_issue("missing_h10_input", f"{path.name}: en az bir H10 girdi linki gerekli"))
    if len(output_links) < 1:
        issues.append(build_issue("insufficient_forward_links", f"{path.name}: en az 1 audit çıktı linki gerekli"))

    existing_stems = {candidate.stem for candidate in knowledge_dir.glob("*.md")}
    for target in h10_inputs + audit_anchors + audit_surfaces + output_links:
        if target not in existing_stems:
            issues.append(build_issue("missing_target_note", f"{path.name}: hedef not bulunamadı: {target}"))

    family = h11_family_lookup().get(path.name)
    if family is not None:
        try:
            verify_h11_note(path, family)
        except ValueError as exc:
            issues.append(build_issue("h11_spec_violation", str(exc)))

    return FileReport(
        path=str(path),
        kind="h11",
        title=title,
        ok=not issues,
        issues=issues,
        metrics={
            "h10_inputs": len(h10_inputs),
            "audit_anchors": len(audit_anchors),
            "audit_surfaces": len(audit_surfaces),
            "audit_contracts": len(audit_contracts),
            "audit_outputs": len(output_links),
            "wikilink_count": len(parse_wikilinks(text)),
        },
    )


def validate_index_note(path: Path) -> FileReport:
    text = read_text(path)
    title = extract_title(text)
    issues = validate_common_shape(
        path=path,
        text=text,
        required_sections=INDEX_REQUIRED_SECTIONS,
        required_tags=(),
    )
    return FileReport(
        path=str(path),
        kind="index",
        title=title,
        ok=not issues,
        issues=issues,
        metrics={"wikilink_count": len(parse_wikilinks(text))},
    )


def summarize_kind(kind: str, reports: list[FileReport]) -> dict[str, Any]:
    issue_count = sum(len(report.issues) for report in reports)
    return {
        "kind": kind,
        "file_count": len(reports),
        "ok_count": sum(1 for report in reports if report.ok),
        "issue_count": issue_count,
    }


def build_graph_metrics(file_reports: list[FileReport]) -> dict[str, Any]:
    total = len(file_reports)
    compliant = sum(
        1
        for report in file_reports
        if not any(issue.code in LINK_COMPLIANCE_ISSUE_CODES for issue in report.issues)
    )
    return {
        "node_count_by_kind": {
            "raw": sum(1 for report in file_reports if report.kind == "raw"),
            "synthesis": sum(1 for report in file_reports if report.kind == "synthesis"),
            "h4": sum(1 for report in file_reports if report.kind == "h4"),
            "h5": sum(1 for report in file_reports if report.kind == "h5"),
            "h6": sum(1 for report in file_reports if report.kind == "h6"),
            "h7": sum(1 for report in file_reports if report.kind == "h7"),
            "h8": sum(1 for report in file_reports if report.kind == "h8"),
            "h9": sum(1 for report in file_reports if report.kind == "h9"),
            "h10": sum(1 for report in file_reports if report.kind == "h10"),
            "index": sum(1 for report in file_reports if report.kind == "index"),
        },
        "forward_link_compliance_ratio": 0.0 if total == 0 else round(compliant / total, 4),
        "forbidden_reference_count": sum(
            1
            for report in file_reports
            for issue in report.issues
            if issue.code == "forbidden_node_reference"
        ),
        "total_wikilinks": sum(int(report.metrics.get("wikilink_count", 0)) for report in file_reports),
    }


def load_previous_report(report_path: Path) -> dict[str, Any] | None:
    if not report_path.exists():
        return None
    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def build_delta_entry(before: int | float, after: int | float) -> dict[str, int | float]:
    delta = round(after - before, 4) if isinstance(before, float) or isinstance(after, float) else after - before
    return {
        "before": before,
        "after": after,
        "delta": delta,
    }


def build_report_delta(current_report: dict[str, Any], previous_report: dict[str, Any]) -> dict[str, Any]:
    summary_before = previous_report.get("summary", {})
    summary_after = current_report.get("summary", {})
    kinds_before = previous_report.get("kinds", {})
    kinds_after = current_report.get("kinds", {})
    graph_before = previous_report.get("graph_metrics", {})
    graph_after = current_report.get("graph_metrics", {})
    nodes_before = graph_before.get("node_count_by_kind", {})
    nodes_after = graph_after.get("node_count_by_kind", {})

    return {
        "previous_generated_at": previous_report.get("generated_at"),
        "summary": {
            "files_scanned": build_delta_entry(
                int(summary_before.get("files_scanned", 0)),
                int(summary_after.get("files_scanned", 0)),
            ),
            "files_with_issues": build_delta_entry(
                int(summary_before.get("files_with_issues", 0)),
                int(summary_after.get("files_with_issues", 0)),
            ),
            "issue_count": build_delta_entry(
                int(summary_before.get("issue_count", 0)),
                int(summary_after.get("issue_count", 0)),
            ),
        },
        "kinds": {
            kind: {
                "file_count": build_delta_entry(
                    int(kinds_before.get(kind, {}).get("file_count", 0)),
                    int(kinds_after.get(kind, {}).get("file_count", 0)),
                ),
                "ok_count": build_delta_entry(
                    int(kinds_before.get(kind, {}).get("ok_count", 0)),
                    int(kinds_after.get(kind, {}).get("ok_count", 0)),
                ),
                "issue_count": build_delta_entry(
                    int(kinds_before.get(kind, {}).get("issue_count", 0)),
                    int(kinds_after.get(kind, {}).get("issue_count", 0)),
                ),
            }
            for kind in REPORT_KIND_ORDER
        },
        "graph_metrics": {
            "node_count_by_kind": {
                kind: build_delta_entry(
                    int(nodes_before.get(kind, 0)),
                    int(nodes_after.get(kind, 0)),
                )
                for kind in REPORT_KIND_ORDER
            },
            "forward_link_compliance_ratio": build_delta_entry(
                float(graph_before.get("forward_link_compliance_ratio", 0.0)),
                float(graph_after.get("forward_link_compliance_ratio", 0.0)),
            ),
            "forbidden_reference_count": build_delta_entry(
                int(graph_before.get("forbidden_reference_count", 0)),
                int(graph_after.get("forbidden_reference_count", 0)),
            ),
            "total_wikilinks": build_delta_entry(
                int(graph_before.get("total_wikilinks", 0)),
                int(graph_after.get("total_wikilinks", 0)),
            ),
        },
    }


def build_report(
    scope: str = "all",
    knowledge_dir: Path = KNOWLEDGE_DIR,
    fixes: dict[str, Any] | None = None,
    previous_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    grouped_paths = collect_paths(scope, knowledge_dir)
    reports: list[FileReport] = []

    for kind, paths in grouped_paths.items():
        for path in paths:
            if kind == "raw":
                reports.append(validate_raw_note(path, knowledge_dir=knowledge_dir))
            elif kind == "synthesis":
                reports.append(validate_synthesis_note(path, knowledge_dir=knowledge_dir))
            elif kind == "h4":
                reports.append(validate_h4_note(path, knowledge_dir=knowledge_dir))
            elif kind == "h5":
                reports.append(validate_h5_note(path, knowledge_dir=knowledge_dir))
            elif kind == "h6":
                reports.append(validate_h6_note(path, knowledge_dir=knowledge_dir))
            elif kind == "h7":
                reports.append(validate_h7_note(path, knowledge_dir=knowledge_dir))
            elif kind == "h8":
                reports.append(validate_h8_note(path, knowledge_dir=knowledge_dir))
            elif kind == "h9":
                reports.append(validate_h9_note(path, knowledge_dir=knowledge_dir))
            elif kind == "h10":
                reports.append(validate_h10_note(path, knowledge_dir=knowledge_dir))
            elif kind == "h11":
                reports.append(validate_h11_note(path, knowledge_dir=knowledge_dir))
            else:
                reports.append(validate_index_note(path))

    grouped_reports = {
        kind: [report for report in reports if report.kind == kind]
        for kind in REPORT_KIND_ORDER
    }
    issue_count = sum(len(report.issues) for report in reports)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": scope,
        "knowledge_dir": str(knowledge_dir),
        "summary": {
            "files_scanned": len(reports),
            "files_with_issues": sum(1 for report in reports if not report.ok),
            "issue_count": issue_count,
            "status": "pass" if issue_count == 0 else "fail",
        },
        "kinds": {
            kind: summarize_kind(kind, grouped_reports[kind])
            for kind in REPORT_KIND_ORDER
        },
        "graph_metrics": build_graph_metrics(reports),
        "remediation_map": build_remediation_map(reports),
        "files": [
            {
                **asdict(report),
                "issues": [asdict(issue) for issue in report.issues],
            }
            for report in reports
        ],
    }
    if fixes is not None:
        report["fixes"] = fixes
    if previous_report is not None:
        report["delta"] = build_report_delta(report, previous_report)
    return report


def remediation_guidance_for_code(code: str) -> dict[str, Any]:
    guidance = REMEDIATION_GUIDANCE_BY_CODE.get(code)
    if guidance is not None:
        return guidance
    return {
        "repair_class": "general_manual_review",
        "summary": "Bu issue kodu için manuel inceleme gerekir.",
        "recommended_actions": [
            "Issue mesajını incele.",
            "İlgili note ailesi şemasına göre elle düzeltme uygula.",
        ],
    }


def build_remediation_map(file_reports: list[FileReport]) -> dict[str, Any]:
    issue_buckets: dict[str, dict[str, Any]] = {}
    for report in file_reports:
        for issue in report.issues:
            bucket = issue_buckets.setdefault(
                issue.code,
                {
                    "issue_code": issue.code,
                    "occurrence_count": 0,
                    "affected_files": set(),
                    "sample_messages": [],
                },
            )
            bucket["occurrence_count"] += 1
            bucket["affected_files"].add(report.path)
            if issue.message not in bucket["sample_messages"] and len(bucket["sample_messages"]) < 3:
                bucket["sample_messages"].append(issue.message)

    entries: list[dict[str, Any]] = []
    for issue_code in sorted(issue_buckets):
        bucket = issue_buckets[issue_code]
        guidance = remediation_guidance_for_code(issue_code)
        affected_files = sorted(bucket["affected_files"])
        entries.append(
            {
                "issue_code": issue_code,
                "repair_class": guidance["repair_class"],
                "summary": guidance["summary"],
                "recommended_actions": list(guidance["recommended_actions"]),
                "occurrence_count": bucket["occurrence_count"],
                "affected_file_count": len(affected_files),
                "affected_files": affected_files,
                "sample_messages": bucket["sample_messages"],
            }
        )

    return {
        "issue_code_count": len(entries),
        "total_affected_files": len({path for entry in entries for path in entry["affected_files"]}),
        "entries": entries,
    }


def default_report_output_path(output_format: str) -> Path:
    suffix = "json" if output_format == "json" else "txt"
    return REPORTS_DIR / f"{REPORT_FILENAME_STEM}.{suffix}"


def quote_unquoted_frontmatter_tags(text: str) -> tuple[str, bool]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text, False

    updated_lines = list(lines)
    in_frontmatter = True
    in_tags = False
    changed = False

    for index in range(1, len(updated_lines)):
        line = updated_lines[index]
        stripped = line.strip()
        if stripped == "---":
            break
        if not stripped:
            continue
        if not line.startswith("  - "):
            in_tags = stripped.startswith("tags:")
            continue
        if not in_frontmatter or not in_tags:
            continue

        value = line.split("  - ", 1)[1].strip()
        if value and value.startswith("#") and not (
            (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'"))
        ):
            updated_lines[index] = f'  - "{value}"'
            changed = True

    updated_text = "\n".join(updated_lines)
    if text.endswith("\n"):
        updated_text += "\n"
    return updated_text, changed


def missing_section_blocks(text: str, kind: str) -> list[str]:
    required_sections = REQUIRED_SECTIONS_BY_KIND[kind]
    section_templates = SECTION_FIX_CONTENT[kind]
    blocks: list[str] = []
    for section in required_sections:
        if section not in text:
            blocks.append(f"{section}\n\n{section_templates[section]}")
    return blocks


def apply_safe_fixes(text: str, kind: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    updated = text

    updated, tags_changed = quote_unquoted_frontmatter_tags(updated)
    if tags_changed:
        changes.append("quote_tags")

    missing_blocks = missing_section_blocks(updated, kind)
    if missing_blocks:
        updated = updated.rstrip() + "\n\n" + "\n\n".join(missing_blocks) + "\n"
        changes.append("add_missing_sections")

    return updated, changes


def apply_safe_fixes_to_paths(grouped_paths: dict[str, list[Path]]) -> dict[str, Any]:
    changed_files: list[dict[str, Any]] = []
    for kind, paths in grouped_paths.items():
        if kind not in REQUIRED_SECTIONS_BY_KIND or kind in {"h7", "h8", "h9", "h10", "h11"}:
            continue
        for path in paths:
            original_text = read_text(path)
            fixed_text, changes = apply_safe_fixes(original_text, kind=kind)
            if not changes or fixed_text == original_text:
                continue
            path.write_text(fixed_text, encoding="utf-8")
            changed_files.append({"path": str(path), "kind": kind, "changes": changes})

    return {
        "enabled": True,
        "files_changed": len(changed_files),
        "changes_applied": sum(len(item["changes"]) for item in changed_files),
        "changed_files": changed_files,
    }


def render_text_report(report: dict[str, Any]) -> str:
    lines = [
        "Brain Growth Quality Report",
        f"Scope: {report['scope']}",
        f"Knowledge dir: {report['knowledge_dir']}",
        f"Status: {report['summary']['status']}",
        f"Files scanned: {report['summary']['files_scanned']}",
        f"Files with issues: {report['summary']['files_with_issues']}",
        f"Issue count: {report['summary']['issue_count']}",
        "",
        "Kinds:",
    ]

    for kind in REPORT_KIND_ORDER:
        summary = report.get("kinds", {}).get(
            kind,
            {"kind": kind, "file_count": 0, "ok_count": 0, "issue_count": 0},
        )
        lines.append(
            f"- {kind}: files={summary['file_count']}, ok={summary['ok_count']}, issues={summary['issue_count']}"
        )

    graph_metrics = report.get("graph_metrics")
    if graph_metrics:
        lines.extend(
            [
                "",
                "Graph metrics:",
                f"- node_count_by_kind: {graph_metrics.get('node_count_by_kind', {})}",
                f"- forward_link_compliance_ratio: {graph_metrics.get('forward_link_compliance_ratio', 0.0)}",
                f"- forbidden_reference_count: {graph_metrics.get('forbidden_reference_count', 0)}",
                f"- total_wikilinks: {graph_metrics.get('total_wikilinks', 0)}",
            ]
        )

    remediation_map = report.get("remediation_map", {})
    lines.extend(["", "Remediation hints:"])
    if remediation_map.get("entries"):
        for entry in remediation_map["entries"]:
            actions = "; ".join(entry.get("recommended_actions", []))
            lines.append(
                f"- {entry['issue_code']}: repair_class={entry['repair_class']}, "
                f"occurrences={entry['occurrence_count']}, affected_files={entry['affected_file_count']}"
            )
            lines.append(f"  - summary: {entry['summary']}")
            if actions:
                lines.append(f"  - actions: {actions}")
    else:
        lines.append("- none")

    delta = report.get("delta")
    if delta:
        lines.extend(
            [
                "",
                "Delta vs previous report:",
                f"- previous_generated_at: {delta.get('previous_generated_at')}",
            ]
        )
        for field in ("files_scanned", "files_with_issues", "issue_count"):
            summary_delta = delta.get("summary", {}).get(field, {"before": 0, "after": 0, "delta": 0})
            lines.append(
                f"- summary.{field}: {summary_delta['before']} -> {summary_delta['after']} (delta {summary_delta['delta']:+})"
            )
        for kind in REPORT_KIND_ORDER:
            kind_delta = delta.get("kinds", {}).get(kind, {})
            for field in ("file_count", "ok_count", "issue_count"):
                value = kind_delta.get(field, {"before": 0, "after": 0, "delta": 0})
                lines.append(
                    f"- kinds.{kind}.{field}: {value['before']} -> {value['after']} (delta {value['delta']:+})"
                )
        graph_delta = delta.get("graph_metrics", {})
        ratio_delta = graph_delta.get("forward_link_compliance_ratio", {"before": 0.0, "after": 0.0, "delta": 0.0})
        lines.append(
            "- graph_metrics.forward_link_compliance_ratio: "
            f"{ratio_delta['before']} -> {ratio_delta['after']} (delta {ratio_delta['delta']:+})"
        )
        forbidden_delta = graph_delta.get("forbidden_reference_count", {"before": 0, "after": 0, "delta": 0})
        lines.append(
            "- graph_metrics.forbidden_reference_count: "
            f"{forbidden_delta['before']} -> {forbidden_delta['after']} (delta {forbidden_delta['delta']:+})"
        )
        wikilink_delta = graph_delta.get("total_wikilinks", {"before": 0, "after": 0, "delta": 0})
        lines.append(
            f"- graph_metrics.total_wikilinks: {wikilink_delta['before']} -> {wikilink_delta['after']} (delta {wikilink_delta['delta']:+})"
        )
        for kind in REPORT_KIND_ORDER:
            value = graph_delta.get("node_count_by_kind", {}).get(kind, {"before": 0, "after": 0, "delta": 0})
            lines.append(
                f"- graph_metrics.node_count_by_kind.{kind}: {value['before']} -> {value['after']} (delta {value['delta']:+})"
            )

    fixes = report.get("fixes")
    if fixes:
        lines.extend(
            [
                "",
                "Fixes:",
                f"- enabled: {fixes.get('enabled', False)}",
                f"- files_changed: {fixes.get('files_changed', 0)}",
                f"- changes_applied: {fixes.get('changes_applied', 0)}",
            ]
        )
        for item in fixes.get("changed_files", []):
            lines.append(
                f"- {Path(item['path']).name}: kind={item['kind']}, changes={', '.join(item['changes'])}"
            )

    problematic = [item for item in report["files"] if not item["ok"]]
    if problematic:
        lines.extend(["", "Issues:"])
        for item in problematic:
            lines.append(f"- {Path(item['path']).name}")
            for issue in item["issues"]:
                lines.append(f"  - [{issue['code']}] {issue['message']}")

    return "\n".join(lines)


def write_report_output(report: dict[str, Any], output_format: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_format == "json":
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return
    output_path.write_text(render_text_report(report) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Phase 1/2 brain-growth notes and emit reports.")
    parser.add_argument(
        "--scope",
        choices=("raw", "synthesis", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "h11", "index", "all"),
        default="all",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", type=Path, help="Optional output path for report persistence")
    parser.add_argument("--fix", action="store_true", help="Apply safe structural fixes before validation")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    grouped_paths = collect_paths(args.scope, KNOWLEDGE_DIR)
    fixes = apply_safe_fixes_to_paths(grouped_paths) if args.fix else None
    previous_report = load_previous_report(default_report_output_path("json"))
    report = build_report(
        scope=args.scope,
        knowledge_dir=KNOWLEDGE_DIR,
        fixes=fixes,
        previous_report=previous_report,
    )

    if args.output:
        write_report_output(report, args.format, args.output)

    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text_report(report))

    return 0 if report["summary"]["issue_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
