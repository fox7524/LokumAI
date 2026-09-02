---
date: 2026-08-30
tags:
  - "#index/brain_growth"
  - "#domain/embedded_interrupt_dma"
---

# Embedded and ESP32 Index

## Alanlar

- Üst giriş: [[Brain_Growth_Index]]
- Alan sentezi: [[H3_Embedded_Interrupt_DMA_Synthesis]]
- Kapsam özeti: ESP32, FreeRTOS, ISR ve DMA zincirini watchdog, jitter ve buffering semptomlarına göre düzenler.
- Operasyon ekseni: interrupt latency, cache-disable penceresi, DMA descriptor akışı, queue/task teslim biçimi ve build/runtime parity ilişkisi.
- Karşılaştırmalı corpus: yeni 65-71 kümesi, aynı semptom ailesinin ESP32 dışındaki platform ve araç zinciri izdüşümlerini açar.

## Fazlar

### Faz 1 · Temsilci ham memory-cell girişleri

Temel girişler

- [[RAG_Memory_Cell_04_ESP32_FreeRTOS_SMP_Core_Affinity]]
- [[RAG_Memory_Cell_05_ESP32_Interrupt_Allocation_and_Shared_ISR]]
- [[RAG_Memory_Cell_06_ESP32_DMA_Capable_Memory_and_ISR_Preallocation]]
- [[RAG_Memory_Cell_26_ESP32_IRAM_Safe_ISR_Latency_Budgets]]
- [[RAG_Memory_Cell_27_ESP32_Task_Watchdog_And_Core_Starvation_Patterns]]
- [[RAG_Memory_Cell_28_Freertos_Queue_Sets_Versus_Direct_Task_Notifications]]
- [[RAG_Memory_Cell_29_ESP32_Flash_Cache_Disable_Windows_And_Critical_Paths]]

Orta katman kırılma noktaları

- [[RAG_Memory_Cell_30_GPIO_Matrix_Interrupt_Fan_In_And_Signal_Jitter]]
- [[RAG_Memory_Cell_31_RMT_Peripheral_Timing_Determinism_Under_System_Load]]
- [[RAG_Memory_Cell_32_I2S_DMA_Descriptor_Rings_On_ESP32]]
- [[RAG_Memory_Cell_33_SPI_DMA_Burst_Alignment_And_Cache_Coherency]]

İleri hata ve optimizasyon yüzeyleri

- [[RAG_Memory_Cell_36_PSRAM_Access_Penalties_In_Real_Time_Paths]]
- [[RAG_Memory_Cell_37_Multi_Core_Critical_Sections_And_Spinlock_Contention]]
- [[RAG_Memory_Cell_38_Tickless_Idle_And_Wake_Latency_On_ESP32]]

Bu ilk faz, saf ESP32/FreeRTOS hattını temsil eder. ISR güvenliği, starvation ve DMA descriptor sorunları burada doğrudan okunur; fakat aynı semptomların başka platformlarda nasıl maskelendiğini görmek için ikinci faz gerekir.

### Faz 2 · 65-71 genişletilmiş embedded corpus köprüleri

ESP32 dışı ama aynı hata ailesini aydınlatan yeni corpus notları:

- [[RAG_Memory_Cell_65_ESP32_S3_Vector_Unit_Alignment_And_DMA_Tension]]
- [[RAG_Memory_Cell_66_ESP8266_Nodemcu_Wifi_Timing_And_Watchdog_Pressure]]
- [[RAG_Memory_Cell_67_STM32_DMA_Cache_Coherency_And_ISR_Boundaries]]
- [[RAG_Memory_Cell_68_RP2040_PIO_State_Machine_Timing_Debug]]
- [[RAG_Memory_Cell_69_nRF52_Softdevice_Interrupt_Priority_Constraints]]
- [[RAG_Memory_Cell_70_Zephyr_Devicetree_Driver_Bringup_Failure_Modes]]
- [[RAG_Memory_Cell_71_Platformio_Build_Graph_Drift_And_Flag_Parity]]

Bu küme, aynı saha semptomunu farklı katmanlarda ayrıştırmak için kullanılır:

- DMA hizalama ve staging gerilimi için 65.
- Kooperatif zamanlama ve watchdog baskısı için 66.
- Cache görünürlüğü ile ISR callback fazı için 67.
- Cycle düzeyi zamanlama ve FIFO ritmi için 68.
- Öncelik bandı / radio-stack kısıtı için 69.
- Yapılandırma grafiği / bring-up sessiz kırılması için 70.
- Build graph drift ve env parity sapması için 71.

### Faz 3 · Hidden_3 sentez kapısı

- [[H3_Embedded_Interrupt_DMA_Synthesis]]
- Bu kapı, Embedded and ESP32 alanındaki ham hücreleri mekanizma ailesine göre daraltır.
- Aynı sorguda birden çok semptom varsa önce bu sentez açılır; sonra 26-33 çekirdek kümesi ile 65-71 karşılaştırmalı corpus arasında dallanılır.

### Faz 4 · Kürasyon notu

- Toplam raw hücre: 16
- Bu sayfada görünen temsilci bağlantı: 18
- 26-33 çekirdek ESP32 zinciri doğrudan kürate edilir; 65-71 ise tanı ayrıştırmasını güçlendiren yeni corpus köprüleridir.
- Görünmeyen diğer hücreler sentez kapısı, etiket ve ilgili anchor düğümler üzerinden açılır; amaç tek sayfada omnidump yapmak değil, doğru tanı yüzeyine hızlı inmektir.

## Kullanım

- Kesme gecikmesi, underrun veya cache-disable penceresi anlatılıyorsa bu indeksten ilerle.
- Önce hidden_3 sentezini, sonra temsilci ISR ve DMA hücrelerini aç.
- Belirti platform bağımsız görünüyorsa 65-71 karşılaştırma kümesini kullanarak sorunun zamanlama, cache, interrupt priority, bring-up ya da build parity katmanında mı olduğunu ayır.
- "Aynı kod farklı env'de farklı davranıyor" raporu varsa doğrudan [[RAG_Memory_Cell_71_Platformio_Build_Graph_Drift_And_Flag_Parity]] bağlantısını aç; "derleniyor ama cihaz hazır değil" deseni varsa [[RAG_Memory_Cell_70_Zephyr_Devicetree_Driver_Bringup_Failure_Modes]] ile birlikte düşün.
