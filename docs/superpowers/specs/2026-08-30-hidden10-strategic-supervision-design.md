# Wave 10 Hidden 10 Strategic Supervision Design

**Goal:** H9 `execution_packaging` katmanından çıkan delivery-ready paketleri, stratejik oversight, rollback/escalation ve kaynak yönetişimi açısından denetleyen resmi `hidden_10_strategic_supervision` katmanını eklemek.

**Why now:** H9 ile policy artık execution yüzeylerine bağlanabilir paketlere dönüştü. Ama sistem hâlâ “bu paket ne zaman yükseltilmeli, geri alınmalı, hangi stratejik yüzeyler devreye girmeli, uzun vadeli planlayıcı ile kaynak ayırıcı bunu nasıl üstten görmeli” sorusunu first-class modellemiyor. H10 bu üst denetim katmanını açar.

## Scope

- Yeni semantic katman: `hidden_10_strategic_supervision`
- Gerçek `H10_*.md` düğümleri
- `brain_growth` toolchain içinde H10 discovery, builder, validator ve projection desteği
- H9 -> H10 transition görünürlüğü
- Yeni türetilmiş projection grafı: `strategic_supervision_graph`

Scope dışı:

- gerçek runtime executor
- dış API/agent entegrasyonu
- otomatik görev tetikleyici ya da cron motoru
- H11 ve sonrası

## Current state

Şu zincir first-class durumda:

- `raw`
- `hidden_3`
- `hidden_4`
- `hidden_5`
- `hidden_6`
- `hidden_7`
- `hidden_8`
- `hidden_9`
- `index`

H9’un yaptığı iş:

- policy’yi execution package’a indirmek
- delivery surface bağlamak
- commit/readiness seviyesinde package semantics üretmek

H9’un yapmadığı iş:

- paketlerin stratejik risk sınıfını belirlemek
- escalation / rollback kararını supervision düzeyinde ayırmak
- `Long_Term_Strategic_Planner`, `Strategic_Resource_Allocator`, `Global_State_Consensus` gibi yüzeylere üst-denetim sinyali üretmek

Bu yüzden H10’un görevi execution üretmek değil, execution packaging üstünde strategic supervision üretmektir.

## Chosen approach

### Recommended: ayrı `hidden_10_strategic_supervision` katmanı

Bu yaklaşımda:

- H8 karar montajı olarak kalır
- H9 execution packaging olarak kalır
- H10 üst denetim ve stratejik yönetişim olur

Artıları:

- semantic sınırlar net
- rollback/escalation mantığı packaging’den ayrılır
- projection’da package graph ile supervision graph ayrışır
- gelecekte H11 reflection/audit katmanı için temiz zemin oluşur

Eksileri:

- yeni builder/test/validator/projection dalgası gerekir

### Rejected: H9 içine supervision gömmek

Packaging ve supervision tek katmanda birleşirse delivery contract ile strategic governance birbirine karışır. Özellikle validator issue code’ları ve derived graph anlamı bulanıklaşır.

### Rejected: doğrudan executor kurmak

Semantic graph büyüme desenini bozup tool/runtime dünyasına erken sıçrar. Mevcut repo mimarisi için YAGNI.

## H10 semantic model

### Katman adı

- `#layer/hidden_10_strategic_supervision`

### Zorunlu frontmatter alanları

- `supervision_mode`
- `governing_signal`
- `oversight_surfaces`
- `supervision_contracts`

### Zorunlu tag seti

- `#layer/hidden_10_strategic_supervision`
- `#strategy/supervision_contract`
- `#strategy/oversight_surface`
- `#execution/governance_binding`

### Zorunlu section başlıkları

- `## Stratejik denetim amacı`
- `## Governing signal eşlemesi`
- `## Oversight surface sözleşmeleri`
- `## Escalation ve rollback kuralları`
- `## Besleyen H9 düğümleri`
- `## Denetlenen çıktı yolları`

## Proposed H10 families

- `H10_Global_Supervision_Arbitration.md`
- `H10_Rollback_Escalation_Governance.md`
- `H10_Strategic_Resource_Oversight.md`
- `H10_Long_Horizon_Outcome_Review.md`

Bu aileler H9’un üstüne şu şekilde oturur:

