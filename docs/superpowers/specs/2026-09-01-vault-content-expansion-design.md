# Vault Content Expansion & Reasoning-Grade Knowledge Design

**Goal:** LokumAI vault içindeki `.md` düğümlerini yüzeysel not deposundan çıkarıp, agent muhakemesine gerçekten yakıt veren yoğun teknik bilgi ağına dönüştürmek; aynı anda hem mevcut ince notları derinleştirmek hem de yeni gömülü platform corpus’unu eklemek.

**Why now:** Mevcut graph katmanları `H11` seviyesine kadar semantik olarak kurulmuş durumda; fakat agent’ın düşünme kalitesi yalnız graph topolojisine değil, düğüm içeriğinin derinliğine bağlı. Şu an bazı `RAG_Memory_Cell_*` notları güçlü, bazı synthesis ve index düğümleri ise ince. Bu boşluk kapatılmadan “neural ağ gibi düşünen” bir substrate elde edilemez.

## Scope

- Hibrit büyüme modeli:
  - mevcut ince `.md` düğümlerini derinleştirme
  - yeni embedded/platform odaklı `.md` düğümler ekleme
- Not tipine göre zorunlu içerik omurgası tanımlama
- Embedded platform taksonomisini genişletme
- Vault kalite validator’ını içerik derinliği açısından büyütme
- Index ve synthesis düğümlerini retrieval yönlendirici hale getirme

Scope dışı:

- Gerçek zamanlı otomatik web crawling ile sınırsız kaynak ingest
- LLM fine-tuning veya embedding model retraining
- Bu dalganın içinde doğrudan “self-modifying autonomous rewrite loop” açılması
- Vault dışındaki bağımsız veri tabanı migrasyonu

## Core principle

Bu dalganın amacı “daha çok markdown dosyası” üretmek değildir. Amaç, her düğümün retrieval sırasında işe yarayan teknik taşıyıcılık kazanmasıdır. Bir notun var olması yetmez; agent için aşağıdaki sorulara cevap taşıması gerekir:

- Bu konu teknik olarak nasıl çalışır?
- Hangi failure mode’lar kritik?
- Hangi telemetry/debug sinyalleri aranmalı?
- Hangi diğer düğümlere gidilirse çözüm uzayı daralır?
- Bu bilgi LokumAI içinde hangi karar yüzeyine etki eder?

## Content model

### 1. `RAG_Memory_Cell_*`

Bu sınıf, en yoğun teknik bilgi hücreleridir. Her not retrieval sırasında tek başına yüksek fayda sağlamalıdır.

Zorunlu section omurgası:

- `## Teknik çekirdek`
- `## Mimari davranış`
- `## Kritik sınırlamalar`
- `## Failure modes`
- `## Debug / telemetry / profiling sinyalleri`
- `## LokumAI için çıkarım`
- `## Sorgu ipuçları`
- `## Kaynaklar`

Beklenen içerik karakteri:

- yüzeysel tanım değil, mekanizma seviyesi açıklama
- platforma özgü sınırlamalar
- tipik hata imzaları
- retrieval ipuçları
- alan içi cross-link’ler

### 2. `H3_*`

`H3` notları salt özet olmayacak; bunlar hidden routing/synthesis düğümleri olacak.

Zorunlu section omurgası:

- `## Soyutlama`
- `## İnvariantlar`
- `## Retrieval yönlendirme anlamı`
- `## Besleyen düğümler`
- `## İleri besleme`

Beklenen içerik karakteri:

- alt notların ortak mekanizmasını sıkıştırma
- semptom -> düğüm yönlendirmesi
- retrieval sırasında ilk çağrılacak router davranışı

### 3. `H4_*`, `H5_*`, `H6_*`

Bu düğümler karar ve ayrıştırma katmanlarıdır. Ansiklopedi gibi değil, branch logic taşıyacak biçimde kalınlaştırılır.

Zorunlu içerik:

- ayrıştırma kriterleri
- semptom ve sinyal eşlemesi
- tercih/eleme mantığı
- aşağı katman veya yan katman yönlendirmesi

### 4. `H7_*`, `H8_*`, `H9_*`, `H10_*`, `H11_*`

Bu katmanlar episodic, decision, execution, governance ve audit/reflection yüzeylerini taşır.

Beklenen içerik:

- provenance ve karar zinciri açıklığı
- failure/rollback/override mantığı
- write-back veya future learning loop için semantic yüzey
- hangi bilgi ne zaman graph’a commit edilmeli sorusuna zemin

### 5. `Index_*`

Index sayfaları salt link listesi veya dump olmayacak.

Zorunlu içerik:

- alan özeti
- kapsama sınırı
- temsilci düğümler
- hangi semptomta hangi cluster açılmalı
- bilinen boşluklar

## Embedded corpus expansion

Yeni notlar sadece kart ismi listesi olarak eklenmeyecek; aile ve problem yüzeyine göre gruplanacak.

### Platform / MCU family

- `ESP32`
- `ESP32-S2`
- `ESP32-S3`
- `ESP32-C3`
- `ESP32-C6`
- `ESP32-H2`
- `ESP8266 / NodeMCU`
- `STM32` aileleri (`F1`, `F4`, `H7` çizgileri)
- `RP2040`
- `nRF52`
- `Teensy / i.MX RT`

### Framework / RTOS / toolchain surface

- `FreeRTOS`
- `Zephyr`
- `ESP-IDF`
- `Arduino core`
- `PlatformIO`

### Peripheral / failure clusters

