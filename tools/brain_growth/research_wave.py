from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.brain_growth.common import (
    KNOWLEDGE_DIR,
    allowed_forward_targets,
    assert_link_target_layer_membership,
    assert_no_forbidden_nodes,
    build_note_filename,
    parse_wikilinks,
)


APPLE_TOPICS = [
    {
        "title": "MLX Lazy Evaluation and Stream Dependency Barriers",
        "summary": "MLX işlemleri sonucu hemen gerçekleştirmek yerine gözlem anına kadar erteleyebilir; bu yüzden Apple Silicon üzerinde asıl kritik konu veri kopyası değil stream bağımlılığı ve realization sınırıdır.",
        "boundary": "Host okuması, DLPack paylaşımı ve karışık CPU/GPU erişimi gizli senkronizasyon maliyetlerini görünür hale getirir.",
        "retrieval": "Beklenmeyen yavaşlama, stale sonuç veya ani barrier maliyeti görüldüğünde bu hücre geri çağrılmalıdır.",
    },
    {
        "title": "Metal Heap Residency and Buffer Alias Reuse",
        "summary": "Metal heap kullanımı, yaşam döngüsü çakışmayan buffer'ların aynı fiziksel rezervasyonu paylaşmasına izin vererek tahsis baskısını ve parçalanmayı azaltabilir.",
        "boundary": "Alias reuse yanlış yaşam döngüsü varsayımıyla yapılırsa eski veri görünürlüğü ve overwrite riski oluşur.",
        "retrieval": "Aynı iş hattında çok sayıda geçici tensor oluşuyorsa heap residency notu doğrudan ilişkilidir.",
    },
    {
        "title": "Apple Silicon UMA Pressure and Page Migration Signals",
        "summary": "Apple Silicon UMA, CPU ve GPU arasında tek adres alanı sunsa da baskı arttığında sayfa erişim örüntüsü efektif bant genişliğini ve erişim gecikmesini belirler.",
        "boundary": "Büyük KV cache, video buffer ve model aktivasyonları aynı anda yükseldiğinde locality bozulur ve faydalı shared-memory hissi azalır.",
        "retrieval": "Bant genişliği daralması, token başına gecikme artışı veya cache thrash sinyali görüldüğünde bu not önem kazanır.",
    },
    {
        "title": "MLX Graph Capture and Kernel Fusion Boundaries",
        "summary": "MLX tarafında kernel fusion kazancı, operasyon zincirinin hangi noktada materyalize edildiğine ve farklı backend sınırlarının fusion zincirini nerede kırdığına bağlıdır.",
        "boundary": "Shape değişimi, debugging amaçlı ara okuma ve frameworkler arası interop çoğu zaman fusion zincirini beklenmedik yerde böler.",
        "retrieval": "Aynı matematiksel iş yükü teorik olarak hafif görünürken pratikte fazla kernel sayısı üretiyorsa bu hücre kullanılmalıdır.",
    },
    {
        "title": "Metal Argument Buffers for Batched Dispatch Coordination",
        "summary": "Argument buffer yaklaşımı, çok sayıda kaynak tanımını tek seferde encode ederek dispatch başına CPU tarafı kurulum yükünü düşürür.",
        "boundary": "Kaynak yaşam döngüsü ve offset düzeni disiplinli tutulmazsa karmaşık descriptor topolojisi hata ayıklamayı zorlaştırır.",
        "retrieval": "Çoklu kernel dispatch sırasında encode overhead baskın hale gelirse bu not öne çıkar.",
    },
    {
        "title": "MPS versus MLX Execution Surface Selection",
        "summary": "Aynı Apple GPU üzerinde MPS ve MLX farklı soyutlama seviyeleri sunar; seçim, operatör kapsaması ile kontrol yüzeyi arasındaki dengeye dayanır.",
        "boundary": "Backend karışımı arttıkça veri görünürlüğü, debug ergonomisi ve performans tahmin edilebilirliği birlikte zorlaşır.",
        "retrieval": "Bir model parçasının hangi Apple kütüphanesinde kalması gerektiği tartışıldığında bu düğüm bağlam sağlar.",
    },
    {
        "title": "AMX Neural Engine and GPU Scheduling Tradeoffs",
        "summary": "Apple ekosisteminde AMX, Neural Engine ve GPU farklı throughput-precision profilleri taşır; doğru yerleştirme iş yükünün matris biçimine ve gecikme hedeflerine bağlıdır.",
        "boundary": "Yanlış hızlandırıcı seçimi toplam throughput'u artırırken uçtan uca latency veya dönüştürme maliyetini yükseltebilir.",
        "retrieval": "Operatör yerleşimi ve hızlandırıcı seçimi konuşuluyorsa bu hücre bir karar ayracı gibi çalışır.",
    },
    {
        "title": "Metal Command Buffer Commit Latency and Queue Depth",
        "summary": "Command buffer commit davranışı yalnızca GPU işini başlatmaz; kuyruk derinliği, batched commit ve completion takibi birlikte algılanan gecikmeyi belirler.",
        "boundary": "Aşırı küçük commit paketleri CPU tarafını boğarken aşırı büyük paketler de interaktif yanıt gecikmesini yükseltebilir.",
        "retrieval": "Profil çıktısında encode ucuz ama submit pahalı görünüyorsa bu not devreye alınmalıdır.",
    },
    {
        "title": "Unified Memory Backpressure in Token Streaming Pipelines",
        "summary": "Token akışı sırasında attention cache, logits ve post-processing tamponları aynı unified memory yüzeyinde yarıştığında backpressure oluşabilir.",
        "boundary": "Düşük batch ile iyi görünen iş hattı uzun oturum veya paralel istek altında aniden dar boğaza girebilir.",
        "retrieval": "Uzayan sohbetlerde zamanla büyüyen bellek baskısı incelenirken bu hücre önemlidir.",
    },
    {
        "title": "Zero Copy Tensor Interop between MLX and PyTorch",
        "summary": "DLPack tabanlı interop, private olmayan Metal buffer'larda zero-copy imkânı verebilir; fakat sahiplik ve yaşam döngüsü yanlış yönetilirse avantaj correctness riskine döner.",
        "boundary": "External mutation, gradient beklentisi ve buffer mode uyumsuzluğu interop'u sessizce kopyalı yola itebilir.",
        "retrieval": "Bir tensor farklı frameworklerde dolaşıyorsa ve beklenmedik copy overhead oluşuyorsa bu not kullanılmalıdır.",
    },
    {
        "title": "Sparse Attention on Apple Silicon Memory Budget",
        "summary": "Sparse attention teorik hesap yükünü düşürse de Apple Silicon üzerinde asıl kazanç, düzensiz erişim örüntüsünün memory budget ile nasıl uzlaştığına bağlıdır.",
        "boundary": "Daha az FLOP her zaman daha iyi throughput anlamına gelmez; locality bozulursa sparse yaklaşım avantajını kaybedebilir.",
        "retrieval": "Attention optimizasyonu kâğıt üstünde iyi ama cihaz üzerinde tutarsızsa bu hücre açıklayıcı olur.",
    },
    {
        "title": "Quantized KV Cache Placement on UMA",
        "summary": "Quantized KV cache, unified memory tüketimini düşürürken erişim desenini ve dequantization maliyetini yeniden şekillendirir.",
        "boundary": "Aşırı agresif quantization, bant genişliği tasarrufu sağlasa da uzun bağlam doğruluğunu ve decode akışını bozabilir.",
        "retrieval": "Uzun context maliyeti ile kalite kaybı birlikte değerlendiriliyorsa bu not gereklidir.",
    },
    {
        "title": "Metal Resource Hazard Tracking and Explicit Fencing",
        "summary": "Metal hazard tracking birçok yarış durumunu gizlice yönetebilir; ancak paylaşılan kaynaklar ve farklı encoder türleri birleşince explicit fencing yine de kritik hale gelir.",
        "boundary": "Otomatik güvenlik ağına aşırı güvenmek, karmaşık command graph içinde nondeterministic görünürlük sorunları bırakabilir.",
        "retrieval": "Nadiren tekrar eden veri bozulması veya sıra bağımlı hata imzası görüldüğünde bu hücre çağrılmalıdır.",
    },
]

