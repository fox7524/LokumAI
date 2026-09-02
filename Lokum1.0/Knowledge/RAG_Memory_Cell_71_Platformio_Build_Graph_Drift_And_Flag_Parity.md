---
date: 2026-09-01
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - "#tooling/platformio"
---

# PlatformIO Build Graph Drift And Flag Parity

## Teknik çekirdek

PlatformIO projelerinde "aynı kod ama farklı makinede farklı davranıyor" vakalarının önemli kısmı kaynak koddan değil build graph drift'ten gelir. `platformio.ini` içindeki environment farkları, `build_flags`, `lib_deps`, ekstra script'ler ve varsayılan environment seçimi birbirinden koptuğunda derleme başarılı olsa bile binary semantiği değişebilir. Buna burada flag parity problemi diyoruz.

Drift çoğu zaman dramatik görünmez. Bir env'de `-DUSE_DMA=1` tanımlıdır, diğerinde yoktur; birinde farklı board JSON seçilidir; başka bir env ek `lib_deps` ile farklı sürüm çekmiştir. Build grafiği sessizce ayrıştığında semptom sahada "yalnız release imajı bozuk", "yalnız CI üretimi farklı" veya "sadece bir board varyantı sapıyor" biçiminde belirir.

## Mimari davranış

PlatformIO build sistemi çok katmanlıdır: platform, framework, board manifest, env seçenekleri, library dependency finder ve ekstra script'ler birlikte nihai compile/link çağrısını üretir. Geliştirici yalnız `build_flags` satırına bakarsa resmin küçük kısmını görür. Asıl davranış, hangi env'nin varsayılan olduğu ve o env'nin hangi script/flag/dependency kümesini taşıdığıyla belirlenir.

Flag parity bozulduğunda kod tabanı iki farklı program gibi davranabilir. Üstelik bu fark, kaynak diff'inde görünmez. Aynı commit'ten iki binary üretip davranış farkı gördüğünüzde önce build grafiğinin eşit olup olmadığı kontrol edilmelidir.

## Kritik sınırlamalar

PlatformIO'nun esnekliği aynı zamanda sürüklenme yüzeyi yaratır. `extra_scripts`, `extends`, env override'ları ve auto library çözümleme, küçük ekiplerde bile zamanla görünmez varyasyon üretir. Ayrıca lokal cache ve önceki derleme artıkları yanlış kıyaslamayı besleyebilir; ancak kök neden çoğu zaman cache değil yapılandırma eşitsizliğidir.

Bir diğer sınır, "tek `platformio.ini` var, o halde tek gerçek var" varsayımıdır. Dosya tek olsa da env başına derleme grafiği farklı olabilir. Bu fark belgelenmediyse parity kaybı kaçınılmaz olur.

## Failure modes

En sık failure mode, debug env'de çalışan kodun release veya üretim env'de beklenmedik hata vermesidir. Sorun kod regresyonu sanılır; oysa gerçek fark derleyici tanımları, optimize seviyesi veya kütüphane çözümlemesidir. Başka bir yaygın desen, CI ile lokal üretim arasında makro parity'sinin bozulmasıdır. Derleme geçer, fakat binary içindeki özellik bayrakları değişir.

Board varyantı bazlı sorunlarda da build graph drift belirgindir. Aynı kaynak ağacı farklı board env'lerinde eşit flag taşımıyorsa periferal veya pin konfigürasyonu sapar; hata donanım arızası sanılabilir.

## Debug / telemetry / profiling sinyalleri

İlk adım, karşılaştırılan env'lerin final compile komutları ve tanımlı makrolarını yan yana çıkarmaktır. `platformio run -v` benzeri ayrıntılı çıktı, farkın gerçekten kaynakta mı yoksa build grafiğinde mi olduğunu ayırır. Ayrıca `libdeps` çözümlemesinin env başına hangi sürümleri çektiği görülmelidir.

İyi bir teknik, aynı commit için iki env'nin derleme bayraklarını normalize edip diff almaktır. Eğer davranış farkı makro veya board tanımı farkıyla hizalanıyorsa, kod debug'ına geçmeden parity onarımı yapılmalıdır. CI artefaktlarında derleme meta bilgisini saklamak da uzun vadede yüksek değer üretir.

## Doğrulanmış bulgular

- PlatformIO'da binary davranış farkı çoğu zaman kaynak diff'inden değil env bazlı build graph drift'ten gelir.
- `build_flags`, `lib_deps`, board seçimi ve `extra_scripts` birlikte parity belirler.
- Derleme başarısı parity garantisi değildir; sessiz makro farkları semantiği değiştirebilir.
- Final compile komutu ve makro diff'i, kod regresyonu ile yapılandırma sürüklenmesini ayırmanın en hızlı yoludur.

## LokumAI için çıkarım

LokumAI, "aynı commit farklı yerde farklı davranıyor" raporlarında önce build graph parity incelemesi yapmalıdır. Retrieval yalnız kod diff'ine değil env grafiğine, makro setine ve kütüphane çözümlemesine yöneltilmelidir. Bu hücre, özellikle CI/lokal ayrışması ve çoklu board environment bakımında kritik açıklama düğümüdür.

Öneri de buna göre şekillenmelidir: sorunu yeniden üretmeden önce final derleme bayraklarını ve bağımlılık çözümünü eşleştirmek, çoğu durumda hatayı daha hızlı kapatır.

## Sorgu ipuçları

- `platformio build flags parity environments`
- `platformio libdeps drift extra scripts`
- `platformio run verbose compare compile commands`
- `platformio same code different binary env`

## Kaynaklar

- https://docs.platformio.org/en/latest/projectconf/sections/env/options/build/build_flags.html
- https://docs.platformio.org/en/latest/librarymanager/ldf.html
- https://docs.platformio.org/en/latest/scripting/index.html
- https://docs.platformio.org/en/latest/projectconf/sections/platformio/options/generic/default_envs.html

[[Topology_Analysis]]
[[Behavioral_Feature_Mapping]]
[[Temporal_Pattern_Recognition]]
[[H3_Embedded_Interrupt_DMA_Synthesis]]
