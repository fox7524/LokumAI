---
date: 2026-08-30
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - "#hardware/apple_mlx"
---

# Metal Shared vs Private StorageMode

## Teknik çekirdek

Metal compute dispatch zincirinde iki ayrı karar yüzeyi vardır: buffer'ın storage mode'u ve kernel dispatch geometrisi. `MTLBuffer` kaynağı `storageModeShared` ile CPU-GPU paylaşımına açılabilir; `storageModePrivate` ise GPU odaklı yerleşim tercihidir ve reuse/kopyalama davranışını etkiler.

Dispatch tarafında `dispatchThreads(_:threadsPerThreadgroup:)` arbitrary grid kullanır; Metal gerekli threadgroup sayısını kendisi hesaplar ve gerekiyorsa partial threadgroup üretir. Buna karşılık `dispatchThreadgroups(_:threadsPerThreadgroup:)` grid'i threadgroup sınırlarına hizalı düşünür.

Sonuç olarak zero-copy, resource residency ve dispatch saturation aynı problem değildir. Buffer shared olsa bile yanlış threadgroup geometrisi occupancy, bounds check maliyeti veya kernel saturation üzerinde darboğaz yaratabilir.

## Doğrulanmış bulgular

- `MTLBuffer` genel amaçlı tiplenmemiş bellek tahsisidir ve `storageMode` ile erişim davranışı belirlenir.
- `dispatchThreads` arbitrary grid kabul eder ve gerekirse partial threadgroup üretir.
- `dispatchThreadgroups` hizalı grid dispatch eder; uniform grid doygunluğu için farklı planlama gerektirir.
- Shared/private storage kararı ile dispatch geometry kararı birlikte değerlendirilmelidir; yalnızca buffer modu performansı açıklamaz.

## LokumAI için çıkarım

LokumAI'nin Metal tabanlı hızlandırmalarında gerçek darboğaz bazen veri taşıma değil dispatch geometrisidir. Bu hücre, özellikle future custom MLX/Metal kernel'lerinde resource locality ile compute saturation'ı aynı graf düğümünde bağlamlandırmak için kullanılmalıdır.

## Sorgu ipuçları

- `mtlbuffer storageModeShared`
- `storageModePrivate`
- `dispatchThreads partial threadgroup`
- `threadsPerThreadgroup occupancy`

## Kaynaklar

- https://developer.apple.com/documentation/metal/buffers?changes=_6
- https://developer.apple.com/documentation/metal/mtlcomputecommandencoder/dispatchthreads(_:threadsperthreadgroup:)?language=_8

[[L1_Cache_Hit_Ratio]]
[[L2_Cache_Hit_Ratio]]
[[Zero_Copy_Buffer_Analysis]]