EMBEDDED_TOPICS = [
    {
        "title": "ESP32 IRAM Safe ISR Latency Budgets",
        "summary": "ESP32 üzerinde IRAM-safe ISR tasarımı, flash cache duraklamaları sırasında bile kesme yolunun öngörülebilir kalmasını sağlar.",
        "boundary": "ISR içinde IRAM dışı çağrı veya heap kullanımı gecikmeyi sıçratabilir ve nadir ama kritik timeout'lar üretebilir.",
        "retrieval": "Sistem yalnızca bazı flash veya Wi-Fi anlarında kesme kaçırıyorsa bu hücre ilişkilidir.",
    },
    {
        "title": "ESP32 Task Watchdog and Core Starvation Patterns",
        "summary": "Task watchdog sinyalleri çoğu zaman tek bir sonsuz döngüden değil, core affinity ve uzun kritik bölgelerin yarattığı starvation örüntüsünden kaynaklanır.",
        "boundary": "Bir core'un housekeeping yükleri birikirse diğer task'lar sağlıklı görünse bile watchdog reset tetiklenebilir.",
        "retrieval": "Reset logları sporadik watchdog taşmaları gösteriyorsa bu düğüm inceleme başlangıcıdır.",
    },
    {
        "title": "FreeRTOS Queue Sets versus Direct Task Notifications",
        "summary": "Queue set yapısı çoklu bekleme kaynağını sadeleştirir; direct task notification ise daha az overhead ile tek alıcıyı hızlı uyandırır.",
        "boundary": "Yanlış primitive seçimi driver kodunu gereksiz yere ağırlaştırabilir veya olay birleşimini yönetilemez kılabilir.",
        "retrieval": "Senkronizasyon primitive seçimi tartışılırken bu not karar matrisine dönüşür.",
    },
    {
        "title": "ESP32 Flash Cache Disable Windows and Critical Paths",
        "summary": "Flash işlemleri sırasında cache disable pencereleri, ISR ve zaman hassas kodun hangi bellek bölgesinde durduğunu aniden önemli hale getirir.",
        "boundary": "Normal akışta güvenli görünen fonksiyon zinciri, flash erase veya OTA sırasında deterministik davranışını kaybedebilir.",
        "retrieval": "OTA ya da log flush esnasında ortaya çıkan latency sıçramalarında bu hücre kullanılmalıdır.",
    },
    {
        "title": "GPIO Matrix Interrupt Fan In and Signal Jitter",
        "summary": "GPIO matrix esnek routing sağlar ancak çok sayıda sinyal kaynağını aynı kesme yüzeyinde toplamak jitter ve hata ayıklama karmaşıklığını artırabilir.",
        "boundary": "Mantıksal olarak bağımsız olaylar tek interrupt baskısı altında birleştiğinde root-cause görünürlüğü azalır.",
        "retrieval": "Giriş tarafında düzensiz event sırası veya ölçülemeyen jitter varsa bu not faydalıdır.",
    },
    {
        "title": "RMT Peripheral Timing Determinism under System Load",
        "summary": "RMT çevre birimi zamanlamayı donanım seviyesinde rahatlatır; fakat refill, interrupt ve görev zamanlaması yine de yük altında deterministik sınırlar üretir.",
        "boundary": "Uzun pulse zincirleri veya yüksek kesme baskısı altında kullanıcı kodu besleme hızını tutturamazsa timing drift başlar.",
        "retrieval": "IR, LED veya hassas pulse üretiminde yük altında bozulma görülürse bu hücre hedeflenmelidir.",
    },
    {
        "title": "I2S DMA Descriptor Rings on ESP32",
        "summary": "I2S DMA descriptor ring tasarımı, ses veya veri akışının kopmadan sürmesi için burst boyu, buffer sayısı ve ISR servis süresi arasında denge kurar.",
        "boundary": "Az descriptor düşük gecikme verirken underrun riskini artırır; çok descriptor ise bellek ve geri basınç maliyeti doğurur.",
        "retrieval": "Akış kopması veya periyodik ses tıklaması inceleniyorsa bu not kullanılır.",
    },
    {
        "title": "SPI DMA Burst Alignment and Cache Coherency",
        "summary": "SPI DMA hattında burst alignment, buffer yerleşimi ve cache görünürlüğü birlikte ele alınmadığında throughput beklenenden düşük kalabilir.",
        "boundary": "Yanlış hizalanmış veya DMA-capable olmayan buffer'lar sessiz kopyalara ya da yeniden paketleme maliyetine neden olur.",
        "retrieval": "SPI üzerinden teorik bant genişliğine ulaşılamıyorsa bu düğüm açıklayıcıdır.",
    },
    {
        "title": "UART ISR Backpressure and Ring Buffer Design",
        "summary": "UART alım yolunda ISR, ring buffer ve kullanıcı task'ı arasındaki hız dengesi bozulursa backpressure önce küçük kayıplar, sonra bütün akış bozulması üretir.",
        "boundary": "Burst halinde gelen veri, düşük hızda boşaltılan tamponla birleştiğinde framing hataları ve parse kopmaları artar.",
        "retrieval": "Seri port bazen düzgün bazen eksik veri taşıyorsa bu not geri çağrılmalıdır.",
    },
    {
        "title": "FreeRTOS Event Groups versus Semaphores for Driver States",
        "summary": "Event group yapıları çoklu bit tabanlı durum taşırken semaforlar belirli el sıkışmalar için daha yalın bir yol sunar.",
        "boundary": "Sürücü durumu büyüdükçe event group okunabilirliği düşebilir; tersine basit el sıkışmada semafor fazladan yapı gerektirmez.",
        "retrieval": "Driver state machine karmaşıklaşıp sinyal modeli bulanıklaştığında bu hücre karar yardımı verir.",
    },
    {
        "title": "PSRAM Access Penalties in Real Time Paths",
        "summary": "PSRAM kapasite kazandırır ama gerçek zamanlı yol içine sokulduğunda erişim gecikmesi ve DMA kısıtları nedeniyle kritik patikayı zayıflatabilir.",
        "boundary": "Büyük buffer'ları PSRAM'e atmak rahatlatıcı görünse de ISR yakınındaki veri için yanlış seçim olabilir.",
        "retrieval": "Sistem yük altında aniden tepki kaybediyor ancak RAM kullanım grafiği sağlıklı görünüyorsa bu not incelenmelidir.",
    },
    {
        "title": "Multi Core Critical Sections and Spinlock Contention",
        "summary": "ESP32 çok çekirdekli kritik bölgeler, doğru spinlock disiplini olmadan görünmez bekleme cepleri ve priority inversion benzeri etkiler doğurabilir.",
        "boundary": "Kısa görünen kritik bölge iki core arasında sık tekrarlandığında toplam jitter beklenenden büyük olur.",
        "retrieval": "İki çekirdekli çalışmada yalnızca yük altında görülen gecikme varyansı için bu hücre kullanılır.",
    },
    {
        "title": "Tickless Idle and Wake Latency on ESP32",
        "summary": "Tickless idle enerji tasarrufu sağlar ancak wake latency hedefleri sıkıysa zamanlama planını ve alarm kaynaklarını yeniden düşünmek gerekir.",
        "boundary": "Derin uykuya yakın davranışlar, bekleme kazanımı sunarken kısa tepki süresi isteyen olayları cezalandırabilir.",
        "retrieval": "Enerji optimizasyonu sonrası olay cevabı yavaşladıysa bu not durumu çerçeveler.",
    },
]

