# Wave 9 Hidden 9 Execution Packaging Design

**Goal:** H8 `decision_assembly` katmanından çıkan dominant policy ve broadcast hedeflerini, gerçek downstream execution yüzeylerine bağlanabilen, doğrulanabilir ve projection/export içinde görünür `hidden_9_execution_packaging` katmanına dönüştürmek.

**Why now:** H8 ile karar montajı tamamlandı, fakat sistem hâlâ “hangi policy hangi execution surface’e hangi paket biçimiyle iner” sorusunu first-class bir katman olarak modellemiyor. H9 bu boşluğu dolduracak ve H8 ile legacy execution yüzeyleri arasında kontrollü bir köprü kuracak.

## Scope

- Yeni resmi semantic katman: `hidden_9_execution_packaging`
- Gerçek `H9_*.md` düğümleri
- `brain_growth` toolchain içinde H9 discovery, builder, validator ve projection desteği
- H8 -> H9 transition görünürlüğü
- Yeni türetilmiş projection grafı: `execution_package_graph`

Scope dışı:

- Runtime executor
- dış sistem entegrasyonu
- shell/script çalıştıran gerçek action engine
- H10 veya daha üst stratejik katmanlar

## Current state

Sistemde şu akış artık first-class:

- `raw`
- `hidden_3`
- `hidden_4`
- `hidden_5`
- `hidden_6`
- `hidden_7`
- `hidden_8`
- `index`

H8 şu işi yapıyor:

- dominant thoughtseed seçimi
- candidate policy set assembly
- broadcast target belirleme

Ama H8 şu işi yapmıyor:

- policy’nin execution paket formatını modelleme
- aynı policy’nin farklı yüzeylere nasıl “surface-bound package” olarak ineceğini ayırma
- delivery readiness ile commitment durumunu ayrı bir katman olarak izleme

Bu yüzden en temiz devam, H8’i şişirmek değil, H9’da execution-packaging semantics açmaktır.

## Chosen approach

### Recommended: ayrı `hidden_9_execution_packaging` katmanı

Bu yaklaşımda H8 policy seviyesinde kalır, H9 ise delivery/readiness/packaging seviyesini üstlenir.

Artıları:

- semantic sınırlar net kalır
- validator mantığı daha temiz ayrılır
- projection’da H8 broadcast graph ile H9 package graph ayrı ayrı görülebilir
- gelecekte H10 strategic oversight katmanı için temiz taban bırakır

Eksileri:

- bir builder/test/validator/projection dalgası daha gerekir

### Rejected: H8 içine packaging eklemek

Bu yaklaşım daha az dosya üretir ama H8’in karar montajı ile execution surface bağlama sorumluluğunu birbirine karıştırır. Projection ve validator anlamında da tek dosyada aşırı rol yüklenir.

### Rejected: H10’a atlamak

Execution seam boş kalacağı için mimari zincirde yapay bir sıçrama oluşur. H8 policy’den H10 strategy’ye geçmek, alt teslim yüzeylerini görünmez bırakır.

## H9 semantic model

### Katman adı

- `#layer/hidden_9_execution_packaging`

### Zorunlu frontmatter alanları

- `package_mode`
- `source_policy`
- `delivery_surfaces`
- `package_contracts`

### Zorunlu tag seti

- `#layer/hidden_9_execution_packaging`
- `#execution/package_contract`
- `#execution/delivery_surface`
- `#policy/surface_binding`

### Zorunlu section başlıkları

- `## Paketleme amacı`
- `## Source policy eşlemesi`
- `## Delivery surface sözleşmeleri`
- `## Readiness ve commit koşulları`
- `## Besleyen H8 düğümleri`
- `## Paketlenen çıktı yolları`

## Proposed H9 families

- `H9_Execution_Surface_Binding.md`
- `H9_Response_Payload_Composition.md`
- `H9_Commit_Ready_Delivery_Check.md`
- `H9_Failsafe_Action_Packaging.md`

