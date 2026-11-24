"""Função única da Vercel: recebe todas as rotas /api/* (ver vercel.json)."""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _servico import ErroUsuario, criar_convite, montar_questionario, processar  # noqa: E402


class handler(BaseHTTPRequestHandler):  # noqa: N801 (nome exigido pela Vercel)
    def _json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _executar(self, fn):
        try:
            self._json(fn())
        except ErroUsuario as e:
            self._json({"ok": False, "erro": str(e)}, 400)
        except Exception as e:  # noqa: BLE001
            print(f"ERRO {self.path}: {type(e).__name__}: {e}", flush=True)
            self._json({"ok": False, "erro": "Erro inesperado no servidor. Avise seu líder."}, 500)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path.rstrip("/").endswith("/questionario"):
            t = parse_qs(url.query).get("t", [""])[0]
            return self._executar(lambda: montar_questionario(t))
        self._json({"ok": False, "erro": "não encontrado"}, 404)

    def do_POST(self):
        url = urlparse(self.path)
        n = int(self.headers.get("Content-Length", "0") or 0)
        if n > 200_000:
            return self._json({"ok": False, "erro": "Requisição muito grande."}, 413)
        try:
            dados = json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            return self._json({"ok": False, "erro": "Requisição inválida."}, 400)
        rota = url.path.rstrip("/")
        if rota.endswith("/enviar"):
            return self._executar(lambda: processar(dados))
        if rota.endswith("/convite"):
            proto = self.headers.get("x-forwarded-proto", "https")
            base = f"{proto}://{self.headers.get('host', '')}"
            return self._executar(lambda: criar_convite(dados.get("senha", ""), dados.get("nome", ""),
                                                        dados.get("email", ""), dados.get("dias", 15), base))
        self._json({"ok": False, "erro": "não encontrado"}, 404)