SECURITY_TOPICS = [
    {
        "title": "Pointer Authentication Key Domains and Signing Contexts",
        "summary": "Pointer Authentication yalnızca bir imza biti eklemekten ibaret değildir; hangi anahtar alanının ve bağlam bilgisinin kullanıldığı saldırı yüzeyini doğrudan değiştirir.",
        "boundary": "Yanlış modelleme, PAC'i mutlak koruma gibi gösterir ve geçersiz pointer sınıflarını aynı sepete atar.",
        "retrieval": "PAC logları okunurken bağlam, anahtar alanı ve pointer türü ayrıştırılmak istendiğinde bu hücre kullanılmalıdır.",
    },
    {
        "title": "Control Flow Integrity and PAC Complementarity",
        "summary": "PAC, control-flow integrity ile aynı şey değildir; biri pointer bütünlüğüne odaklanırken diğeri yürütme grafiğinin geçerli yollarını sınırlar.",
        "boundary": "Bu iki korumayı tek savunma katmanı gibi düşünmek, hangi ihlalin hangi primitive ile yakalanacağını bulanıklaştırır.",
        "retrieval": "Bir bütünlük savunmasının kapsamadığı saldırı yolu tartışılıyorsa bu not önemlidir.",
    },
    {
        "title": "Use After Free Telemetry and Crash Clustering",
        "summary": "Use-after-free hataları çoğu zaman tekil çökme imzası vermez; allocator davranışı ve yeniden kullanım paterni crash kümelenmesini değiştirir.",
        "boundary": "Yüzeyde birbirinden farklı crash logları aslında aynı yaşam döngüsü bozulmasının varyantları olabilir.",
        "retrieval": "Dağınık görünen crash ailesini tek köke indirmek gerektiğinde bu hücre geri çağrılır.",
    },
    {
        "title": "Heap Metadata Corruption Signatures",
        "summary": "Heap metadata bozulması, uygulama mantığından önce allocator invariant'larını kırdığı için semptomlarını daha üst katmanlarda ama sebeplerini çok daha altta gösterir.",
        "boundary": "Bozulma anı ile çökme anı arasındaki zaman farkı root-cause analizini zorlaştırır.",
        "retrieval": "Rastgele görünen bellek çöküşlerinde metadata imzası aranıyorsa bu not gereklidir.",
    },
    {
        "title": "Stack Canary Failure Telemetry and Triage",
        "summary": "Stack canary tetiklenmesi, overflow'un büyüklüğünü değil dönüş yoluna ya da kritik çerçeveye kadar ulaşıldığını bildirir.",
        "boundary": "Canary alarmını yalnızca derin exploit göstergesi saymak, daha basit fakat sık tekrarlanan taşmaları gözden kaçırabilir.",
        "retrieval": "Crash triage sırasında stack smash ile diğer pointer bozulmalarını ayırmak için bu hücre kullanılır.",
    },
    {
        "title": "Secure Enclave Boundaries and Key Ladder Separation",
        "summary": "Secure Enclave yaklaşımı, anahtar kullanımını genel işlem bağlamından ayırarak veri erişimi ile gizli malzeme kullanımını farklı güven sınırlarına taşır.",
        "boundary": "Uygulama, enclave dışında kalan metadata veya policy bilgisini yanlış korursa anahtar izolasyonu tek başına yeterli olmaz.",
        "retrieval": "Kriptografik anahtar kullanımının hangi güven sınırında tutulacağı sorulduğunda bu not yol gösterir.",
    },
    {
        "title": "AEAD Nonce Reuse Failure Modes",
        "summary": "AEAD şemalarında nonce tekrar kullanımı, yalnızca teorik bir hijyen hatası değil gizlilik ve bütünlük varsayımlarını aynı anda zayıflatan temel bir bozulmadır.",
        "boundary": "Dağıtık üreticiler veya yeniden başlatma senaryoları nonce koordinasyonunu sessizce kırabilir.",
        "retrieval": "Oturum şifreleme tasarımında sayaç, rastgelelik ve yeniden başlatma ilişkisi sorgulanıyorsa bu not seçilmelidir.",
    },
    {
        "title": "Zero Knowledge Proof Witness Exposure Surfaces",
        "summary": "ZKP tasarımında ispatlayıcı mantık doğru olsa bile witness üretim hattı, trace logları ve ara veri tamponları gizli yüzeyler oluşturabilir.",
        "boundary": "Kriptografik protokol güvenli görünürken uygulama katmanındaki gözlemlenebilir izler sır sızıntısı doğurabilir.",
        "retrieval": "Kanıt sistemi uygulanırken çevresel telemetry sızıntıları değerlendiriliyorsa bu hücre kullanılır.",
    },
    {
        "title": "Merkle Commitments for Retrieval Integrity",
        "summary": "Merkle commitment, retrieval çıktısının hangi içerik tabanına bağlandığını denetlenebilir hale getirerek kaynak bütünlüğü için hafif bir doğrulama yüzeyi sunar.",
        "boundary": "Commitment varsa bile kök hash güncelleme ve dağıtım disiplini bozuksa güven zinciri eksik kalır.",
        "retrieval": "Bilgi tabanı bütünlüğü veya kanıtlanabilir alıntı gereksinimi konuşulurken bu not yararlıdır.",
    },
    {
        "title": "Forward Secrecy in Peer to Peer Session Rotation",
        "summary": "P2P oturumlarda forward secrecy, eski anahtar sızsa bile geçmiş trafiğin açılmamasını hedefler; bunun için anahtar dönüşüm ritmi ve yeniden anahtarlama mantığı önemlidir.",
        "boundary": "Uzun yaşayan oturumlar veya düşük kaliteli yeniden anahtarlama tasarımı geçmiş trafiği gereksiz yere geniş bir riske maruz bırakır.",
        "retrieval": "Oturum döndürme politikasının güvenlik maliyeti inceleniyorsa bu hücre devreye alınmalıdır.",
    },
    {
        "title": "Remote Attestation Signals for Edge Nodes",
        "summary": "Remote attestation, uç düğümün hangi yazılım ve ölçüm durumu ile çalıştığını merkezi tarafa raporlayarak güven zinciri oluşturur.",
        "boundary": "Attestation sinyalini almak yetmez; doğrulayan tarafın kabul politikası ve ölçüm güncelliği zayıfsa karar kalitesi düşer.",
        "retrieval": "Dağıtık edge bileşenlerinin güvenilir çalıştığını nasıl ispatlayacağı soruluyorsa bu not uygundur.",
    },
    {
        "title": "Memory Disclosure versus Code Reuse Attack Paths",
        "summary": "Bellek ifşası ve code-reuse saldırıları farklı ilk semptomlar verse de çoğu zaman aynı hata ailesinin iki farklı kullanım biçimidir.",
        "boundary": "Savunma yalnızca kontrol akışına odaklanırsa bilgi sızdıran fakat hemen çökmeyen hatalar yeterince izlenmeyebilir.",
        "retrieval": "Bir açığın veri ifşası mı yoksa yürütme sapması mı ürettiği ayrıştırılırken bu hücre etkindir.",
    },
    {
        "title": "Crash Triage for Memory Safety Regressions",
        "summary": "Bellek güvenliği regresyonları versiyonlar arasında sessizce taşınabilir; etkili triage için crash kümeleri, değişiklik yüzeyi ve allocator davranışı birlikte okunmalıdır.",
        "boundary": "Sadece son stack trace'e bakmak tekrar eden regresyon ailesini parçalara bölerek görünmez kılar.",
        "retrieval": "Yeni sürümle birlikte artan bellek hataları sınıflandırılırken bu not anahtar görevi görür.",
    },
]

