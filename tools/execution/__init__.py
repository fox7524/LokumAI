"""Execution-time surfaces for LokumAI.

Bu paket, H9 execution packaging katmanından türetilen paketleri runtime tarafında
okuyup deterministik bir plan (dry-run) üretmek için kullanılır.
"""

# NOT: Bu importlar `python -m tools.execution.live_executor` çalıştırmalarında
# `runpy` üzerinden "sys.modules already has ..." uyarısı üretebiliyor. O yüzden
# burada eager import yapmıyoruz; kullanıcılar modülleri doğrudan import etmeli.
