---
date: 2026-08-30
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - "#hardware/apple_mlx"
---

# MLX Unified Memory Model

## Teknik çekirdek

MLX, Apple Silicon üzerinde klasik "tensoru CPU'dan GPU'ya taşı" modelini değil, aynı fiziksel bellek havuzunu paylaşan bir yürütme modelini kullanır. Diziler oluşturulurken cihaz seçilmez; cihaz seçimi operasyon yürütülürken `stream=mx.cpu` veya `stream=mx.gpu` ile yapılır.

Bu ayrım kritik önem taşır: veri yer değiştirmesi yerine iş yükü yerleştirmesi yapılır. Böylece küçük, gecikme duyarlı işlerin CPU'da; geniş matmul veya attention benzeri yoğun işlerin GPU'da koşturulması aynı veri nesnesi üstünde gerçekleşebilir.

MLX scheduler'ı akışlar arasında veri bağımlılığı oluşursa bunu otomatik olarak ekler. Yani bağımsız işler paralel ilerlerken, bir önceki sonuca bağlı sonraki iş ancak veri hazır olduğunda tetiklenir.

## Doğrulanmış bulgular

- MLX dizileri unified memory içinde yaşar; dizi oluştururken lokasyon pinleme yapılmaz.
- Aynı dizi üzerinde CPU ve GPU işlemleri kopyasız planlanabilir; yürütme cihazı operasyon çağrısında seçilir.
- Bağımlı stream'ler arasında scheduler otomatik dependency ekler; bağımsız stream'ler paralel akabilir.
- Bu model, UMA üzerinde veri kopyası azaltarak compute placement kararını birinci sınıf optimizasyon eksenine çevirir.

## LokumAI için çıkarım

LokumAI tarafında bu hücre, M5 Pro üzerindeki retrieval veya embedding işlerinin neden "önce veriyi taşı, sonra işle" değil "aynı veri üstünde farklı yürütme yolu seç" mantığıyla modellenmesi gerektiğini sabitler. Özellikle graph embedding, token işleme ve küçük/yoğun kernel ayrımında bu not yönlendirici düğüm olarak kullanılmalıdır.

## Sorgu ipuçları

- `mlx unified memory`
- `shared memory arrays`
- `stream dependency`
- `cpu gpu parallel placement`

## Kaynaklar

- https://ml-explore.github.io/mlx/build/html/usage/unified_memory.html

[[Zero_Copy_Buffer_Analysis]]
[[DRAM_Bandwidth_Utilization]]
[[Data_Prefetch_Evaluation]]
