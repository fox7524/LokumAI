---
date: 2026-09-01
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - "#hardware/zephyr"
---

# Zephyr DeviceTree Driver Bringup Failure Modes

## Teknik çekirdek

Zephyr'de bir sürücünün ayağa kalkması yalnız C kodunun derlenmesine bağlı değildir; devicetree node'u, binding şeması, Kconfig seçimi ve device model yaşam döngüsü aynı anda hizalanmalıdır. Bu zincirin herhangi bir halkası eksik olduğunda hata bazen net build failure, bazen de sessizce `device_is_ready()` false dönmesi olarak görünür. Bu yüzden bring-up problemi çoğu zaman "driver bozuk" değil "tanımlama yüzeyi parçalı" problemidir.

Devicetree, Zephyr için salt açıklama dosyası değil, kod üretimi ve init sırasını besleyen bir sözleşmedir. `compatible`, `status`, `reg`, `interrupts`, `pinctrl` veya `gpios` alanlarından biri yanlışsa derleyici her zaman açık hata vermez. Makrolar expand olur, fakat runtime'da cihaz ayağa kalkmaz. Bu sessiz başarısızlık, yeni sürücü getirirken en tehlikeli failure modudur.

## Mimari davranış

Bring-up zinciri dört basamakta okunmalıdır: DTS/DTSI overlay içeriği, binding uyumu, Kconfig enable durumu ve init order. Geliştiriciler çoğu zaman ilk iki basamağa bakıp üçüncüyü ya da dördüncüyü atlar. Oysa doğru `compatible` değeri tek başına yetmez; ilgili driver konfigürasyonu kapalıysa cihaz örneği oluşmaz.

Runtime tarafında `DEVICE_DT_GET()` başarılı gibi görünse bile `device_is_ready()` false kalabilir. Bu desen, compile-time varlık ile runtime hazır olma durumunun farklı şeyler olduğunu hatırlatır. Özellikle clock, reset, bus veya pinctrl bağımlılığı olan sürücülerde zincirleme failure oluşur.

## Kritik sınırlamalar

Zephyr overlay'lerinde bir node'u görünür kılmak kolaydır, fakat binding'in zorunlu property set'i eksikse sonuç yanıltıcı olur. Ayrıca board DTSI dosyasından gelen varsayılan `status = "disabled"` ya da pinctrl çatışması overlay'de beklenmedik öncelik etkisi yaratabilir. Bir diğer sınır, sample uygulamanın çalışmasının sizin driver kombinasyonunuzun çalışacağı anlamına gelmemesidir; çünkü init order ve bağımlılık matrisi farklı olabilir.

Kod tarafında log seviyesini artırmak yardımcıdır, ancak makro expand sonucu üretilen sembolleri okumadan yapılan debug eksik kalır. Zephyr bring-up, konfigürasyon grafiği okumayı gerektirir.

## Failure modes

En tipik failure mode, `DT_NODE_HAS_STATUS` true olduğu halde device'ın ready olmamasıdır. Başka bir sık desen, binding dosyasında beklenen property adının overlay'de farklı yazılması nedeniyle driver'ın eksik konfigürasyonla derlenmesidir. Hata bazen init callback başarısızlığı olarak görülür, bazen tamamen sessiz kalır.

I2C/SPI child node'larında bus tanımı doğru, fakat `cs-gpios`, `irq-gpios` veya clock bağımlılığı eksik olduğunda sürücü kendini "var ama işlevsiz" biçimde gösterebilir. Bu da bring-up süresini uzatır çünkü geliştirici önce iletişim katmanını suçlar.

## Debug / telemetry / profiling sinyalleri

Önce generated devicetree çıktısı ve Kconfig final durumu okunmalıdır; ham overlay dosyasına bakmak tek başına yeterli değildir. `zephyr.dts`, `devicetree_generated.h` ve final `.config` birlikte incelendiğinde düğüm gerçekten nasıl yorumlandı sorusu netleşir. Ardından init log'larında hangi driver instance'ın kaydolduğu kontrol edilmelidir.

İyi bir yöntem, aynı sürücüyü çalışan reference board overlay'iyle diff etmektir. Farkların çoğu kodda değil property, compatible veya Kconfig seviyesinde çıkar. Eğer `device_is_ready()` false ise önce bağımlı bus/clock/reset yolunu sorgulamak gerekir.

## Doğrulanmış bulgular

- Zephyr driver bring-up sorunları çoğu zaman tek dosyalık hata değil, DTS + binding + Kconfig + init-order zinciri problemidir.
- Compile-time node varlığı, runtime readiness garantisi vermez.
- Sessiz başarısızlık en sık yanlış compatible/property veya kapalı driver config kombinasyonunda görülür.
- Generated DTS ve final `.config` okunmadan yapılan debug kolayca yanlış katmana sapar.

## LokumAI için çıkarım

LokumAI, Zephyr cihaz ayağa kalkmıyor raporlarında doğrudan sürücü C koduna atlamamalıdır. Retrieval öncelikle generated devicetree, binding uyumu, `.config` ve init log eksenine kaydırılmalıdır. Bu hücre, "derleniyor ama çalışmıyor" desenini özellikle iyi açıklar.

Ajanın önerisi de buna göre olmalıdır: overlay'i tekrar yazmak yerine önce son üretilen DTS/Kconfig durumunu doğrulamak, sonra runtime readiness zincirini test etmek.

## Sorgu ipuçları

- `zephyr devicetree driver bringup device_is_ready false`
- `zephyr generated dts binding compatible mismatch`
- `zephyr overlay kconfig init order driver`
- `devicetree runtime ready failure modes zephyr`

## Kaynaklar

- https://docs.zephyrproject.org/latest/build/dts/intro.html
- https://docs.zephyrproject.org/latest/build/dts/howtos.html
- https://docs.zephyrproject.org/latest/kernel/drivers/index.html

[[H3_Embedded_Interrupt_DMA_Synthesis]]
[[Topology_Analysis]]
[[Temporal_Pattern_Recognition]]
[[Behavioral_Feature_Mapping]]
