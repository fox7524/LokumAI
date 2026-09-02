---
date: 2026-09-01
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - "#hardware/nrf52"
---

# nRF52 SoftDevice Interrupt Priority Constraints

## Teknik çekirdek

nRF52 üzerinde SoftDevice aktifken interrupt öncelikleri artık yalnız uygulamanın tasarım kararı değildir; bazı seviyeler radyo ve stack işleri için rezerve edilir, bazıları ise uygulamaya bırakılır. Bu kısıt ihlal edildiğinde problem derleme aşamasında değil çalışma zamanında görünür: beklenmeyen assert, geciken peripheral ISR veya BLE davranışında düzensizlik.

Kritik nokta, "daha yüksek öncelik her zaman daha güvenli" varsayımının burada yanlış olmasıdır. SoftDevice kendi zaman kritik radyo pencerelerini korur. Uygulama ISR'ı çok agresif öncelik seçerse ya SoftDevice API kısıtlarına çarpar ya da preemption düzeni bozulur. Sonuç doğrudan crash olmayabilir; zamanlama sapması, event gecikmesi ve zor tekrarlanan hata olarak da çıkabilir.

## Mimari davranış

Sağlam mimaride ISR'lar iki sınıfa ayrılır: SoftDevice ile dost, kısa ve sinyal odaklı ISR'lar; bir de thread/context tarafına ertelenmiş ağır işler. nRF52 ekosisteminde bu ayrım özellikle önemlidir çünkü BLE radyo penceresi kısa ama katıdır. GPIOTE, timer veya uygulama periferalinden gelen kesme doğru öncelikte olsa bile ISR içinde fazla iş yapılırsa SoftDevice ile dolaylı yarış oluşur.

Öncelik tablosu stack sürümüne göre küçük farklılıklar gösterebilir. Bu yüzden örneğin başka projeden taşınan "çalışan" IRQ priority değeri yeni SoftDevice sürümünde riskli olabilir. Doğru yaklaşım, API'nin izin verdiği öncelik bandını baz almak ve ağır işi alt katmana itmektir.

## Kritik sınırlamalar

SoftDevice açıkken bazı NVIC işlemleri özel API üzerinden yapılmalıdır; çıplak CMSIS kullanımının her yerde güvenli olduğu varsayılmamalıdır. Ayrıca interrupt önceliği sorunu tek başına görülmez; kritik bölüm uzunluğu, logger kullanımı ve radio event yoğunluğu ile birlikte büyür.

Bir diğer sınır, laboratuvarda düşük trafikle stabil görünen sistemin sahada çoklu bağlantı veya yüksek notify oranında bozulmasıdır. Çünkü öncelik çakışması ancak radyo yoğunluğu arttığında belirginleşebilir.

## Failure modes

En yaygın failure mode, periferal ISR'ın "arada sırada" gecikmesi veya event kaçırmasıdır. Geliştirici periferal sürücüyü suçlar; oysa kök neden SoftDevice rezervasyonuna uygun olmayan öncelik veya ISR içindeki fazla iştir. Başka bir failure mode, SoftDevice API çağrısının yanlış bağlamda yapılmasıyla assert veya error code zinciri oluşmasıdır.

BLE bağlantı aralığı bozulması, notify jitter'ı ve yalnız yük altında çıkan packet loss da dolaylı priority baskısına işaret edebilir. Çünkü sorun buffer değil preemption sırasıdır.

## Debug / telemetry / profiling sinyalleri

İlk kontrol, kullanılan her IRQ için öncelik haritasını çıkarmaktır. Kâğıt üzerinde bu tabloyu görmeden yapılan debug çoğu zaman yanıltıcıdır. Ardından hata yalnız radyo aktifken mi, bağlantı sayısı arttığında mı, yoksa notify trafiği yükseldiğinde mi belirginleşiyor sorusu sorulmalıdır.

ISR süre histogramı ve SoftDevice hata/assert logları birlikte izlenirse sinyal güçlenir. Eğer periferal mantığı doğru görünmesine rağmen BLE yükü arttıkça semptom büyüyorsa sorun büyük olasılıkla priority bandı veya ISR içeriğidir.

## Doğrulanmış bulgular

- SoftDevice aktif nRF52 sistemlerinde interrupt priority seçimi özgür değil, stack kısıtlarıyla sınırlıdır.
- Uygulama ISR'ını aşırı yüksek önceliğe taşımak güvenlik değil çakışma üretir.
- Sorun çoğu zaman yalnızca "yanlış sayı" değil, ISR içinde fazla iş yapılması ve preemption bütçesinin aşılmasıdır.
- BLE yükü arttıkça görünür hale gelen periferal gecikmeleri priority baskısının tipik imzasıdır.

## LokumAI için çıkarım

LokumAI, nRF52 sahasından gelen "BLE açıkken periferal kararsız" vakalarını değerlendirirken sürücü/uygulama hatası ile SoftDevice priority ihlalini ayırmalıdır. Retrieval önce IRQ tablosu, SoftDevice API bağlamı ve ISR süresi ekseninde yapılmalıdır. Bu hücre özellikle düşük tekrar oranlı ama radyo yüküne hassas hataları açıklamak için önemlidir.

Ajanın önerisi, önceliği körlemesine yükseltmek değil; doğru priority bandına dönmek, ISR'ı kısaltmak ve ağır işi thread/context'e ertelemek olmalıdır.

## Sorgu ipuçları

- `nrf52 softdevice interrupt priority application irq`
- `softdevice nvic reserved priorities`
- `nrf52 ble peripheral interrupt jitter`
- `softdevice api wrong interrupt priority`

## Kaynaklar

- https://devzone.nordicsemi.com/cfs-file/__key/support-attachments/beef5d1b77644c448dabff31668f3a47-27893fd63c424bf38fdd8d272a0e46bf/8524.S140_5F00_SDS_5F00_v2.1.pdf
- https://docs-be.nordicsemi.com/bundle/sds_s112/attach/S112_SDS_v3.1.pdf?_LANG=enus

[[Context_Switch_Monitor]]
[[Temporal_Pattern_Recognition]]
[[Behavioral_Feature_Mapping]]
[[Packet_Header_Parsing]]
