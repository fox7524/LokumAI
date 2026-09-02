# Wave 11 Hidden 11 Reflection & Audit Design

**Goal:** H10 `strategic_supervision` katmanından çıkan yönetişim kararlarını *post-hoc* (sonradan) açıklanabilir, izlenebilir ve doğrulanabilir hale getiren resmi `hidden_11_reflection_audit` katmanını eklemek.

**Why now:** H9 ile execution paketleri, H10 ile stratejik supervision tamamlandı. Şu an zincirde eksik olan şey “bu karar / bu paket / bu rollback neden oldu?” sorusuna **kanıt zinciri** (trace/provenance) üzerinden deterministik cevap verebilen bir audit katmanı.

## Scope

- Yeni semantic katman: `hidden_11_reflection_audit`
- Gerçek `H11_*.md` düğümleri
- `brain_growth` toolchain içinde:
  - discovery (`common.py`)
  - builder (`h11_builder.py`)
  - validator (`quality_validator.py`) desteği
  - projection (`layered_projection.py`) desteği
- H10 -> H11 transition görünürlüğü
- Yeni türetilmiş projection grafı: `reflection_audit_graph`

Scope dışı:

- Gerçek “legal-grade” imzalama / kriptografik attestation (şimdilik semantic model)
- Runtime executor’ın gerçek aksiyon çalıştırması (bu başka bir katman/kapasite modeli)

## H11 semantic model

### Katman adı (tag)

- `#layer/hidden_11_reflection_audit`

### Zorunlu frontmatter alanları

- `reflection_mode`
- `audit_signal`
- `audit_surfaces`
- `audit_contracts`

### Zorunlu tag seti

- `#layer/hidden_11_reflection_audit`
- `#audit/trace_contract`
- `#audit/evidence_surface`
- `#audit/provenance_binding`

### Zorunlu section başlıkları

- `## Yansıma amacı`
- `## Audit signal eşlemesi`
- `## Evidence surface sözleşmeleri`
- `## İspat ve tutarlılık kuralları`
- `## Besleyen H10 düğümleri`
- `## Üretilen audit çıktıları`

## Proposed H11 families

- `H11_Trace_Provenance_Attestation.md`
  - H10 supervision route’larının provenance izini sabitler.
- `H11_Outcome_Regression_Postmortem.md`
  - H10 outcome review sapmalarını postmortem raporlar.
- `H11_Rollback_Decision_Audit.md`
  - rollback/escalation kararlarını gerekçelendiren audit log üretir.
- `H11_Failsafe_Cost_Accounting.md`
  - failsafe paketlerinin kaynak/lifecycle maliyetini muhasebeleştirir.

## Projection behavior

`LAYER_ORDER` zincirine `hidden_11` eklenir. H10 -> H11 edge’leri ve H11 -> index edge’leri, normal wikilink kurallarıyla edge graph’a yansır.

Yeni türetilmiş graph: `reflection_audit_graph`

- `signal_nodes`: `audit_signal` temelli signal düğümleri
- `audit_nodes`: H11 notları
- `surface_nodes`: audit_surfaces düğümleri
- `signal_edges`: `signal -> audit` (attests)
- `surface_edges`: `audit -> surface` (audits)

