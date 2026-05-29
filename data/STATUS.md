## İndirme özeti

Bu klasöre **52 doküman** indirildi:

- **Project Gutenberg (Public Domain)**: `pg-*` (8 adet)
- **Wikibooks (CC BY-SA 4.0)**: `wb-*` (44 adet)  
  (TR: `tr.wikibooks.org` alt sayfaları + EN: `en.wikibooks.org` alt sayfaları)

### Boyut
- `data/raw/` toplam: ~4.85 MB
- `data/txt/` toplam: ~4.81 MB

### Lisans / yasal notlar
- `sources.json` her dosya için: kaynak URL + lisans + dosya hash’leri içerir.
- Gutenberg metinleri genelde Public Domain olsa da, Gutenberg’in kendi **license/terms** sayfasını referans aldım.
- Wikibooks içerikleri **CC BY-SA 4.0**: atıf ve share-alike şartları var. Fine-tune dağıtımı yapacaksan buna göre “attribution”/metaveri akışını planlamak gerekebilir.

### Bir sonraki mantıklı adım
Eğer bunu gerçekten **pair-programmer** hedefiyle fine-tune edeceksen:
- edebiyat metinleri (Gutenberg) “yazınsal üslup” aşılar,
- Wikibooks ise daha “öğretici/teknik” tona yakındır.

İstersen bir sonraki adımda, sadece teknik olanları ayrı bir subset’e ayıracak şekilde `data/txt/` içinde bir `train/` ve `rag/` ayrımı da yapabilirim.

