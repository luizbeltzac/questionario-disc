"""Gera o PDF do resultado DISC do participante."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from reportlab.graphics.shapes import Circle, Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from _perfis import AVISO, ENCAIXE, PERFIS, resumo
from _questionario import TITULOS_C
from _questionario import FATORES, NOMES_FATORES

NAVY = colors.HexColor("#2D366F")
INK = colors.HexColor("#1D2340")
MUTED = colors.HexColor("#5F6782")
LINE = colors.HexColor("#D9DDE8")
MIST = colors.HexColor("#EEF0F6")
CLASSE_COR = {
    "otimo": colors.HexColor("#DFF0D8"),
    "bom": colors.HexColor("#FBF3D5"),
    "regular": colors.HexColor("#FCE3C4"),
    "apoio": colors.HexColor("#F8D3CF"),
}

W, H = A4
MARGEM = 18 * mm
LARG = W - 2 * MARGEM

ST = {
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=NAVY, spaceAfter=4),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13.5, leading=17, textColor=NAVY, spaceBefore=10, spaceAfter=6),
    "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=INK, spaceBefore=6, spaceAfter=3),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14, textColor=INK),
    "muted": ParagraphStyle("muted", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=MUTED),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=9, leading=12, textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=INK),
    "big": ParagraphStyle("big", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=NAVY),
    "kicker": ParagraphStyle("kicker", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=MUTED),
    "center": ParagraphStyle("center", fontName="Helvetica", fontSize=8.5, leading=11, textColor=MUTED, alignment=TA_CENTER),
}


def _cor(f: str):
    return colors.HexColor(PERFIS[f]["cor"])


def _grafico_barras(final: dict, principal: str) -> Drawing:
    w, h = LARG * 0.56, 62 * mm
    d = Drawing(w, h)
    base_y, top = 14 * mm, h - 8 * mm
    alt = top - base_y
    for g in (0, 25, 50, 75, 100):
        y = base_y + alt * g / 100
        d.add(Line(10 * mm, y, w, y, strokeColor=LINE, strokeWidth=0.5))
        d.add(String(8 * mm, y - 2.5, str(g), fontName="Helvetica", fontSize=7, fillColor=MUTED, textAnchor="end"))
    slot = (w - 12 * mm) / 4
    for i, f in enumerate(FATORES):
        x = 12 * mm + i * slot + slot * 0.2
        bw = slot * 0.6
        v = final[f]
        bh = alt * v / 100
        d.add(Rect(x, base_y, bw, bh, fillColor=_cor(f), strokeColor=None))
        d.add(String(x + bw / 2, base_y + bh + 3, f"{v:.0f}", fontName="Helvetica-Bold", fontSize=9, fillColor=INK, textAnchor="middle"))
        d.add(String(x + bw / 2, base_y - 10, f, fontName="Helvetica-Bold", fontSize=11,
                     fillColor=_cor(f) if f != principal else NAVY, textAnchor="middle"))
        d.add(String(x + bw / 2, base_y - 19, NOMES_FATORES[f], fontName="Helvetica", fontSize=7, fillColor=MUTED, textAnchor="middle"))
    return d


def _grafico_eixos(ritmo: float, foco: float) -> Drawing:
    s = 58 * mm
    d = Drawing(LARG * 0.42, s + 12 * mm)
    ox, oy = (LARG * 0.42 - s) / 2, 8 * mm
    cx, cy = ox + s / 2, oy + s / 2
    quad = [("D", ox, cy), ("I", cx, cy), ("C", ox, oy), ("S", cx, oy)]
    for f, x, y in quad:
        d.add(Rect(x, y, s / 2, s / 2, fillColor=colors.Color(*_cor(f).rgb(), alpha=0.12), strokeColor=colors.white, strokeWidth=1))
        d.add(String(x + s / 4, y + s / 4 - 5, f, fontName="Helvetica-Bold", fontSize=16,
                     fillColor=colors.Color(*_cor(f).rgb(), alpha=0.55), textAnchor="middle"))
    d.add(Line(ox, cy, ox + s, cy, strokeColor=MUTED, strokeWidth=0.6))
    d.add(Line(cx, oy, cx, oy + s, strokeColor=MUTED, strokeWidth=0.6))
    d.add(String(cx, oy + s + 3, "Ativo / rápido", fontName="Helvetica", fontSize=7, fillColor=MUTED, textAnchor="middle"))
    d.add(String(cx, oy - 8, "Reflexivo / cauteloso", fontName="Helvetica", fontSize=7, fillColor=MUTED, textAnchor="middle"))
    d.add(String(ox - 2, cy + 3, "Tarefa", fontName="Helvetica", fontSize=7, fillColor=MUTED, textAnchor="end"))
    d.add(String(ox + s + 2, cy + 3, "Pessoas", fontName="Helvetica", fontSize=7, fillColor=MUTED, textAnchor="start"))
    px = cx + max(-1, min(1, foco / 75)) * (s / 2 - 4)
    py = cy + max(-1, min(1, ritmo / 75)) * (s / 2 - 4)
    d.add(Circle(px, py, 4.5, fillColor=NAVY, strokeColor=colors.white, strokeWidth=1.2))
    return d


def _rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGEM, 10 * mm, "Perfil Comportamental DISC · uso interno para desenvolvimento")
    canvas.drawRightString(W - MARGEM, 10 * mm, f"Página {doc.page}")
    canvas.restoreState()


def _cabecalho(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 8 * mm, W, 8 * mm, stroke=0, fill=1)
    canvas.restoreState()
    _rodape(canvas, doc)


def _lista(itens):
    return Paragraph("<br/>".join(f"•&nbsp;&nbsp;{i}" for i in itens), ST["body"])


def gerar_pdf(destino: Path, nome: str, email: str, resultado: dict, quando: datetime | None = None) -> Path:
    quando = quando or datetime.now()
    p = resultado["principal"]
    sec = resultado["secundario"]
    P = PERFIS[p]
    story = []

    story.append(Paragraph("PERFIL COMPORTAMENTAL DISC", ST["kicker"]))
    story.append(Spacer(1, 2))
    story.append(Paragraph(nome, ST["h1"]))
    story.append(Paragraph(f"{email} · respondido em {quando:%d/%m/%Y às %H:%M}", ST["muted"]))
    story.append(Spacer(1, 10))

    destaque = Table(
        [[Paragraph("SEU PERFIL", ST["kicker"])], [Paragraph(resultado["rotulo"], ST["big"])],
         [Paragraph(resumo(resultado), ST["body"])]],
        colWidths=[LARG],
    )
    destaque.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MIST),
        ("LINEBEFORE", (0, 0), (0, -1), 4, _cor(p)),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, 0), 9), ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
    ]))
    story.append(destaque)
    if not resultado["consistente"] and not resultado["equilibrado"]:
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            "<b>Perfil a confirmar em conversa.</b> As duas partes do questionário apontaram "
            "estilos diferentes. Isso é comum quando a pessoa adapta bastante o comportamento "
            "ao contexto; vale conversar com seu líder sobre as situações do dia a dia.",
            ST["body"]))
    story.append(Spacer(1, 6))

    graficos = Table([[_grafico_barras(resultado["final"], p), _grafico_eixos(resultado["ritmo"], resultado["foco"])]],
                     colWidths=[LARG * 0.57, LARG * 0.43])
    graficos.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "BOTTOM"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    story.append(Paragraph("Intensidade de cada estilo (0 a 100)", ST["h2"]))
    story.append(graficos)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Como ler:</b> as barras mostram o quanto cada estilo aparece no seu jeito de trabalhar; "
        "o mais alto é o seu estilo principal. O quadrante mostra onde você está em dois eixos: "
        "ritmo (ativo ou reflexivo) e foco (tarefa ou pessoas).", ST["muted"]))
    fd = resultado.get("faceta_d")
    if fd:
        story.append(Spacer(1, 3))
        story.append(Paragraph(
            "<b>Dominância em duas leituras</b> (Parte 1): "
            + " · ".join(f"{k} {v:.0f}" for k, v in fd.items())
            + ". Posicionamento é falar de forma direta, assumir e defender uma posição; "
            "velocidade/desafio é agir rápido, correr risco calculado e buscar metas difíceis.", ST["muted"]))

    story.append(Paragraph("Os quatro estilos em uma frase", ST["h2"]))
    linhas = [[Paragraph(f"<b>{f} · {PERFIS[f]['nome']}</b>", ST["cell"]), Paragraph(PERFIS[f]["resumo"], ST["cell"])]
              for f in FATORES]
    t = Table(linhas, colWidths=[38 * mm, LARG - 38 * mm])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ] + [("TEXTCOLOR", (0, i), (0, i), _cor(f)) for i, f in enumerate(FATORES)]))
    story.append(t)

    # Página 2 – perfil principal
    story.append(PageBreak())
    titulo_p = "Estilo com maior pontuação" if resultado["equilibrado"] else "Seu estilo principal"
    story.append(Paragraph(f"{titulo_p}: {p} · {P['nome']}", ST["h1"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Características", ST["h3"]))
    story.append(Paragraph(P["caracteristicas"], ST["body"]))
    story.append(Paragraph("O que motiva", ST["h3"]))
    story.append(Paragraph(P["motiva"], ST["body"]))
    story.append(Paragraph("Competências naturais", ST["h3"]))
    story.append(Paragraph(" · ".join(P["competencias"]), ST["body"]))
    story.append(Paragraph("Forças naturais", ST["h3"]))
    story.append(_lista(P["forcas"]))
    story.append(Paragraph("Pontos de atenção", ST["h3"]))
    story.append(Paragraph(P["atencao"], ST["body"]))

    if sec:
        S = PERFIS[sec]
        box = Table([[Paragraph(f"ESTILO SECUNDÁRIO · {sec} · {S['nome'].upper()}", ST["kicker"])],
                     [Paragraph(S["resumo"], ST["body"])],
                     [Paragraph(f"<b>O que motiva:</b> {S['motiva']}  <b>Atenção:</b> {S['atencao']}", ST["cell"])]],
                    colWidths=[LARG])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), MIST),
            ("LINEBEFORE", (0, 0), (0, -1), 4, _cor(sec)),
            ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, 0), 8), ("BOTTOMPADDING", (0, -1), (-1, -1), 9),
        ]))
        story.append(Spacer(1, 12))
        story.append(KeepTogether(box))

    # Página 3 – trabalhando juntos
    story.append(PageBreak())
    story.append(Paragraph("Trabalhando juntos", ST["h1"]))
    story.append(Paragraph("Suas respostas na Parte 3 e o que o seu estilo costuma preferir. Use esta página para "
                           "combinar com seu líder o jeito de se comunicar, de dar feedback e de acompanhar o trabalho.", ST["muted"]))
    # Parte 3 do questionário – como trabalhar melhor com a pessoa
    pc = resultado.get("parte_c")
    if pc:
        linhas = []
        for qid, titulo in TITULOS_C.items():
            v = pc.get(qid)
            if v:
                txt = " · ".join(v) if isinstance(v, list) else v
                linhas.append([Paragraph(f"<b>{titulo}</b>", ST["cell"]), Paragraph(txt, ST["cell"])])
        tc = Table(linhas, colWidths=[38 * mm, LARG - 38 * mm])
        tc.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(KeepTogether([
            Paragraph("Como trabalhar melhor com você (suas respostas)", ST["h2"]),
            tc]))

    story.append(Paragraph("Como o seu estilo tende a preferir ser conduzido", ST["h2"]))
    cols = [p] + ([sec] if sec else [])
    head = [Paragraph("<b>Dimensão</b>", ST["cell"])] + [Paragraph(f"<b>{f} · {PERFIS[f]['nome']}</b>", ST["cell"]) for f in cols]
    rows = [head]
    for dim in PERFIS[p]["como_prefere"]:
        rows.append([Paragraph(f"<b>{dim}</b>", ST["cell"])] + [Paragraph(PERFIS[f]["como_prefere"][dim], ST["cell"]) for f in cols])
    cw = [38 * mm] + [(LARG - 38 * mm) / len(cols)] * len(cols)
    t = Table(rows, colWidths=cw)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), MIST),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)

    # Página 4 – atividades, sombras e desenvolvimento
    story.append(PageBreak())
    story.append(Paragraph("Encaixe com os tipos de atividade", ST["h2"]))
    story.append(Paragraph(
        "Quão natural cada tipo de atividade tende a ser para o seu estilo. Cores mais quentes não indicam "
        "incapacidade: mostram onde um modelo, recursos ou acompanhamento ajudam mais.", ST["muted"]))
    story.append(Spacer(1, 5))
    rows = [[Paragraph("<b>Tipo de atividade</b>", ST["cell"])] + [Paragraph(f"<b>{f} · {PERFIS[f]['nome']}</b>", ST["cell"]) for f in cols]]
    estilos = [("BACKGROUND", (0, 0), (-1, 0), MIST), ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.white),
               ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
    for r, (atividade, por_perfil) in enumerate(ENCAIXE, start=1):
        linha = [Paragraph(atividade, ST["cellb"])]
        for c, f in enumerate(cols, start=1):
            texto, classe = por_perfil[f]
            linha.append(Paragraph(texto, ST["cell"]))
            estilos.append(("BACKGROUND", (c, r), (c, r), CLASSE_COR[classe]))
        rows.append(linha)
    t = Table(rows, colWidths=cw)
    t.setStyle(TableStyle(estilos))
    story.append(t)
    story.append(Spacer(1, 3))
    leg = Table([[Paragraph(lbl, ST["muted"]) for lbl in ["Ótimo / Excelente", "Bom", "Regular", "Precisa de apoio"]]],
                colWidths=[LARG / 4] * 4)
    leg.setStyle(TableStyle([("BACKGROUND", (i, 0), (i, 0), CLASSE_COR[k]) for i, k in enumerate(["otimo", "bom", "regular", "apoio"])]
                            + [("LEFTPADDING", (0, 0), (-1, -1), 6)]))
    story.append(leg)

    story.append(Paragraph("Quando a força vira excesso", ST["h2"]))
    t = Table([[Paragraph("<b>Vulnerabilidades</b>", ST["cell"]), Paragraph("<b>O que tende a gerar estresse</b>", ST["cell"])],
               [_lista(P["vulnerabilidades"]), _lista(P["estresse"])]],
              colWidths=[LARG / 2] * 2)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), MIST), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story.append(t)
    story.append(Spacer(1, 3))
    story.append(Paragraph("Tendências, não rótulos: nem toda pessoa do estilo mostra tudo isto.", ST["muted"]))

    story.append(Paragraph("Competências que vale desenvolver", ST["h2"]))
    rows = [[Paragraph("<b>Competência</b>", ST["cell"]), Paragraph("<b>Ferramentas que ajudam</b>", ST["cell"])]]
    rows += [[Paragraph(c, ST["cellb"]), Paragraph(fz, ST["cell"])] for c, fz in P["desenvolver"]]
    t = Table(rows, colWidths=[70 * mm, LARG - 70 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), MIST), ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story.append(t)
    story.append(Spacer(1, 3))
    story.append(Paragraph("Escolha uma ou duas para conversar com seu líder; se você já mostra a competência, siga em frente.", ST["muted"]))

    story.append(Spacer(1, 14))
    av = Table([[Paragraph(f"<b>Importante.</b> {AVISO}", ST["muted"])]], colWidths=[LARG])
    av.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.6, LINE), ("LEFTPADDING", (0, 0), (-1, -1), 9),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    story.append(av)
    story.append(Spacer(1, 4))
    story.append(Paragraph("Base: modelo DISC de William M. Marston (1928) e material do Instituto da Liderança "
                           "(Planner do Líder · Análise de Comportamento EXTRA).", ST["center"]))

    destino.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(destino), pagesize=A4, leftMargin=MARGEM, rightMargin=MARGEM,
                            topMargin=16 * mm, bottomMargin=16 * mm,
                            title=f"Perfil DISC - {nome}", author="Questionário DISC")
    doc.build(story, onFirstPage=_cabecalho, onLaterPages=_cabecalho)
    return destino