AI_TOPICS = [
    {
        "title": "Hybrid Sparse Dense Graph Retrieval",
        "summary": "Hybrid sparse+dense retrieval, grafik komşuluğu ile semantik benzerliği ayrı sinyaller olarak toplar ve tek başına birinin kaçırdığı düğümleri geri alabilir.",
        "boundary": "Ağırlıklandırma kötü yapılırsa sparse taraf popüler düğümlere, dense taraf ise yüzeysel benzerliğe aşırı yaslanabilir.",
        "retrieval": "Graph RAG'de recall ile precision aynı anda yükseltilmek istendiğinde bu hücre seçilir.",
    },
    {
        "title": "Graph Expansion Budgeting and Beam Search",
        "summary": "Graph expansion budgeting, traversal derinliğini değil toplam dallanma maliyetini kontrol ederek context penceresini yönetilebilir tutar.",
        "boundary": "Bütçesiz genişleme, faydalı komşuluk yerine gürültü zinciri üretir ve yanıtı seyreltebilir.",
        "retrieval": "Çok-hop sorgularda graph büyümesi patlıyorsa bu not karar kılavuzu olur.",
    },
    {
        "title": "Query Decomposition for Multi Hop Retrieval",
        "summary": "Sorgu dekompozisyonu, tek bir geniş arama yerine ara hedefler tanımlayarak multi-hop retrieval'i daha ölçülebilir adımlara böler.",
        "boundary": "Kötü dekompozisyon, doğru cevabı taşıyan yolu kırabilir ve hata zincirini ilk adımda başlatabilir.",
        "retrieval": "Sorgu tek parça halinde çözülemiyor fakat alt sorulara ayrılabiliyorsa bu hücre kullanılmalıdır.",
    },
    {
        "title": "Edge Reweighting from Retriever Feedback",
        "summary": "Retriever geri bildirimi ile edge reweighting yapmak, statik graph yapısını canlı kullanım sinyaline göre düzeltir.",
        "boundary": "Kısa dönemli sorgu trendlerine fazla uyum sağlamak, uzun vadeli bilgi topolojisini bozabilir.",
        "retrieval": "Bağlantı ağı veri değişmeden eskiyor gibi görünüyorsa bu not açıklama sunar.",
    },
    {
        "title": "Temporal Edges in Episodic Memory Graphs",
        "summary": "Episodic memory graph içinde temporal edge'ler, yalnızca neyin ilişkili olduğunu değil hangi sırayla bağlandığını da retrieval sinyaline dönüştürür.",
        "boundary": "Zaman boyutu ihmal edilirse aynı düğümler doğru olsa bile yanlış sırada bir anlatı kurulabilir.",
        "retrieval": "Olay dizisi, neden-sonuç akışı veya oturum geçmişi sorgularında bu hücre önemlidir.",
    },
    {
        "title": "Entity Resolution as Graph Construction Discipline",
        "summary": "Entity resolution yalnızca veri temizliği değildir; graph'in düğüm kimliğini doğru kurarak sonraki tüm traversal kalitesini belirler.",
        "boundary": "Birden fazla adla anılan aynı varlık çözülmezse multi-hop yol parçalanır; yanlış birleştirme yapılırsa bilgi karışır.",
        "retrieval": "Aynı kavram farklı belgelerde farklı adla geçiyorsa bu not devreye girer.",
    },
    {
        "title": "Cross Encoder Reranking after Graph Traversal",
        "summary": "Traversal sonrası cross-encoder reranking, ulaşılmış adayları sorgu bağlamında yeniden sıralayarak graph recall'ını cevap kalitesine dönüştürür.",
        "boundary": "Reranker bütçesi sınırlıysa yanlış aday havuzu üzerine harcanan maliyet toplam sistemi yavaşlatır.",
        "retrieval": "Traversal iyi fakat son bağlam seçimi zayıfsa bu hücre seçilmelidir.",
    },
    {
        "title": "Subgraph Packing for Context Window Control",
        "summary": "Subgraph packing, seçilen düğümleri düz liste yerine yapısal bütünlük koruyarak context penceresine sığdırma problemidir.",
        "boundary": "Yalnızca en yüksek skorlu parçaları almak, açıklayıcı köprü düğümleri dışarıda bırakıp reasoning zincirini kesebilir.",
        "retrieval": "Context window sınırlı ama ilişki zinciri korunmak zorundaysa bu not kullanılır.",
    },
    {
        "title": "Semantic Drift Detection in Graph RAG",
        "summary": "Semantic drift, düğüm ilişkileri korunuyor görünse bile zamanla kenar anlamının sorgu niyetiyle hizasını kaybetmesi durumudur.",
        "boundary": "Eski etiketler ve sabit edge'ler güncel kavram haritasını yansıtmazsa retrieval isabeti sessizce düşer.",
        "retrieval": "Doğru belgeler var ama yanlış çağrışımlar ön plana çıkıyorsa bu hücre ilişkilidir.",
    },
    {
        "title": "Negative Sampling for Relation Aware Embeddings",
        "summary": "Relation-aware embedding eğitiminde negative sampling kalitesi, hangi komşuluğun gerçekten ayırt edildiğini belirler.",
        "boundary": "Kolay negatifler modelin ilişkisel ayırım gücünü şişirir ama gerçek retrieval zorluğunu temsil etmez.",
        "retrieval": "Embedding iyi metrik verip sahada zayıf davranıyorsa bu not açıklama sağlar.",
    },
    {
        "title": "Graph Neighborhood Pruning under Token Budgets",
        "summary": "Neighborhood pruning, çok-hop grafikte her komşuyu taşımak yerine hangi dalların token bütçesine değdiğini seçer.",
        "boundary": "Aşırı agresif budama zinciri kırar; gevşek budama ise bağlamı gürültü ile doldurur.",
        "retrieval": "Token bütçesi sert ama çok-hop bilgi korunacaksa bu hücre çağrılmalıdır.",
    },
    {
        "title": "Tool Augmented Retrieval Routing Policies",
        "summary": "Tool-augmented routing, graph traversal kararını yalnızca embedding skoruna değil dış araç, hesaplama ve doğrulama ihtiyacına göre de verir.",
        "boundary": "Her sorguya araç çağırmak maliyet patlatır; hiç çağırmamak ise doğrulama gerektiren sorularda kalite düşürür.",
        "retrieval": "Araç kullanımının retrieval ile ne zaman birleşeceği tartışmasında bu not anahtar rol oynar.",
    },
    {
        "title": "Citation Grounding across Multi Source Reasoning",
        "summary": "Multi-source reasoning içinde citation grounding, farklı düğümlerden gelen iddiaların hangi kanıta dayandığını zincir kaybetmeden taşımalıdır.",
        "boundary": "Kaynak zinciri kırılırsa doğru cevap bile denetlenemez ve sistem güvenilir görünmez.",
        "retrieval": "Bir cevap çok kaynaktan besleniyor ama izlenebilir alıntı gerekiyorsa bu not kullanılmalıdır.",
    },
]


