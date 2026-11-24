"""Teste local: python dev_local.py  ->  http://127.0.0.1:8000/admin.html"""
import os, sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "api"))
if (RAIZ / ".env").exists():
    for linha in (RAIZ / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in linha and not linha.lstrip().startswith("#"):
            k, v = linha.split("=", 1); os.environ.setdefault(k.strip(), v.strip())
from _handler import handler as Api

class Dev(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(RAIZ / "public"), **k)
    def do_GET(self):
        if self.path.startswith("/api/"): return Api.do_GET(self)
        if self.path.startswith("/?") : self.path = "/index.html"
        return super().do_GET()
    def do_POST(self): return Api.do_POST(self)
    _json = Api._json; _executar = Api._executar

ThreadingHTTPServer(("127.0.0.1", int(os.getenv("PORT", "8000"))), Dev).serve_forever()
