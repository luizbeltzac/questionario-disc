"""Regras da versão online: convites assinados, questionário, envio do resultado.

Nada é gravado na plataforma. O resultado vai por e-mail:
- participante: PDF;
- líder (LEADER_EMAIL): PDF + .json (para importar no programa Gestão do Time).
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import html
import json
import os
import re
import secrets
import tempfile
import time
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path

from _email_envio import env_bool, send_email
from _pdf_relatorio import gerar_pdf
from _perfis import AVISO, PERFIS, resumo
from _questionario import FATORES, NOMES_FATORES, PARTE_A, PARTE_B, ler_parte_c, pontuar, questionario_para_tela

VERSAO = "1.1-online"
FUSO = timezone(timedelta(hours=-3))  # Brasília
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@([A-Za-z0-9.\-]+\.[A-Za-z]{2,})$")


class ErroUsuario(Exception):
    """Erro com mensagem para mostrar na tela."""


def _cfg(nome: str, padrao: str = "") -> str:
    return os.getenv(nome, padrao).strip()


def _segredo() -> bytes:
    s = _cfg("APP_SECRET")
    if len(s) < 16:
        raise RuntimeError("Configure APP_SECRET (mínimo 16 caracteres) nas variáveis de ambiente.")
    return s.encode()


def _dominio() -> str:
    return _cfg("ALLOWED_EMAIL_DOMAIN", "senff.com.br").lower().lstrip("@")


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")


def _unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def _assinar(texto: str, n: int = 32) -> str:
    return hmac.new(_segredo(), texto.encode(), hashlib.sha256).hexdigest()[:n]


# ------------------------------------------------------------------ convites
def criar_convite(senha: str, nome: str, email: str, dias: int, base_url: str) -> dict:
    admin = _cfg("ADMIN_PASSWORD")
    if not admin:
        raise RuntimeError("Configure ADMIN_PASSWORD nas variáveis de ambiente.")
    if not hmac.compare_digest(senha.encode(), admin.encode()):
        time.sleep(1)
        raise ErroUsuario("Senha incorreta.")
    nome = " ".join(nome.split())
    email = email.strip().lower()
    if len(nome.split()) < 2:
        raise ErroUsuario("Informe o nome completo do participante.")
    m = EMAIL_RE.match(email)
    if not m or (_dominio() and m.group(1) != _dominio()):
        raise ErroUsuario(f"Informe um e-mail corporativo válido (@{_dominio()}).")
    dias = max(1, min(int(dias or 15), 90))
    expira = int(time.time()) + dias * 86400
    carga = _b64(json.dumps({"n": nome, "e": email, "x": expira}, ensure_ascii=False).encode())
    token = f"{carga}.{_assinar(carga)}"
    return {"ok": True, "link": f"{base_url}/?t={token}",
            "expira": datetime.fromtimestamp(expira, FUSO).strftime("%d/%m/%Y")}


def ler_convite(token: str) -> dict:
    try:
        carga, assinatura = token.split(".")
    except (ValueError, AttributeError):
        raise ErroUsuario("Link inválido. Peça um novo link ao seu líder.") from None
    if not hmac.compare_digest(assinatura, _assinar(carga)):
        raise ErroUsuario("Link inválido. Peça um novo link ao seu líder.")
    dados = json.loads(_unb64(carga))
    if dados["x"] < time.time():
        raise ErroUsuario("Este link expirou. Peça um novo link ao seu líder.")
    return {"nome": dados["n"], "email": dados["e"]}


# ------------------------------------------------------------------ questionário
def _id_item(seed: int, i: int, f: str) -> str:
    return _assinar(f"{seed}|{i}|{f}", 12)


def montar_questionario(token: str) -> dict:
    pessoa = ler_convite(token)
    seed = secrets.randbits(32)
    q = questionario_para_tela(seed=seed)
    for i, bloco in enumerate(q["parte_a"]):
        for item in bloco["itens"]:
            item["id"] = _id_item(seed, i, item["id"][-1])  # a letra do fator não vai para o navegador
    return {**q, **pessoa, "seed": seed}


def _slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_") or "participante"


def _corpo_participante(nome: str, res: dict) -> tuple[str, str]:
    p = PERFIS[res["principal"]]
    primeiro = html.escape(nome.split()[0])
    barras = "".join(
        f"<tr><td style='padding:3px 10px 3px 0;font-weight:bold;color:{PERFIS[f]['cor']}'>{f} · {NOMES_FATORES[f]}</td>"
        f"<td><div style='background:#EEF0F6;width:220px;height:12px;border-radius:6px'>"
        f"<div style='background:{PERFIS[f]['cor']};width:{res['final'][f] * 2.2:.0f}px;height:12px;border-radius:6px'></div></div></td>"
        f"<td style='padding-left:10px'>{res['final'][f]:.0f}</td></tr>" for f in FATORES)
    corpo = f"""<div style="font-family:Segoe UI,Arial,sans-serif;color:#1D2340;max-width:600px">