DOMAIN_BUNDLES: list[dict[str, Any]] = [
    {
        "key": "apple_mlx",
        "label": "Apple Silicon / MLX",
        "tag": '"#hardware/apple_mlx"',
        "focus": "buffer locality, dispatch ve unified memory davranışı",
        "hint_seed": "apple silicon mlx",
        "sources": [
            "https://ml-explore.github.io/mlx/build/html/usage/unified_memory.html",
            "https://ml-explore.github.io/mlx/build/html/usage/numpy.html",
            "https://developer.apple.com/documentation/metal/buffers",
            "https://developer.apple.com/documentation/metal/mtlcommandbuffer",
        ],
        "anchors": [
            "Zero_Copy_Buffer_Analysis",
            "DRAM_Bandwidth_Utilization",
            "Data_Prefetch_Evaluation",
            "L1_Cache_Hit_Ratio",
            "L2_Cache_Hit_Ratio",
            "GPU_Performance_Counters",
            "Cache_Miss_Detector",
            "Context_Switch_Monitor",
        ],
        "topics": APPLE_TOPICS,
    },
    {
        "key": "embedded_esp32",
        "label": "Embedded / ESP32",
        "tag": '"#hardware/esp32"',
        "focus": "latency, DMA ve kesme disiplini",
        "hint_seed": "esp32 freertos dma",
        "sources": [
            "https://docs.espressif.com/projects/esp-idf/en/v5.3.5/esp32p4/api-reference/system/freertos_idf.html",
            "https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/system/intr_alloc.html",
            "https://docs.espressif.com/projects/esp-idf/en/v5.2.7/esp32s3/api-reference/system/mem_alloc.html",
            "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/wdts.html",
            "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/rmt.html",
            "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/i2s.html",
            "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/spi_master.html",
            "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/uart.html",
        ],
        "anchors": [
            "Behavioral_Feature_Mapping",
            "Instruction_Fetch_Analysis",
            "Packet_Header_Parsing",
            "Memory_Leak_Fingerprinting",
            "Context_Switch_Monitor",
            "Temporal_Pattern_Recognition",
            "Cross_Correlation_Matrix",
            "DRAM_Bandwidth_Utilization",
        ],
        "topics": EMBEDDED_TOPICS,
    },
    {
        "key": "security_crypto",
        "label": "Security / Crypto",
        "tag": '"#system/crypto"',
        "focus": "bütünlük, failure signature ve kriptografik sınırlar",
        "hint_seed": "memory safety crypto",
        "sources": [
            "https://support.apple.com/en-ca/guide/security/sec8b776536b/web",
            "https://datatracker.ietf.org/doc/html/rfc5116",
            "https://csrc.nist.gov/pubs/sp/800/38/d/final",
            "https://www.zkdocs.com/docs/zkdocs/",
        ],
        "anchors": [
            "Pointer_Authentication_Check",
            "Stack_Smash_Detection",
            "Heap_Overflow_Heuristics",
            "Cryptographic_Entropy_Analysis",
            "Instruction_Fetch_Analysis",
            "Causal_Inference_Engine",
            "Probabilistic_Graphical_Models",
            "Temporal_Pattern_Recognition",
        ],
        "topics": SECURITY_TOPICS,
    },
    {
        "key": "graph_rag",
        "label": "Graph RAG / Cognitive Retrieval",
        "tag": '"#rag/graph_rag"',
        "focus": "graph traversal, routing ve çok-kaynaklı reasoning",
        "hint_seed": "graph rag retrieval",
        "sources": [
            "https://arxiv.org/html/2607.28397v1",
            "https://arxiv.org/abs/2404.16130",
            "https://arxiv.org/abs/2205.13147",
        ],
        "anchors": [
            "Graph_Neural_Network_Embeddings",
            "Node2Vec_Mapping",
            "Topology_Analysis",
            "Temporal_Pattern_Recognition",
            "Cross_Correlation_Matrix",
            "Causal_Inference_Engine",
            "Probabilistic_Graphical_Models",
            "Sequence_Alignment",
        ],
        "topics": AI_TOPICS,
    },
]


