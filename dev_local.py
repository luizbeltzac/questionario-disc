"""Teste local: python dev_local.py  ->  http://127.0.0.1:8000/admin.html"""
import os
from pathlib import Path
from wsgiref.simple_server import make_server

RAIZ = Path(__file__).resolve().parent
if (RAIZ / ".env").exists():
    for linha in (RAIZ / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in linha and not linha.lstrip().startswith("#"):
            k, v = linha.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

from app import app  # noqa: E402

porta = int(os.getenv("PORT", "8000"))
print(f"http://127.0.0.1:{porta}/admin.html")
make_server("127.0.0.1", porta, app).serve_forever()