Bu dört aile H8 ailelerinin aşağı akış karşılığı gibi davranacak:

- thoughtseed/policy seçimi -> surface binding
- global policy broadcast -> payload composition
- decision commitment gate -> commit-ready delivery check
- exception override arbitration -> failsafe action packaging

## File changes

### Create

- `tools/brain_growth/h9_builder.py`
- `tests/test_brain_growth_h9_builder.py`
- `Lokum1.0/Knowledge/H9_Execution_Surface_Binding.md`
- `Lokum1.0/Knowledge/H9_Response_Payload_Composition.md`
- `Lokum1.0/Knowledge/H9_Commit_Ready_Delivery_Check.md`
- `Lokum1.0/Knowledge/H9_Failsafe_Action_Packaging.md`
- `docs/superpowers/plans/2026-08-30-hidden9-execution-packaging-implementation-plan.md`

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

`h9_builder.py` H8 builder desenini takip edecek ama H8 girdilerini kullanacak.

Her H9 family:

- belirli `H8_*` kaynaklarına bağlanacak
- delivery surface listesi taşıyacak
- package contract listesi taşıyacak
- downstream legacy yüzeylere wikilink verecek
- `LokumAI-1.0.md` ve forbidden center rule’u ihlal etmeyecek

Builder şu güvenlikleri zorunlu kılmalı:

- H8 source notları var mı kontrolü
- delivery surface hedefleri var mı kontrolü
- downstream output hedefleri var mı kontrolü
- overwrite için explicit `--force`

## Validator behavior

Validator artık `h9` kind’ını first-class desteklemeli.

Yeni issue code aileleri:

- `invalid_package_mode`
- `missing_source_policy`
- `missing_delivery_surface`
- `missing_package_contract`
- `missing_h8_input`
- `missing_delivery_strategy`
- `missing_commit_readiness_rule`
- `h9_spec_violation`

Yeni remediation class aileleri:

- `package_frontmatter_repair`
- `delivery_surface_repair`
- `execution_contract_repair`
- `commit_readiness_repair`

Önemli karar:

- `--fix` H9 semantics’ini uydurmayacak
- yalnız güvenli yapısal düzeltmeler yapılacak
- semantic eksikler raporlanacak ama otomatik doldurulmayacak

## Projection behavior

`LAYER_ORDER` içine `hidden_9` eklenecek ve H8 -> H9 geçişleri görünür olacak.

Yeni türetilmiş graph:

- `execution_package_graph`

Bu graph en az şu alanları taşımalı:

- `policy_nodes`
- `package_nodes`
- `surface_nodes`
- `binding_edges`
- `delivery_edges`

Karar:

- `workspace_broadcast_graph` H8 için kalacak
- `execution_package_graph` H9 için ayrı üretilecek
- semantic source-of-truth vault ile derived graph export birbirine karıştırılmayacak

## Testing strategy

TDD zorunlu olacak:

1. `test_brain_growth_h9_builder.py` önce kırılacak
2. minimal H9 builder implementasyonu yazılacak
3. validator’a H9 testleri eklenecek, önce fail sonra pass
4. projection’a `hidden_9` ve `execution_package_graph` assertion’ları eklenecek, önce fail sonra pass
5. tam `brain_growth` suite tekrar koşulacak

## Success criteria

Wave 9 başarılı sayılırsa:

- 4 adet `H9_*` note üretilmiş olacak
- validator `h9` kind’ını gösterecek
- projection `hidden_9` ve `execution_package_graph` export edecek
- H8 davranışı regress etmeyecek
- forbidden reference count artmayacak
- `LokumAI-1.0.md` untouched kalacak

## Notes on requested skills

Bu dalganın çekirdeği yine builder/validator/projection/Obsidian note zinciri olduğu için pratikte aktif kullanılacak skill’ler:

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

Kullanıcı tekrar adlarını verdi ama bu dalgada doğrudan leverage etmeyenleri sırf isim geçti diye devreye almak YAGNI olur.