def memory_cell_paths() -> list[Path]:
    return sorted(KNOWLEDGE_DIR.glob("RAG_Memory_Cell_*.md"))


def max_existing_index() -> int:
    maximum = 0
    for path in memory_cell_paths():
        parts = path.stem.split("_", 4)
        if len(parts) >= 4 and parts[3].isdigit():
            maximum = max(maximum, int(parts[3]))
    return maximum


def rotate_links(anchor_pool: list[str], offset: int, count: int = 4) -> list[str]:
    selected: list[str] = []
    for step in range(len(anchor_pool)):
        candidate = anchor_pool[(offset + step) % len(anchor_pool)]
        if candidate not in selected:
            selected.append(candidate)
        if len(selected) == count:
            return selected
    raise ValueError("Anchor pool is too small for requested link count")


def flatten_topic_specs() -> list[dict[str, Any]]:
    flattened: list[dict[str, Any]] = []
    for bundle in DOMAIN_BUNDLES:
        for local_index, topic in enumerate(bundle["topics"]):
            flattened.append(
                {
                    **topic,
                    "domain_key": bundle["key"],
                    "domain_label": bundle["label"],
                    "domain_tag": bundle["tag"],
                    "focus": bundle["focus"],
                    "hint_seed": bundle["hint_seed"],
                    "sources": bundle["sources"],
                    "anchors": rotate_links(bundle["anchors"], local_index, count=4),
                }
            )
    return flattened


