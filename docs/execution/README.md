# Runtime Executor (Dry-Run)

Bu katman, `Lokum1.0/Knowledge` içindeki **H9 execution packaging** notlarını okuyup
“gerçekte ne teslim edilecekti?” sorusuna deterministik bir **plan (dry-run)** üretir.

Bu tasarımın amacı:

- H9 paketlerini runtime tarafında “okunabilir sözleşme” haline getirmek
- Henüz *gerçek aksiyon çalıştırmadan* (shell, network, donanım) önce kontrol edilebilir bir çıktı vermek

## Çalıştırma

Repo kökünde:

```bash
python3 -m tools.execution.runtime_executor --out docs/brain_growth/reports/execution_plan.json
```

Eğer farklı bir vault dizini test ediyorsan:

```bash
python3 -m tools.execution.runtime_executor --knowledge-dir /path/to/Knowledge --out execution_plan.json
```

## Çıktı şeması (özet)

Üretilen JSON şu alanları içerir:

- `packages[]`
  - `package_id` (örn. `H9_Commit_Ready_Delivery_Check`)
  - `package_mode`, `source_policy`
  - `delivery_surfaces[]` (teslim yüzeyleri)
  - `package_contracts[]` (sözleşmeler)
  - `outputs[]` (not içindeki `## Paketlenen çıktı yolları` wikilink listesi)
- `surface_index` : `surface -> [package_id...]` indeksi

## Tasarım notu

Bu executor şu an **sadece plan üretir**. “Gerçek aksiyon çalıştırma” (script/shell/ESP32 vs.) adımı,
bir sonraki katmanda (Wave 11+ veya ayrı bir runtime modülü) güvenli bir *capability* modeliyle eklenmeli.

