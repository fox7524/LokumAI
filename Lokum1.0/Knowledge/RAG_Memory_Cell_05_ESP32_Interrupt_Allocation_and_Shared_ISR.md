---
date: 2026-08-30
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - "#hardware/esp32"
---

# ESP32 Interrupt Allocation and Shared ISR

## Teknik çekirdek

ESP32 interrupt allocator, peripheral kaynağını CPU interrupt girişine eşleyen bir yönlendirme tabakasıdır. `esp_intr_alloc()` ve türevleri, interrupt seviyesi, paylaşım gereksinimi, edge/level karakteri ve IRAM kısıtı gibi parametrelere bakarak uygun hattı seçer. Bu seçim soyut bir kayıt işlemi değildir; handler hangi çekirdekte çalışacak, hangi öncelik bandını tüketecek ve başka hangi kaynaklarla aynı hattı paylaşacak sorularını belirler.

External interrupt tahsisinin allocate eden çekirdeğe bağlanması, interrupt topolojisini task affinity ile birlikte düşünmeyi zorunlu kılar. Bir driver Core 0 üzerinde init edilip ISR oraya bağlandıysa, daha sonra o ISR'ın wake ettiği task'ı Core 1'e koymak, latency zincirine cross-core handoff maliyeti ekler. Bu maliyet her zaman ortalama değerde görünmez; çoğu zaman yalnızca yüksek yük ve cache baskısı altında kuyruk şeklinde büyür.

Shared ISR modeli, birden fazla peripheral'in aynı CPU interrupt line'ını paylaşmasına izin verir. Bu durumda dispatcher sihirli biçimde hangi kaynağın tetiklediğini bilmez; her handler kendi durum bitini okuyup "bu interrupt bana mı ait" kararını vermek zorundadır. Tam da bu nedenle shared interrupt'ların edge-triggered yerine level-triggered olması gerekir; aksi halde bir periferal interrupt'ı diğerini gölgede bırakabilir ve missed interrupt oluşur.

## Mimari davranış

Shared interrupt line üzerinde bir arada yaşayan ISR'lar kooperatif yaşar. Bir handler gereksiz yere uzun sürerse yalnız kendi periferalini değil, aynı hatta bağlı diğer kaynakların servis süresini de uzatır. Bu yüzden paylaşılan hatta çalışan ISR'lar minimum iş yapmalı, status bitini hızlı kontrol etmeli ve asıl işi task context'ine bırakmalıdır.

`ESP_INTR_FLAG_IRAM` kullanımı da mimari bir taahhüttür. Sadece handler fonksiyonunun IRAM'de olması yetmez; handler'ın çağırdığı tüm yardımcılar ve dokunduğu tüm veri yapıları cache kapalı pencerede erişilebilir iç bellekte olmalıdır. Aksi halde "IRAM-safe" diye etiketlenen yol, tam da flash erase veya yazma anlarında illegal instruction, cache access fault ya da uzun latency spike üretebilir.

## Kritik sınırlamalar

ESP32 ailesinde kullanılabilir interrupt hattı, öncelik seviyesi ve paylaşılabilirlik kombinasyonları sonsuz değildir. Sık "allocate et, gerekirse sistem halleder" yaklaşımı, özellikle Wi-Fi, Bluetooth, I2S, SPI ve GPIO gibi birden çok periferal aynı anda aktifken allocator baskısı yaratır. Ayrıca free işleminin aynı core'da yapılması gereksinimi, dinamik sürücü yaşam döngüsünde teardown path'ini de tasarım konusu haline getirir.

Paylaşılan hatta status biti temizleme sırası da sınırlayıcıdır. Yanlış sırada clear edilen veya ack edilen durum, aynı anda iki kaynağın hizmet istediği durumda phantom retrigger ya da tam tersi missed service üretebilir. Bu yüzden shared ISR kodu kısa olduğu kadar deterministik olmalıdır.

## Failure modes

En klasik arıza, shared hatta bağlanan handler'lardan birinin status biti kontrolünü atlayıp her interrupt'ta koşmasıdır. Bu durumda CPU kullanımı sebepsiz şişer, diğer kaynakların gerçek kesmeleri gecikir ve loglarda "yük altında garip latency" dışında belirgin sinyal görülmeyebilir. Edge-triggered paylaşıma zorlanan tasarımlarda ise interrupt kaybı sporadik veri boşluğu veya stuck peripheral olarak görünür.

IRAM-safe sanılan fakat yardımcı fonksiyonları flash'ta kalan ISR'lar, özellikle flash erase, OTA veya NVS yazımı sırasında patlar. Bir diğer failure mode, ISR'ın allocate edildiği core ile deferred worker topolojisinin uyuşmamasıdır; bu durumda semptom doğrudan crash değil, interrupt serviced ama veri pipeline geride kalıyor biçiminde ortaya çıkar.

## Debug / telemetry / profiling sinyalleri

Interrupt latency profilini anlamak için yalnız ISR giriş sayısına değil, line sharing durumuna, status-bit hit oranına ve deferred work kuyruğunun backlog'una bakmak gerekir. Belirli bir periferal nominalde düşük frekanslı tetiklenirken CPU interrupt sayısı aşırı yüksekse shared hatta "yanlış alarm" yaşayan bir handler olabilir. Flash/NVS işlemleri sırasında timeout veya cache error log'ları artıyorsa IRAM zinciri eksik demektir.

Pratik profiling sinyali olarak, handler başına servis süresi histogramı ve aynı line üzerindeki kaynağa göre dağılım tutulmalıdır. Eğer sadece yük altında belirginleşen latency kuyruğu varsa, önce shared ISR cohabitation düzeni, sonra core affinity ve son olarak interrupt level seçimi sorgulanmalıdır.

## LokumAI için çıkarım

Bu hücre, LokumAI'nin ESP32 kenar cihazlarında interrupt routing davranışını ayrı bir retrieval kalıbına dönüştürür. Özellikle telemetry sapmaları, missed interrupt analizi, driver init sırası ve IRAM-safe doğrulaması gereken olaylarda ajan önce bu düğüme bakmalıdır. Semptom yalnızca "latency yüksek" değildir; paylaşılan ISR hattı, yanlış status-bit disiplini ve çekirdekler arası handoff yüzünden bozulmuş olay zinciri olabilir.

LokumAI tarafında bu bilgi, kök nedenleri ayrıştırmak için kullanılır: aynı semptom GPIO matrix jitter'dan mı, IRAM ihlalinden mi, yoksa shared handler kooperasyon bozulmasından mı geliyor? Bu hücre tam bu ayrımı yapar.

## Sorgu ipuçları

- `esp_intr_alloc`
- `shared interrupt level triggered`
- `esp_intr_flag_iram`
- `interrupt allocation core affinity`
- `esp32 shared isr status bit check`
- `esp32 interrupt latency under load`

## Kaynaklar

- https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/system/intr_alloc.html
- https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/performance/speed.html
- https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/intr_alloc.html#iram-safe-interrupt-handlers

[[RAG_Memory_Cell_26_ESP32_IRAM_Safe_ISR_Latency_Budgets]]
[[RAG_Memory_Cell_30_GPIO_Matrix_Interrupt_Fan_In_And_Signal_Jitter]]
[[Instruction_Fetch_Analysis]]
[[Temporal_Pattern_Recognition]]
