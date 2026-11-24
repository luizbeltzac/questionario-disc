"""Envio do resultado por e-mail via SMTP.

Mesma lógica do envio do relatório do Portfólio (relatorio_portfolio_email.py):
configuração no .env, SMTP_SECURITY ssl/starttls/none, autenticação opcional,
novas tentativas com conexão nova e espera crescente.
"""
from __future__ import annotations

import mimetypes
import os
import re
import smtplib
import ssl
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


def env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "sim", "s"}


def parse_recipients(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"[;,]", value or "") if part.strip()]


def send_email(
    html_body: str,
    text_body: str,
    recipient: str,
    subject: str,
    attachment_path=None,
    cc_override: str | None = None,
) -> None:
    smtp_host = os.getenv("SMTP_HOST", "smtppro.zoho.com").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_security = os.getenv("SMTP_SECURITY", "").strip().lower()

    # SMTP_SECURITY=ssl -> TLS implícito (porta 465 / SMTP_SSL)
    # SMTP_SECURITY=starttls -> STARTTLS (normalmente porta 587)
    # SMTP_SECURITY=none -> sem criptografia
    if not smtp_security:
        smtp_security = "starttls" if env_bool("SMTP_USE_TLS", True) else "none"
    if smtp_security in {"ssl/tls", "tls", "implicit_tls", "implicit-tls"}:
        smtp_security = "ssl"
    if smtp_security not in {"ssl", "starttls", "none"}:
        raise ValueError("SMTP_SECURITY inválido. Use 'ssl', 'starttls' ou 'none'.")

    smtp_user = os.getenv("SMTP_USER", "").strip()
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    sender = os.getenv("SMTP_FROM", smtp_user).strip()
    cc = parse_recipients(cc_override if cc_override is not None else os.getenv("REPORT_CC", ""))
    to = parse_recipients(recipient)
    recipients = to + [c for c in cc if c.lower() not in {t.lower() for t in to}]

    if not sender:
        raise ValueError("Configure SMTP_FROM ou SMTP_USER no arquivo .env.")
    if not recipients:
        raise ValueError("Nenhum destinatário foi informado.")

    message = MIMEMultipart("mixed")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(to)
    if cc:
        message["Cc"] = ", ".join(cc)

    alternative = MIMEMultipart("alternative")
    message.attach(alternative)
    alternative.attach(MIMEText(text_body, "plain", "utf-8"))
    alternative.attach(MIMEText(html_body, "html", "utf-8"))

    anexos = attachment_path if isinstance(attachment_path, (list, tuple)) else ([attachment_path] if attachment_path else [])
    for anexo in anexos:
        anexo = Path(anexo)
        if not anexo.is_file():
            raise FileNotFoundError(f"Anexo não encontrado: {anexo}")
        mime_type, _ = mimetypes.guess_type(str(anexo))
        main_type, sub_type = (mime_type.split("/", 1) if mime_type and "/" in mime_type
                               else ("application", "octet-stream"))
        part = MIMEBase(main_type, sub_type)
        part.set_payload(anexo.read_bytes())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=anexo.name)
        message.attach(part)

    message_bytes = message.as_bytes()
    smtp_timeout = int(os.getenv("SMTP_TIMEOUT", "20"))
    smtp_max_retries = max(1, int(os.getenv("SMTP_MAX_RETRIES", "2")))
    smtp_retry_delay = max(1, int(os.getenv("SMTP_RETRY_DELAY_SECONDS", "3")))
    context = ssl.create_default_context()

    last_error: Exception | None = None
    for attempt in range(1, smtp_max_retries + 1):
        try:
            print(f"Envio SMTP: tentativa {attempt}/{smtp_max_retries} para {smtp_host}:{smtp_port} ({smtp_security})...", flush=True)
            if smtp_security == "ssl":
                server_context = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=smtp_timeout, context=context)
            else:
                server_context = smtplib.SMTP(smtp_host, smtp_port, timeout=smtp_timeout)
            with server_context as server:
                server.ehlo()
                if smtp_security == "starttls":
                    server.starttls(context=context)
                    server.ehlo()
                if smtp_user:
                    if not smtp_password:
                        raise ValueError("SMTP_USER foi informado, mas SMTP_PASSWORD está vazio.")
                    server.login(smtp_user, smtp_password)
                server.sendmail(sender, recipients, message_bytes)
            print("Envio SMTP concluído.", flush=True)
            return
        except (
            smtplib.SMTPServerDisconnected,
            smtplib.SMTPConnectError,
            smtplib.SMTPAuthenticationError,
            smtplib.SMTPRecipientsRefused,
            smtplib.SMTPSenderRefused,
            smtplib.SMTPDataError,
            ConnectionResetError,
            ConnectionAbortedError,
            TimeoutError,
            OSError,
        ) as exc:
            last_error = exc
            print(f"Falha no SMTP na tentativa {attempt}/{smtp_max_retries}: {type(exc).__name__}: {exc}", flush=True)
            if attempt < smtp_max_retries:
                time.sleep(smtp_retry_delay * attempt)

    raise RuntimeError(
        f"Falha no envio após {smtp_max_retries} tentativa(s). Último erro: "
        f"{type(last_error).__name__}: {last_error}"
    ) from last_error
