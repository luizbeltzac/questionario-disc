"""Rota /api/enviar – a lógica está em _handler.py / _servico.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _handler import handler  # noqa: E402,F401