- `UART`
- `SPI`
- `I2C`
- `I2S`
- `ADC`
- `PWM`
- `USB`
- `Wi-Fi`
- `BLE`
- `watchdog`
- `brownout`
- `boot / flash / PSRAM`
- `DMA / ISR / cache-disable windows`

### Per-note expectations for embedded corpus

Her yeni embedded notu en azından şunları taşımalı:

- execution / memory model
- interrupt / DMA / concurrency davranışı
- toolchain / SDK surface
- common bug signatures
- debug/telemetry heuristics
- hangi üst synthesis düğümlerine bağlanacağı

## Growth waves

### Wave A · Vault audit and classification

- mevcut `.md` düğümleri `thin`, `medium`, `strong` olarak sınıflandır
- en kritik boş synthesis/index düğümlerini tespit et
- embedded, MLX, graph RAG ve execution kümelerindeki zayıf alanları haritala

### Wave B · Existing note deepening

- en zayıf mevcut teknik notları kalite standardına göre doldur
- özellikle içerik gövdesi zayıf olan `RAG_Memory_Cell_*`, `H3_*`, `Index_*` düğümlerini güçlendir

### Wave C · New embedded corpus insertion

- yeni platform ve framework düğümlerini ekle
- bunları yüzeysel değil, failure-aware teknik bilgi taşıyan notlar olarak yaz

### Wave D · Graph integration

- yeni düğümleri doğru synthesis ve index sayfalarına bağla
- gerektiği yerde yeni `H3/H4` yönlendirici bağlantıları ekle
- alan indekslerini kapsama boşluklarıyla birlikte güncelle

### Wave E · Quality gate expansion

- validator içine not derinliği ve retrieval utility kontrolleri ekle
- coverage raporu üret
- yeniden doldurulması gereken düğümleri listeler hale getir

## Validator expansion

Validator yalnız “dosya var mı” veya “frontmatter var mı” kontrolü yapmayacak. İçerik derinliği ve retrieval değeri ölçülecek.

### New rule families

- `thin note detection`
  - teknik gövde belirlenen eşiğin altındaysa `warn/fail`
- `missing required sections`
  - not tipine göre section omurgası eksikse `fail`
- `weak retrieval value`
  - query cues, çıkarım veya yönlendirme yoksa `warn/fail`
- `missing sources`
  - kaynak izi hiç yoksa `warn`
- `bad link density`
  - anlamsız derecede izole veya aşırı linklenmiş düğümse `warn`
- `orphan policy`
  - `LokumAI-1.0.md` dışı orphan düğümleri raporla
- `taxonomy mismatch`
  - dosya adı, tag ve içerik karakteri uyuşmuyorsa `fail`
- `embedded corpus coverage`
  - çekirdek platform kümeleri eksikse coverage raporuna yaz

### Quality scoring

Her düğüm için ölçülebilir skor üretilecek:

- `structure_score`
- `technical_depth_score`
- `retrieval_utility_score`
- `source_grounding_score`
- `graph_integration_score`

Amaç estetik puan değil; hangi düğümlerin hâlâ agent için zayıf olduğunu sistematik görmek.

## File impacts

### Likely content creation / modification

- `Lokum1.0/Knowledge/RAG_Memory_Cell_*.md`
- `Lokum1.0/Knowledge/H3_*.md`
- `Lokum1.0/Knowledge/H4_*.md`
- `Lokum1.0/Knowledge/H5_*.md`
- `Lokum1.0/Knowledge/H6_*.md`
- `Lokum1.0/Knowledge/H7_*.md`
- `Lokum1.0/Knowledge/H8_*.md`
- `Lokum1.0/Knowledge/H9_*.md`
- `Lokum1.0/Knowledge/H10_*.md`
- `Lokum1.0/Knowledge/H11_*.md`
- `Lokum1.0/Knowledge/Index_*.md`

### Likely toolchain changes

- `tools/brain_growth/quality_validator.py`
- gerekiyorsa yeni içerik kalite yardımcıları
- gerekiyorsa raporlama / sınıflandırma scriptleri

## Acceptance criteria

Bu tasarımın implementasyonu tamamlandığında aşağıdaki durumlar kanıtlanabilir olmalı:

- mevcut ince notların anlamlı bir alt kümesi yüksek derinlikli hale gelmiş olmalı
- yeni embedded platform corpus’unda çekirdek aileler temsil edilmiş olmalı
- `RAG_Memory_Cell_*` notları belirlenen section omurgasını taşımalı
- `Index_*` sayfaları link dump olmaktan çıkmış olmalı
- validator içerik derinliği ve retrieval utility açısından yeni kuralları raporlamalı
- graph kuralları bozulmamalı:
  - `LokumAI-1.0.md` orphan kalmalı
  - `rag_links` ve direct link semantiği karışmamalı
  - isimlendirme ve katman kuralları korunmalı

## Risks

- Çok hızlı genişleme kaliteyi sulandırabilir
- Yeni platform corpus’u mevcut taksonomiyi boğabilir
- Salt dosya çoğalması, retrieval utility üretmeyebilir
- Aşırı validator sertliği growth hızını düşürebilir

## Mitigations

- Wave tabanlı ilerleme
- not tipi başına zorunlu section standardı
- otomatik `thin note` tespiti
- coverage ve kalite skoru ile yeniden önceliklendirme

## Recommendation

Uygulama `quality-first hybrid wave` modeliyle yürütülmeli:

1. mevcut vault kalitesini ölç
2. en ince ve en kritik düğümleri derinleştir
3. yeni embedded corpus’u aynı kalite standardıyla ekle
4. synthesis/index entegrasyonunu yap
5. validator ile kalite kapısını kalıcı hale getir
