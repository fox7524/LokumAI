---
date: 2026-08-30
tags:
  - dictionary
  - orphan
  - system_core
---

# LokumAI-1.0

Bu dosya **LokumAI Bilişsel Grafik (Cognitive Graph) Ağının** ana dizinidir (Dictionary).
Ağın yerçekimsel çökmesini (Gravity Well / Spaghetti effect) engellemek adına tamamen **bağlantısız (orphan)** olarak bırakılmıştır. Hiçbir düğüme (node) direkt bağlanmaz, hiçbir düğüm de buraya bağlanmaz.

## Sistem Etiketleri (Tag Dictionary)

Aşağıdaki etiketler, Bilişsel RAG (Cognitive RAG) ağındaki sinir hücrelerinin (markdown dosyalarının) görevlerini ve katmanlarını belirler:

### 🧠 Katmanlar (Neural Layers)
- `#layer/input` : Dış dünyadan, sensörlerden, web crawler'dan veya donanımdan (ESP32, UMA) gelen ham verilerin ilk girdiği algı katmanı.
- `#layer/hidden_1_feature_extraction` : Gelen ham verinin özelliklerini çıkaran, gürültüyü filtreleyen ilk gizli katman.
- `#layer/hidden_2_pattern_recognition` : Veriler arasındaki örüntüleri tanıyan, anlamsal bağları kuran derin katman.
- `#layer/hidden_3_logic_synthesis` : Örüntülerden mantıksal sentezler üreten, çıkarım yapan katman.
- `#layer/hidden_4_decision_making` : Mantıksal çıkarımlara göre karar mekanizmalarını çalıştıran son gizli katman.
- `#layer/output` : Kararları aksiyona dönüştüren (Kod üretimi, donanım kontrolü, siber güvenlik alarmı vb.) motor katmanı.

### 📚 RAG ve Öğrenme (Learning & Ingestion)
- `#rag/training` : LokumAI eğitilirken dışarıdan alınan vektör verilerinin işlendiği düğümler.
- `#rag/memory_cell` : Uzun kısa süreli bellek (LSTM) mantığıyla çalışan, geçmiş RAG context'lerini tutan düğümler.
- `#rag/embedding` : Metinlerin veya kodların matematiksel vektör uzayındaki temsilleri.

### ⚙️ Donanım ve Sistem (Hardware & Core)
- `#hardware/apple_mlx` : Apple M5 Pro UMA (Unified Memory Architecture) ve MLX optimizasyonlarını içeren düğümler.
- `#hardware/esp32` : Gömülü sistemler, donanım kesmeleri (interrupts) ve sensör verileri.
- `#system/crypto` : P2P şifreleme, Zero-Knowledge Proofs (ZKP), bellek güvenliği (PAC bypass) ve siber güvenlik işlemleri.

### 🕷️ Otonom Ajanlar (Autonomous Agents)
- `#agent/web_crawler` : İnternetten otonom olarak veri toplayan alt programlar (sub-agents).
- `#agent/analyzer` : Toplanan verileri analiz edip JSON/Markdown formatına çeviren analitik ajanlar.

---
*LokumAI Bilişsel Ağı, M5 Pro 18-Core CPU / 20-Core GPU üzerinde Apple MLX kullanılarak eğitilmek üzere optimize edilmiştir.*
