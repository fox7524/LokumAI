---
date: 2026-08-30
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - "#hardware/esp32"
---

# ESP32 FreeRTOS SMP Core Affinity

## Teknik çekirdek

ESP-IDF FreeRTOS, upstream vanilla FreeRTOS'tan türetilmiş olsa da ESP32 çift çekirdekli hedefler için scheduler, interrupt dağıtımı ve task affinity katmanlarını pratikte SMP-benzeri davranacak şekilde değiştirir. Core 0 ve Core 1 aynı adres alanını paylaşır; ancak housekeeping yükleri, timer tick bookkeeping ve bazı sistem servisleri simetrik dağılmaz. Bu yüzden "iki core var, her iş otomatik dengelenir" varsayımı çoğu gerçek zamanlı tasarımda yanlıştır.

`xTaskCreatePinnedToCore()` ve `xTaskCreateUniversal()` benzeri desenlerde temel karar, task'ın bir çekirdeğe sabitlenip sabitlenmeyeceğidir. `tskNO_AFFINITY`, scheduler'a iki çekirdekte de koşabilen bir iş parçacığı verir; ama bu özgürlük cache locality, lock contention ve ISR ile aynı core üzerinde ko-lokasyon gibi etkileri görünmez hale getirebilir. Özellikle Wi-Fi/Bluetooth stack, yüksek frekanslı telemetry toplama ve kesme sonrası deferred work taşıyan sistemlerde yanlış affinity seçimi jitter, watchdog ve queue drift olarak geri döner.

ESP-IDF tarafında tick bookkeeping'in kritik kısmı Core 0 ile daha sık ilişkilidir. Core 0 üzerinde uzun kritik bölgeler, yoğun flash/cache disable pencereleri veya sürekli spinlock baskısı oluşursa sistem zamanı yalnızca gecikmez; timeout tabanlı driver davranışları, retry budget'ları ve task watchdog gözlemleri de sapar.

## Mimari davranış

Affinity kararı, yalnızca "performans optimizasyonu" değildir; scheduler gözlenebilirliğini belirleyen bir topoloji seçimidir. ISR'ın allocate edildiği core ile onu tüketen task'ın aynı çekirdekte tutulması, queue hop ve cross-core wakeup maliyetini azaltabilir. Buna karşılık CPU-ağır parsing ya da sık log formatlama işleri Core 0'a pinlenirse housekeeping ile yarışır ve sistem çapında zaman kayması üretir.

`tskNO_AFFINITY` çoğu zaman güvenli başlangıç gibi görünür; fakat aynı anda iki çekirdekte rekabet eden ready list, mutex ve cache line hareketleri sebebiyle deterministik latency gerektiren sürücülerde beklenmedik varyans yaratır. Bunun iyi kullanımı, saf hesaplama veya kısa ömürlü worker task'ları için esneklik sağlamak; kötü kullanımı ise kritik control-plane task'larını "scheduler halleder" diye serbest bırakmaktır.

## Kritik sınırlamalar

Core 0 üzerinde timer/tick ilişkili housekeeping baskısı varken uzun süreli polling, geniş kritik bölgeler veya bloklayıcı debug çıktıları bu çekirdeği kirletir. Core 1'i yoğun iş için kullanmak tek başına çözüm değildir; çünkü shared resource contention devam eder. Ayrıca affinity seçimi interrupt core ownership, queue consumer konumu ve watchdog feed yolu ile birlikte ele alınmazsa yanlış pozitif kök neden çıkarımı yapılır.

Bir diğer sınır, pinlenmiş task'ların migration esnekliğini kaybetmesidir. Bu iyi bir latency kararı olabilir; fakat tek bir core üzerinde backpressure oluştuğunda diğer çekirdek boştayken bile sistem darboğaza girebilir. Bu yüzden affinity kararı throughput değil, determinism ve failure isolation ekseninde değerlendirilmelidir.

## Failure modes

Yanlış core'a pinlenen yüksek frekanslı telemetry task'ı, Core 0 tick akışını bozar ve timeout kullanan sürücülerde sahte "cihaz cevap vermedi" olayları üretir. `tskNO_AFFINITY` bırakılmış ama sık lock kullanan task'lar ise cross-core bounce yüzünden ani latency sıçramaları, watchdog warning ve queue consumer starvation olarak görünür.

Diğer tipik arıza, ISR sonrası worker task'ın farklı core'da uyanması nedeniyle event'in işlenme süresinin uzamasıdır. Loglarda doğrudan "affinity hatası" yazmaz; semptom genellikle periyodik jitter, missed deadline veya yalnızca yük altında ortaya çıkan drift şeklindedir.

## Debug / telemetry / profiling sinyalleri

Core bazlı run-time stats, task watchdog logları ve `vTaskGetRunTimeStats()` benzeri sayaçlar hangi core'un housekeeping yüzünden boğulduğunu gösterir. Eğer timeout'lar özellikle flash operasyonu, yoğun logging veya Wi-Fi aktivitesi sırasında artıyorsa Core 0 baskısı şüphelidir. Queue depth trend'i yükselirken CPU kullanımı düşük görünüyorsa, sorun ham compute eksikliğinden çok core placement olabilir.

Pratik debug heuristiği: ISR allocate eden core, deferred worker task core'u ve watchdog uyarısında adı geçen task'ı aynı zaman penceresinde incele. Ayrıca aynı yazılım yükünü bir kez açık pinleme ile, bir kez `tskNO_AFFINITY` ile kıyaslayıp jitter histogramını karşılaştırmak, scheduler drift ile logic bug'ı ayırmada güçlü sinyaldir.

## LokumAI için çıkarım

LokumAI'nin ESP32 ile etkileşen gömülü ajanlarında "hangi işi hangi core'a pinlemek gerekir" sorusu doğrudan bu hücreye bağlanmalıdır. Özellikle sensör ingestion, ISR sonrası worker zinciri, watchdog triage ve zaman tabanlı retry mekanizmalarında affinity bilgisi retrieval filtresi olarak kullanılmalıdır. Ajan, yalnızca yüksek CPU kullanımı gördüğü için optimizasyon önermemeli; önce Core 0 housekeeping yükü, `tskNO_AFFINITY` trade-off'u ve cross-core wakeup maliyeti arasında bağ kurmalıdır.

Bu hücre aynı zamanda kök neden ayrıştırması yapar: sorun scheduler tasarımı mı, interrupt topolojisi mi, yoksa heap / DMA darboğazı mı? Eğer semptom drift, starvation ve watchdog etrafında dönüyorsa retrieval sırası bu düğümü öne çekmelidir.

## Sorgu ipuçları

- `idf freertos smp`
- `xTaskCreatePinnedToCore`
- `tskNO_AFFINITY`
- `core 0 tick responsibility`
- `esp32 scheduler starvation core 0`
- `esp-idf affinity watchdog drift`

## Kaynaklar

- https://docs.espressif.com/projects/esp-idf/en/v5.3.5/esp32p4/api-reference/system/freertos_idf.html
- https://www.freertos.org/smp-core-affinity-for-openamp-amp-smp-rtos.html
- https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/performance/speed.html

[[RAG_Memory_Cell_27_ESP32_Task_Watchdog_And_Core_Starvation_Patterns]]
[[RAG_Memory_Cell_38_Tickless_Idle_And_Wake_Latency_On_ESP32]]
[[Context_Switch_Monitor]]
[[Behavioral_Feature_Mapping]]
