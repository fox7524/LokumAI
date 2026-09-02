---
date: 2026-08-30
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - "#hardware/esp32"
---

# ESP32 DMA Capable Memory and ISR Preallocation

## Teknik çekirdek

ESP-IDF bellek ayırıcısı, tüm RAM'i eşit görmez; capability-based allocator her bölgeyi belirli kullanım nitelikleriyle etiketler. Bir tamponu donanım DMA motoruna vereceksen, yalnız kapasite değil capability de doğru olmalıdır. Bu yüzden `heap_caps_malloc(size, MALLOC_CAP_DMA)` kullanımı yalnız bir API tercihi değil, veri yolunun gerçekten DMA tarafından erişilebilir olup olmayacağını belirleyen mimari kontrattır.

Kritik nokta, "çok bellek" ile "DMA için uygun bellek" arasındaki farktır. External PSRAM çoğu ESP32 varyantında büyük kapasite sunar; fakat doğrudan DMA-capable değildir ya da erişim biçimi ciddi kısıt taşır. Bu nedenle yüksek hacimli buffer tasarlarken yalnız toplam byte hesabı yapmak yanıltıcıdır. Bir sistem PSRAM bakımından rahat görünebilir ama internal DMA-capable havuz tükendiğinde ses akışı, SPI burst ya da kamera pipeline'ı çökebilir.

ISR bağlamında allocation kararı daha da hassastır. Teknik olarak bazı heap çağrıları çalışıyor gibi görünse de, dokümantasyon bunlardan kaçınılmasını önerir; çünkü allocation yolu lock, fragmentation ve latency varyansı içerir. Deterministik tasarım, descriptor, ring buffer ve bounce buffer'ları init aşamasında ayırmak; ISR içinde yalnızca pointer/index güncellemesi yapmaktır.

## Mimari davranış

DMA-capable buffer topolojisi, periferal türüne göre farklı baskılar altında çalışır. I2S veya SPI gibi sürekli akan arayüzlerde descriptor zincirinin sürekliliği, cache davranışı ve ISR servis hızı birbirini doğrudan etkiler. Eğer veri kaynağı PSRAM'de tutuluyor ama DMA internal memory istiyorsa, araya kopya veya staging buffer girmek zorunda kalınır. Bu da "zero-copy" sanılan tasarımın aslında iki aşamalı hale gelmesine yol açar.

Preallocation yaklaşımı, yalnız latency azaltmaz; hata yüzeyini de daraltır. Başlangıçta ayrılmış sabit boyutlu buffer havuzu sayesinde ISR kodu başarısız allocation, farklı hizalama ve fragmentasyon durumlarıyla uğraşmaz. Böylece buffer ownership kuralları daha net tanımlanır ve race condition analizi kolaylaşır.

## Kritik sınırlamalar

`MALLOC_CAP_DMA` ile ayrılmış bellek havuzu sınırlıdır ve genellikle internal RAM ile rekabet eder. Aynı havuzdan Wi-Fi, stack, driver state ve DMA buffer çekiyorsa, sistem yük arttıkça "bellek var ama doğru bellekte değil" problemi büyür. Ayrıca `MALLOC_CAP_32BIT`, cache line hizalaması veya peripheral alignment gereksinimleri ile karıştırılmamalıdır; yanlış capability kombinasyonu sessiz veri bozulması veya periferal hata register'ı üretir.

PSRAM kullanımının bir başka sınırı cache ve gecikmedir. Veri PSRAM'de dursa bile ISR yolunda anlık kopya yapılması gerekiyorsa latency sabit kalmaz. Bu yüzden yüksek throughput gerektiren yol ile büyük fakat soğuk depolama yolu ayrıştırılmalıdır.

## Failure modes

En tipik arıza, runtime allocation yapan ISR veya ISR'a çok yakın callback zinciridir. Bu durumda sistem nominalde çalışır; ancak yük yükseldiğinde interrupt latency büyür, descriptor starvation görülür ve periferal underrun/overflow hataları patlar. Başka bir failure mode, buffer'ın DMA-capable sanılıp aslında uygun capability'de olmamasıdır; sonuç bazen doğrudan crash değil, kesik ses, eksik frame veya nadir CRC bozulmasıdır.

Descriptor ring sayısı düşükse consumer geçici gecikmede hemen boşalır; fazla yüksekse internal RAM gereksiz tüketilir ve diğer kritik path'ler aç kalır. Bu denge kurulmadığında semptom çoğu zaman aralıklı veri boşluğu, burst sonunda bozuk paket veya yalnız uzun süreli testte görülen jitter olur.

## Debug / telemetry / profiling sinyalleri

Heap capability raporları, allocation başarısızlık sayaçları ve periferalin underrun/overflow flag'leri birlikte okunmalıdır. Free heap yüksek görünürken `MALLOC_CAP_DMA` havuzu düşüyorsa kök neden genel bellek kıtlığı değil, doğru capability'deki bölgenin tükenmesidir. Descriptor tüketim oranı ile ISR servis süresi yan yana izlendiğinde starvation erken yakalanır.

Profiling açısından iyi sinyal, buffer recycle gecikmesi, ring occupancy eğrisi ve flash/cache baskısı altındaki latency histogramıdır. Eğer sorun yalnız PSRAM yoğun erişim dönemlerinde beliriyorsa, staging buffer boyu ve internal RAM rezervasyonu tekrar ayarlanmalıdır. Eğer hata yalnız uzun çalışma sonunda çıkıyorsa fragmentasyon yerine descriptor ownership sızıntısı aranmalıdır.

## LokumAI için çıkarım

LokumAI'nin ESP32 veri toplama ajanlarında buffer tasarımı, ham throughput kadar önemlidir. Bu hücre; DMA yolu ile gelen veri akışında hangi tamponların gerçekten kullanılabilir olduğunu, PSRAM'in neden her zaman doğrudan çözüm olmadığını ve ISR'de allocation yapmanın neden tehlikeli olduğunu ayıran temel bellek düğümüdür. Ajan, "veri kaybı var" diye genel tavsiye vermek yerine önce capability uyumu, descriptor havuzu ve preallocation disiplinini sorgulamalıdır.

Bu hücre ayrıca retrieval sırasında semptom kümelerini ayırır: underrun mı var, descriptor starvation mı, cache/PSRAM staging maliyeti mi, yoksa heap fragmentasyonu mu? Aynı görünen veri kaybı olayları bu ayrım yapılmadan doğru onarıma bağlanamaz.

## Sorgu ipuçları

- `MALLOC_CAP_DMA`
- `dma capable memory psram`
- `heap_caps_malloc`
- `ISR preallocation`
- `esp32 dma descriptor starvation`
- `psram cache dma staging buffer`

## Kaynaklar

- https://docs.espressif.com/projects/esp-idf/en/v5.2.7/esp32s3/api-reference/system/mem_alloc.html
- https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/mem_alloc.html
- https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/performance/ram-usage.html

[[RAG_Memory_Cell_32_I2S_DMA_Descriptor_Rings_On_ESP32]]
[[RAG_Memory_Cell_33_SPI_DMA_Burst_Alignment_And_Cache_Coherency]]
[[RAG_Memory_Cell_36_PSRAM_Access_Penalties_In_Real_Time_Paths]]
[[DRAM_Bandwidth_Utilization]]