<p>Olá, {primeiro}!</p>
<p>Obrigado por responder o questionário de perfil comportamental. Seu resultado completo está no PDF anexo.</p>
<div style="background:#EEF0F6;border-left:4px solid {p['cor']};padding:12px 16px;margin:16px 0">
<div style="font-size:11px;color:#5F6782;font-weight:bold">SEU PERFIL</div>
<div style="font-size:20px;font-weight:bold;color:#2D366F">{html.escape(res['rotulo'])}</div>
<div style="margin-top:6px">{html.escape(resumo(res))}</div></div>
<table style="border-collapse:collapse;font-size:13px">{barras}</table>
<p style="margin-top:18px">Use o PDF como ponto de partida para a próxima conversa com seu líder.</p>
<p style="font-size:11px;color:#5F6782">{html.escape(AVISO)}</p></div>"""
    texto = (f"Olá, {nome.split()[0]}!\n\nSeu perfil: {res['rotulo']}\n{resumo(res)}\n\n"
             + "\n".join(f"{f} · {NOMES_FATORES[f]}: {res['final'][f]:.0f}" for f in FATORES)
             + "\n\nO resultado completo está no PDF anexo.\n\n" + AVISO)
    return corpo, texto


def processar(dados: dict) -> dict:
    pessoa = ler_convite(dados.get("t", ""))
    nome, email = pessoa["nome"], pessoa["email"]
    try:
        seed = int(dados.get("seed"))
    except (TypeError, ValueError):
        raise ErroUsuario("Sessão inválida. Recarregue a página e responda novamente.") from None

    respostas_a = dados.get("parte_a") or []
    if len(respostas_a) != len(PARTE_A):
        raise ErroUsuario("Responda todos os blocos da Parte 1.")
    parte_a = []
    for i, r in enumerate(respostas_a):
        mapa = {_id_item(seed, i, f): f"A{i}{f}" for f in FATORES}
        mais, menos = mapa.get(r.get("mais")), mapa.get(r.get("menos"))
        if not mais or not menos or mais == menos:
            raise ErroUsuario(f"Bloco {i + 1}: resposta inválida. Recarregue a página e responda novamente.")
        parte_a.append({"mais": mais, "menos": menos})
    parte_b = dados.get("parte_b") or {}
    for j in range(len(PARTE_B)):
        if str(parte_b.get(f"B{j}")) not in {"1", "2", "3", "4", "5"}:
            raise ErroUsuario("Responda todas as frases da Parte 2.")
    res = pontuar({"parte_a": parte_a, "parte_b": parte_b})
    pc = ler_parte_c(dados.get("parte_c"))
    res["parte_c"], res["pistas_c"] = pc["respostas"], pc["pistas"]

    agora = datetime.now(FUSO).replace(tzinfo=None)
    base = f"Perfil_DISC_{_slug(nome)}_{agora:%Y-%m-%d_%H%M}"
    pasta = Path(tempfile.mkdtemp())
    pdf = gerar_pdf(pasta / f"{base}.pdf", nome, email, res, agora)
    registro = {
        "nome": nome, "email": email, "data": agora.isoformat(timespec="seconds"),
        "versao_questionario": VERSAO, "resultado": res,
        "respostas": {
            "parte_a": [{"bloco": i + 1, "mais": r["mais"][-1], "menos": r["menos"][-1],
                         "texto_mais": PARTE_A[i][r["mais"][-1]], "texto_menos": PARTE_A[i][r["menos"][-1]]}
                        for i, r in enumerate(parte_a)],
            "parte_b": [{"fator": f, "frase": t, "nota": int(parte_b.get(f"B{j}"))} for j, (f, t) in enumerate(PARTE_B)],
        },
    }
    arq_json = pasta / f"{base}.json"
    arq_json.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")

    enviado, erro_envio = False, None
    if env_bool("DRY_RUN", False):
        erro_envio = "Modo de teste (DRY_RUN=1): e-mail não enviado"
    else:
        try:
            corpo, texto = _corpo_participante(nome, res)
            send_email(corpo, texto, email, f"Seu Perfil Comportamental DISC – {nome}", pdf, cc_override="")
            enviado = True
        except Exception as exc:  # noqa: BLE001
            erro_envio = f"{type(exc).__name__}: {exc}"
            print(f"ERRO envio participante: {erro_envio}", flush=True)
        # Sem LEADER_EMAIL, a cópia vai para a própria conta remetente (a do líder).
        lider = _cfg("LEADER_EMAIL") or _cfg("REPORT_CC") or _cfg("SMTP_FROM") or _cfg("SMTP_USER")
        print(f"Envio líder: destino {'configurado' if _cfg('LEADER_EMAIL') else 'padrão (SMTP_FROM)'}", flush=True)
        if lider:
            try:
                aviso = "" if enviado else f"<p><b>Atenção:</b> o e-mail para o participante falhou ({html.escape(erro_envio or '')}). Encaminhe o PDF.</p>"
                send_email(
                    f"<p>{html.escape(nome)} ({html.escape(email)}) concluiu o questionário DISC.</p>"
                    f"<p><b>{html.escape(res['rotulo'])}</b>{'' if res['consistente'] else ' – perfil a confirmar em conversa'}</p>{aviso}"
                    "<p>Anexos: PDF do resultado e o .json para importar no programa Gestão do Time.</p>",
                    f"{nome} concluiu o questionário DISC: {res['rotulo']}.", lider,
                    f"Resultado DISC – {nome}", [pdf, arq_json], cc_override="")
                print("Envio líder: OK", flush=True)
            except Exception as exc:  # noqa: BLE001
                print(f"ERRO envio líder: {type(exc).__name__}: {exc}", flush=True)

    return {
        "ok": True, "nome": nome, "email": email, "rotulo": res["rotulo"],
        "principal": res["principal"], "consistente": res["consistente"], "equilibrado": res["equilibrado"],
        "final": res["final"], "resumo": resumo(res),
        "cores": {f: PERFIS[f]["cor"] for f in FATORES}, "nomes": NOMES_FATORES,
        "enviado": enviado, "erro_envio": erro_envio,
        "pdf_nome": pdf.name, "pdf_b64": base64.b64encode(pdf.read_bytes()).decode(),
    }
