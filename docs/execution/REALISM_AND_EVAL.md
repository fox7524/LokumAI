# “LokumAI neural ağı gerçekçi mi?”

Kısa cevap: **Bu sistem “eğitilmiş bir neural network” değil**, *sembolik + yapısal* bir **bilişsel grafik / politika-orchestrator**. Yani bir LLM gibi kendi başına dil üretip genelleme yapmaz; ama doğru bağlandığında (RAG + policy gate + action surfaces) “gerçek iş” yapabilecek kadar **pratik bir kontrol katmanı** olabilir.

## 1) Yetki / Capability farkı

Bir LLM’nin “yetkisi” iki şeyden gelir:

- **Model kapasitesi**: parametreler, eğitim verisi, genelleme gücü
- **Araç yetkisi**: dosya yazma, komut çalıştırma, API çağırma vs.

LokumAI grafiği ise:

- “model kapasitesi” değil, **policy + gating + audit** kapasitesidir
- “araç yetkisi” varsa, bu yetki **executor üzerinden** tanımlanır (allowlist)

Bu yüzden “AI neural ağı kadar yetkili mi?” sorusunun gerçek cevabı:

- Tek başına: hayır (LLM değil)
- Executor + RAG + sağlam kurallar: **kullanılabilir bir karar/orchestrator** olur

## 2) Gerçeklik kriterleri (neye bakacağız?)

Bir “kullanılabilir sistem” için ölçülebilir metrikler:

- **Determinism**: Aynı vault + aynı paketlerle aynı planın üretilmesi
- **Graph health**: katman geçişleri tutarlı mı, forbidden node referansı var mı
- **Coverage**: H9 paketleri tüm kritik surface’lere route ediyor mu
- **Auditability**: H11 audit notları H10 kararlarını izleyebiliyor mu
- **Action safety**: dış dünyaya dokunan aksiyonlar allowlist dışında kalıyor mu

## 3) Şu an yaptığımız test (kanıt)

Bu repo içinde “gerçek executor” ilk sürüm şu deterministik işleri çalıştırıyor:

- H9’dan `execution_plan.json` üretme
- `quality_validator` raporu üretme
- `layered_projection` çıktısı üretme

Canlı run çıktısı: `docs/execution/live_run/` altında.

## 4) Bir sonraki eşik: “gerçek aksiyon”

Gerçek kullanılabilirlik için iki katman daha lazım:

1. **Action schema**: H9 paketlerinin “ne yapacağını” bir JSON sözleşmesiyle tarif etmek
2. **Capability profile**: Bu aksiyonlardan hangilerinin bu makinede izinli olduğunu açıkça belirtmek

Önerilen güvenli başlangıç aksiyonları:

- `write_reports` (validator raporları)
- `write_projection`
- `write_execution_plan`
- `write_indexes` (opsiyonel; overwrite için ekstra bayrak)

Shell/ESP32 gibi aksiyonlar daha sonra, ayrı capability ile açılmalı.