def build_query_hints(title: str, hint_seed: str) -> list[str]:
    stem = title.lower()
    short = " ".join(stem.split()[:4])
    return [
        stem,
        f"{hint_seed} {short}",
        f"{short} lokumai",
        f"{short} retrieval boundary",
    ]


def render_note(index: int, spec: dict[str, Any]) -> str:
    hints = build_query_hints(spec["title"], spec["hint_seed"])
    sources = "\n".join(f"- {url}" for url in spec["sources"][:3])
    forward_links = "\n".join(f"[[{target}]]" for target in spec["anchors"])

    text = f"""---
date: 2026-08-30
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - {spec["domain_tag"]}
---

# {spec["title"]}

## Teknik çekirdek

{spec["summary"]} Bu hücre, {spec["domain_label"]} alanında {spec["focus"]} başlığını ayrı bir retrieval sinyali olarak saklar. Amaç, performans ya da güvenilirlik sorunlarını genel gürültü yerine mekanizma düzeyinde isimlendirmektir.

## Doğrulanmış bulgular

- {spec["summary"]}
- Pratik sınır: {spec["boundary"]}
- Retrieval sinyali: {spec["retrieval"]}
- Bu başlık, aynı etkiyi üreten fakat farklı kök nedene sahip semptomları ayırmak için ayrı tutulmalıdır.

## LokumAI için çıkarım

LokumAI tarafında bu not, {spec["domain_label"]} ailesindeki sorunları tek bir kaba etikete yığmadan sınıflandırmak için kullanılır. Böylece ajan, soru performans darboğazı mı, bütünlük riski mi, yoksa graph routing yanlılığı mı taşıyor sorusuna daha erken cevap verebilir.

## Sorgu ipuçları

- `{hints[0]}`
- `{hints[1]}`
- `{hints[2]}`
- `{hints[3]}`

## Kaynaklar

{sources}

{forward_links}
"""
    assert_no_forbidden_nodes(text)
    assert_link_target_layer_membership(parse_wikilinks(text), allowed_targets=allowed_forward_targets())
    return text