- execution surface binding -> global supervision arbitration
- response payload composition -> long horizon outcome review
- commit ready delivery check -> rollback/escalation governance
- failsafe action packaging -> strategic resource oversight

## File changes

### Create

- `tools/brain_growth/h10_builder.py`
- `tests/test_brain_growth_h10_builder.py`
- `Lokum1.0/Knowledge/H10_Global_Supervision_Arbitration.md`
- `Lokum1.0/Knowledge/H10_Rollback_Escalation_Governance.md`
- `Lokum1.0/Knowledge/H10_Strategic_Resource_Oversight.md`
- `Lokum1.0/Knowledge/H10_Long_Horizon_Outcome_Review.md`

### Modify

- `tools/brain_growth/common.py`
- `tools/brain_growth/quality_validator.py`
- `tools/brain_growth/layered_projection.py`
- `tests/test_brain_growth_validator.py`
- `tests/test_brain_growth_layered_projection.py`

### Refresh outputs

- `docs/brain_growth/reports/brain_growth_validation.json`
- `docs/brain_growth/reports/brain_growth_validation.txt`
- `docs/brain_growth/projections/brain_growth_layered_projection.json`
- `docs/brain_growth/projections/brain_growth_layered_projection.md`

## Builder behavior

`h10_builder.py` H9 builder desenini takip edecek ama H9 kaynaklarını kullanacak.

Her H10 family:

- belirli `H9_*` kaynaklarına bağlanacak
- oversight surface listesi taşıyacak
- supervision contract listesi taşıyacak
- mevcut stratejik legacy yüzeylere wikilink verecek
- forbidden center rule’u ihlal etmeyecek

Builder güvenlikleri:

- H9 source notları var mı kontrolü
- oversight surface hedefleri var mı kontrolü
- denetlenen output hedefleri var mı kontrolü
- overwrite için explicit `--force`

## Validator behavior

Validator `h10` kind’ını first-class desteklemeli.

Yeni issue code aileleri:

- `invalid_supervision_mode`
- `missing_governing_signal`
- `missing_oversight_surface`
- `missing_supervision_contract`
- `missing_h9_input`
- `missing_governing_signal_mapping`
- `missing_oversight_contract`
- `missing_escalation_rule`
- `h10_spec_violation`

Yeni remediation class aileleri:

- `supervision_frontmatter_repair`
- `oversight_surface_repair`
- `strategic_contract_repair`
- `escalation_governance_repair`

Karar:

- `--fix` H10 semantics’ini uydurmaz
- yalnız güvenli yapısal düzeltme yapar
- semantic eksikler yalnız raporlanır

## Projection behavior

`LAYER_ORDER` içine `hidden_10` eklenecek ve H9 -> H10 geçişleri görünür olacak.

Yeni türetilmiş graph:

- `strategic_supervision_graph`

Bu graph en az şu alanları taşımalı:

- `signal_nodes`
- `supervision_nodes`
- `oversight_nodes`
- `governance_edges`
- `oversight_edges`

Karar:

- H8 için `workspace_broadcast_graph` kalır
- H9 için `execution_package_graph` kalır
- H10 için `strategic_supervision_graph` ayrı eklenir

## Testing strategy

TDD zorunlu:

1. `test_brain_growth_h10_builder.py` önce kırılacak
2. minimal H10 builder yazılacak
3. validator’a H10 testleri eklenecek, önce fail sonra pass
4. projection’a `hidden_10` ve `strategic_supervision_graph` assertion’ları eklenecek, önce fail sonra pass
5. tam suite tekrar koşulacak

## Success criteria

Wave 10 başarılı sayılırsa:

- 4 adet `H10_*` note üretilmiş olur
- validator `h10` kind’ını gösterir
- projection `hidden_10` ve `strategic_supervision_graph` export eder
- H9 regress etmez
- forbidden reference count artmaz
- `LokumAI-1.0.md` untouched kalır

## Notes on requested skills

Bu dalgada pratikte aktif gerekli skill’ler:

- `brainstorming`
- `writing-plans`
- `executing-plans`
- `obsidian-markdown`

Şu an için gerekli görünmeyenler:

- `agent-browser`
- `data-analysis`
- `consulting-analysis`
- `obsidian-bases`
- `obsidian-cli`

Sırf isim geçti diye devreye almak yine YAGNI olur.
