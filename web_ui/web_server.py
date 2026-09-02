import http.server
import socketserver
import subprocess
import os

PORT = 8000
DIRECTORY = "/Users/fox/Documents/PROJECTS/LokumAI/web_ui"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Eğer graph_data.json istenirse, önce güncelleyip (dinamik oluşturup) sonra servis edelim
        if self.path == "/graph_data.json":
            print("[*] İstek geldi: graph_data.json dinamik olarak güncelleniyor...")
            subprocess.run(["/Users/fox/Documents/PROJECTS/LokumAI/.venv/bin/python", "generate_graph_data.py"], cwd=DIRECTORY)
        return super().do_GET()

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"[*] LokumAI Graphify Sunucusu Başladı: http://localhost:{PORT}")
    print("[*] Klasör:", DIRECTORY)
    httpd.serve_forever()