def plan_wave(count: int) -> list[dict[str, Any]]:
    specs = flatten_topic_specs()
    if count > len(specs):
        raise ValueError(f"Requested {count} notes but only {len(specs)} curated topics are available")

    start_index = max_existing_index() + 1
    planned: list[dict[str, Any]] = []
    for offset, spec in enumerate(specs[:count]):
        index = start_index + offset
        filename = build_note_filename("RAG_Memory_Cell", spec["title"], index=index)
        planned.append(
            {
                **spec,
                "index": index,
                "filename": filename,
                "path": KNOWLEDGE_DIR / filename,
            }
        )
    return planned


def print_dry_run(planned: list[dict[str, Any]]) -> None:
    distribution = Counter(item["domain_key"] for item in planned)
    synapse_count = sum(len(item["anchors"]) for item in planned)

    print(f"Planned file count: {len(planned)}")
    print(f"Projected synapse count: {synapse_count}")
    print("Topic bucket distribution:")
    for key, value in sorted(distribution.items()):
        print(f"  - {key}: {value}")
    if planned:
        print(f"Series start: {planned[0]['index']}")
        print(f"Series end: {planned[-1]['index']}")
        print(f"First file: {planned[0]['filename']}")
        print(f"Last file: {planned[-1]['filename']}")


def write_wave(planned: list[dict[str, Any]]) -> None:
    for item in planned:
        path: Path = item["path"]
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {path.name}")
        path.write_text(render_note(item["index"], item), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Phase 1 research-wave memory cells.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Plan files without writing them")
    mode.add_argument("--write", action="store_true", help="Write markdown files to Knowledge")
    parser.add_argument("--count", type=int, default=52, help="How many new memory cells to plan or write")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    planned = plan_wave(args.count)

    if args.dry_run:
        print_dry_run(planned)
        return 0

    write_wave(planned)
    print_dry_run(planned)
    print("Write completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
