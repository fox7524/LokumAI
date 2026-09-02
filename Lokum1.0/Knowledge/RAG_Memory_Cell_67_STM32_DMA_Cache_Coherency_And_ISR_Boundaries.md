---
date: 2026-09-01
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - "#hardware/stm32"
---

# STM32 DMA Cache Coherency And ISR Boundaries

## Teknik çekirdek

Özellikle Cortex-M7 sınıfı STM32 türevlerinde DMA ile D-cache aynı RAM bölgesini paylaştığında iki farklı gerçeklik oluşabilir: CPU cache'te yeni görünen veri, DMA'nın eriştiği ana bellekte henüz güncel olmayabilir; veya DMA yeni veriyi RAM'e yazdığı halde CPU eski cache satırını okumaya devam edebilir. Bu nedenle DMA doğru yapılandırılmış olsa bile veri akışı yanlış görünür.

Sorun yalnız cache bakım çağrısı eklemekle bitmez. ISR sınırları da önemlidir. Half-transfer, transfer-complete veya periferal callback zincirinde cache temizleme/geçersiz kılma işlemi yanlış fazda yapılırsa semptom bozulmuş frame, kısmi paket veya "sanki bazen bir önceki buffer okunuyor" biçiminde çıkar. Yani coherency problemi çoğu zaman zamanlama problemidir.

## Mimari davranış

Sağlam mimaride buffer sahipliği açıkça tanımlanır: CPU veriyi hazırlarken DMA dokunmaz; DMA yazarken CPU buffer'ı cache üzerinden tüketmez. Bu protokol, çift tampon veya ring yapısında daha da kritiktir. Aynı buffer üzerinde hem ISR hem task context çalışıyorsa "tamamlandı" sinyalinin hangi anda anlamlı olduğu net olmalıdır.

STM32 tarafında D-cache açık sistemler yüksek throughput verir; fakat bu, her DMA yolunun cache ile dost olduğu anlamına gelmez. Bazı tasarımlar MPU ile non-cacheable bölge ayırır, bazıları temizle/geçersiz kıl stratejisi kullanır. Seçim yanlışsa testte çalışan yol sahada sessiz veri sapmasına dönüşebilir.

## Kritik sınırlamalar

Cache bakım fonksiyonları kendi başına ücretsiz değildir; adres hizalaması ve satır boyu hesabı da doğru olmalıdır. Yanlış aralıkta invalidate çağrısı komşu veriyi etkileyebilir, eksik aralık ise sorunu görünmez kılar. Ayrıca ISR içinde ağır bakım işlemi yapmak latency bütçesini zorlayabilir.

Bir diğer sınır, DMA callback'inde işin fazlasını yapma eğilimidir. Cache bakımı, state güncellemesi, log ve veri parse işi tek callback'e yüklendiğinde periferal zinciri gecikir. Böylece asıl kök neden coherency iken sistemde ikinci bir ISR baskısı oluşur.

## Failure modes

Klasik failure mode, TX tarafında DMA'nın eski veriyi göndermesi; RX tarafında ise CPU'nun yeni gelen verinin eski versiyonunu okumasıdır. Bu durum çoğu zaman deterministik değildir: aynı kod yalnız belirli buffer boyunda veya yük altında bozulur. Başka bir failure mode, çift buffer yapısında callback sınırının yanlış yorumlanmasıyla henüz DMA'nın kullandığı buffer'a CPU'nun tekrar yazmasıdır.

CRC hataları, nadir frame kayması veya yalnızca ilk paketlerin bozuk gelmesi gibi semptomlar da coherency ve ISR sınırı sorunlarına işaret edebilir. Çünkü hata mantıksal değil, veri görünürlüğü seviyesindedir.

## Debug / telemetry / profiling sinyalleri

İyi bir debug stratejisi, aynı veri yolunu önce D-cache kapalı veya non-cacheable bölge ile, sonra mevcut yapı ile çalıştırmaktır. Sorun kayboluyorsa DMA konfigürasyonundan çok coherency protokolü sorgulanmalıdır. Ayrıca half-transfer ve transfer-complete callback zamanlarını ayrı loglamak gerekir; çünkü yanlış fazda işlenen buffer çoğu zaman burada yakalanır.

Profiling tarafında buffer generation counter, callback latency ve CRC/sequence numarası birlikte izlenirse cache bakımının nerede koptuğu görünür. Tek başına periferal hata bayrağı yeterli değildir.

## Doğrulanmış bulgular

- STM32 DMA sorunlarının önemli kısmı "DMA çalışmıyor" değil "cache ve CPU başka veri görüyor" problemidir.
- ISR callback sınırı yanlış seçilirse doğru cache bakımı bile yanlış fazda uygulanır.
- Non-cacheable bölge, temizle/geçersiz kıl stratejisi ve çift tampon sahipliği birlikte düşünülmelidir.
- Nadir veri bozulmaları çoğu zaman mantık hatasından çok coherency sözleşmesinin ihlalidir.

## LokumAI için çıkarım

LokumAI, STM32 tarafında aralıklı paket bozulması veya "DMA bazen eski veriyi yolluyor" türü raporlarda doğrudan HAL sürücüsünü suçlamamalıdır. Retrieval sırasında cache politikası, buffer sahipliği ve callback fazı birlikte sorgulanmalıdır. Özellikle hata düşük frekanslı ve tekrar üretmesi zor ise bu hücre yüksek öncelikli açıklayıcı düğümdür.

Bu not, gözlemi doğru onarıma bağlar: çözüm daha fazla delay eklemek değil, coherency protokolünü ve ISR sınırını açık sözleşmeye dönüştürmektir.

## Sorgu ipuçları

- `stm32 dma cache coherency invalidate clean dcache`
- `stm32 half transfer callback buffer ownership`
- `cortex m7 dma stale data cache`
- `stm32 isr boundary dma double buffer`

## Kaynaklar

- https://www.st.com/content/ccc/resource/technical/document/application_note/group0/08/dd/25/9c/4d/83/43/12/DM00272913.pdf/jcr:content/translations/en.DM00272913.pdf
- https://www.st.com/resource/en/application_note/an4031-using-the-stm32f2-stm32f4-and-stm32f7-series-dma-controller-stmicroelectronics.pdf

[[DRAM_Bandwidth_Utilization]]
[[Instruction_Fetch_Analysis]]
[[Zero_Copy_Buffer_Analysis]]
[[Temporal_Pattern_Recognition]]
