"""Aplicação WSGI do questionário DISC (ponto de entrada da Vercel: variável `app`).

Rotas:
  GET  /api/questionario?t=<convite>   monta o questionário
  POST /api/enviar                     calcula, gera o PDF e envia os e-mails
  POST /api/convite                    gera link de convite (senha de administrador)
  GET  /, /admin.html                  páginas (servidas da pasta public/)
"""
import json
import os
import sys
from pathlib import Path
from urllib.parse import parse_qs

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "disc"))

from _servico import ErroUsuario, criar_convite, montar_questionario, processar  # noqa: E402

PAGINAS = {"/": "index.html", "/index.html": "index.html", "/admin": "admin.html", "/admin.html": "admin.html"}
CABECALHOS = [("Cache-Control", "no-store"), ("X-Robots-Tag", "noindex"), ("Referrer-Policy", "no-referrer")]


def _resposta(start_response, status, corpo: bytes, tipo: str):
    start_response(status, [("Content-Type", tipo), ("Content-Length", str(len(corpo)))] + CABECALHOS)
    return [corpo]


def _json(start_response, obj, status="200 OK"):
    return _resposta(start_response, status, json.dumps(obj, ensure_ascii=False).encode("utf-8"),
                     "application/json; charset=utf-8")


def _executar(start_response, fn):
    try:
        return _json(start_response, fn())
    except ErroUsuario as e:
        return _json(start_response, {"ok": False, "erro": str(e)}, "400 Bad Request")
    except Exception as e:  # noqa: BLE001
        print(f"ERRO: {type(e).__name__}: {e}", flush=True)
        return _json(start_response, {"ok": False, "erro": "Erro inesperado no servidor. Avise seu líder."},
                     "500 Internal Server Error")


def app(environ, start_response):
    caminho = environ.get("PATH_INFO", "/") or "/"
    metodo = environ.get("REQUEST_METHOD", "GET")
    rota = caminho.rstrip("/") or "/"

    if metodo == "GET" and rota in PAGINAS:
        return _resposta(start_response, "200 OK", (RAIZ / "public" / PAGINAS[rota]).read_bytes(),
                         "text/html; charset=utf-8")

    if metodo == "GET" and rota == "/api/questionario":
        t = parse_qs(environ.get("QUERY_STRING", "")).get("t", [""])[0]
        return _executar(start_response, lambda: montar_questionario(t))

    if metodo == "POST" and rota in ("/api/enviar", "/api/convite"):
        try:
            n = int(environ.get("CONTENT_LENGTH") or 0)
        except ValueError:
            n = 0
        if n > 200_000:
            return _json(start_response, {"ok": False, "erro": "Requisição muito grande."}, "413 Payload Too Large")
        try:
            dados = json.loads(environ["wsgi.input"].read(n) or b"{}")
        except json.JSONDecodeError:
            return _json(start_response, {"ok": False, "erro": "Requisição inválida."}, "400 Bad Request")
        if rota == "/api/enviar":
            return _executar(start_response, lambda: processar(dados))
        proto = environ.get("HTTP_X_FORWARDED_PROTO") or environ.get("wsgi.url_scheme", "https")
        base = f"{proto}://{environ.get('HTTP_X_FORWARDED_HOST') or environ.get('HTTP_HOST', '')}"
        return _executar(start_response, lambda: criar_convite(
            dados.get("senha", ""), dados.get("nome", ""), dados.get("email", ""), dados.get("dias", 15), base))

    return _json(start_response, {"ok": False, "erro": "não encontrado"}, "404 Not Found")
