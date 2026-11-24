"""Itens do questionário DISC e regras de pontuação.

Parte A: 24 blocos de escolha forçada (mais / menos), uma frase por fator.
Parte B: 16 frases de concordância (1 a 5), quatro por fator, em ordem aleatória.
Parte C: "Como trabalhar melhor com você" – 5 perguntas de escolha única e
2 de múltipla escolha (até 3). Não entra na pontuação DISC; vai para o PDF e
para o líder. As opções das perguntas de estilo indicam um fator só como
conferência (campo "pistas_c" do resultado).

As frases foram escritas a partir das definições de Marston (1928) e do
material "Como conduzir cada pessoa em cada atividade" (Instituto da
Liderança). Para revisar o texto de uma frase, altere apenas a string; não
mude a letra do fator.
"""
from __future__ import annotations

import random

FATORES = ["D", "I", "S", "C"]
NOMES_FATORES = {
    "D": "Dominância",
    "I": "Influência",
    "S": "Estabilidade",
    "C": "Conformidade",
}

# Cada bloco: {fator: frase}
PARTE_A = [
    {"D": "Vou direto ao ponto para chegar ao resultado", "I": "Animo as pessoas ao meu redor", "S": "Mantenho um ritmo constante de trabalho", "C": "Confiro os detalhes antes de entregar"},
    {"D": "Assumo o comando quando a situação pede", "I": "Gosto de trocar ideias com várias pessoas", "S": "Prefiro saber com antecedência o que vai mudar", "C": "Sigo os procedimentos combinados"},
    {"D": "Gosto de metas desafiadoras", "I": "Gosto quando o time celebra junto as conquistas", "S": "Valorizo um ambiente de confiança e lealdade", "C": "Gosto de entender o porquê de cada decisão"},
    {"D": "Prefiro decidir logo e ajustar no caminho", "I": "Convenço as pessoas com entusiasmo", "S": "Escuto com atenção antes de opinar", "C": "Analiso os dados antes de decidir"},
    {"D": "Questiono quando algo não traz resultado", "I": "Puxo conversa com facilidade, até com quem não conheço", "S": "Sou a pessoa a quem os colegas recorrem para ajudar", "C": "Percebo erros que os outros deixam passar"},
    {"D": "Prefiro ter autonomia para fazer do meu jeito", "I": "Prefiro trabalhar com pessoas a trabalhar sozinho(a)", "S": "Prefiro uma rotina previsível", "C": "Prefiro receber instruções claras e completas"},
    {"D": "Busco vencer obstáculos com rapidez", "I": "Busco deixar o clima leve e positivo", "S": "Busco manter a harmonia na equipe", "C": "Busco fazer certo da primeira vez"},
    {"D": "Fico impaciente com processos lentos", "I": "Fico desconfortável quando trabalho isolado(a)", "S": "Fico desconfortável com mudanças bruscas", "C": "Fico desconfortável quando as regras mudam sem explicação"},
    {"D": "Encaro conflitos de frente", "I": "Uso o bom humor para aliviar tensões", "S": "Evito conflitos para preservar as relações", "C": "Uso fatos e argumentos lógicos numa discussão"},
    {"D": "Gosto de começar coisas novas", "I": "Gosto de apresentar ideias para um grupo", "S": "Gosto de concluir o que comecei antes de pegar outra coisa", "C": "Gosto de organizar e planejar cada etapa"},
    {"D": "Sou objetivo(a) e prático(a)", "I": "Sou comunicativo(a) e expressivo(a)", "S": "Sou paciente e calmo(a)", "C": "Sou cuidadoso(a) e preciso(a)"},
    {"D": "Me motiva ter resultados para mostrar", "I": "Me motiva trabalhar junto com outras pessoas", "S": "Me motiva saber que meu trabalho tem propósito", "C": "Me motiva resolver um problema técnico difícil"},
    {"D": "Em reuniões, quero ir logo para a decisão", "I": "Em reuniões, gosto de espaço para conversar", "S": "Em reuniões, prefiro ouvir mais do que falar", "C": "Em reuniões, gosto de pauta e objetividade"},
    {"D": "Aceito um risco calculado para ganhar tempo", "I": "Confio na minha intuição", "S": "Prefiro o caminho que já foi testado", "C": "Prefiro checar tudo antes de arriscar"},
    {"D": "Gosto de competir e vencer", "I": "Gosto de construir uma boa relação com todo mundo", "S": "Prefiro cooperar a competir", "C": "Gosto de manter um padrão de qualidade alto"},
    {"D": "Falo o que penso de forma direta", "I": "Falo com entusiasmo para engajar as pessoas", "S": "Falo com calma e cuidado com o outro", "C": "Falo com precisão e embasamento"},
    {"D": "Diante de um problema, tomo a frente", "I": "Diante de um problema, mobilizo as pessoas", "S": "Diante de um problema, apoio quem está resolvendo", "C": "Diante de um problema, investigo a causa"},
    {"D": "Prefiro que me cobrem o resultado, não o passo a passo", "I": "Prefiro um líder próximo e acessível", "S": "Prefiro um líder que combine os prazos comigo", "C": "Prefiro um líder que deixe claras as prioridades e o cronograma"},
    {"D": "Trabalho bem sob pressão de prazo", "I": "Trabalho bem fazendo várias coisas ao mesmo tempo", "S": "Trabalho bem com tarefas contínuas e estáveis", "C": "Trabalho bem com tarefas que exigem precisão"},
    {"D": "Sou persistente até atingir a meta", "I": "Sou otimista mesmo em situações difíceis", "S": "Sou leal às pessoas e aos combinados", "C": "Sou disciplinado(a) com prazos e regras"},
    {"D": "Assumo responsabilidades além do meu papel", "I": "Faço contatos e networking com facilidade", "S": "Sou bom(boa) ouvinte e alguém em quem se pode confiar", "C": "Sou criterioso(a) e observador(a)"},
    {"D": "Prefiro tarefas com desafio e liberdade", "I": "Prefiro tarefas com interação e variedade", "S": "Prefiro tarefas com método e continuidade", "C": "Prefiro tarefas com regras e padrões claros"},
    {"D": "Costumo falar sobre metas e conquistas", "I": "Costumo falar sobre pessoas e o ambiente de trabalho", "S": "Costumo falar sobre acordos e casos que já aconteceram", "C": "Costumo falar sobre fatos, dados e detalhes"},
    {"D": "Quando discordo, defendo minha posição com firmeza", "I": "Quando discordo, busco convencer conversando com as pessoas", "S": "Quando discordo, prefiro ceder para manter o bom clima", "C": "Quando discordo, peço dados que comprovem o ponto"},
]

# (fator, frase, invertida). Na frase invertida a nota conta ao contrário (5 -> 1).
PARTE_B = [
    ("D", "Gosto de assumir o controle das situações", False),
    ("I", "Prefiro resolver as coisas conversando a trocar mensagens", False),
    ("S", "Prefiro manter a rotina mesmo quando surge algo novo e interessante", False),
    ("C", "Reviso meu trabalho mais de uma vez, mesmo com prazo apertado", False),
    ("D", "Prefiro decidir rápido, mesmo que precise corrigir depois", False),
    ("I", "Rendo mais trabalhando perto das pessoas do que sozinho(a)", False),
    ("S", "Mudanças de última hora me incomodam bastante", False),
    ("C", "Sigo o procedimento mesmo quando um atalho resolveria", False),
    ("D", "Prefiro um desafio difícil a uma tarefa tranquila", False),
    ("I", "Costumo ser quem puxa o grupo para uma ideia nova", False),
    ("S", "Prefiro ceder num ponto a criar atrito com um colega", False),
    ("C", "Prefiro atrasar uma decisão a decidir sem os dados", False),
    ("D", "Num impasse, prefiro que outra pessoa conduza", True),
    ("I", "Prefiro trabalhar quieto(a), com pouca conversa", True),
    ("S", "A rotina me entedia rápido", True),
    ("C", "Entrego no \"bom o suficiente\" sem me incomodar", True),
]

# Duas leituras da Dominância na Parte A (índice do bloco -> faceta da frase D)
# P = Posicionamento (direto, assume, defende posição, autonomia)
# V = Velocidade/desafio (rapidez, risco, metas, competição)
FACETA_D = {0: "P", 1: "P", 2: "V", 3: "V", 4: "P", 5: "P", 6: "V", 7: "V", 8: "P", 9: "V", 10: "P", 11: "V",
            12: "V", 13: "V", 14: "V", 15: "P", 16: "P", 17: "P", 18: "V", 19: "V", 20: "P", 21: "V", 22: "V", 23: "P"}
NOMES_FACETA_D = {"P": "Posicionamento", "V": "Velocidade/desafio"}


ESCALA_B = {
    1: "Discordo totalmente",
    2: "Discordo",
    3: "Neutro",
    4: "Concordo",
    5: "Concordo totalmente",
}

# Parte C – escolha única: (id, pergunta, [(fator ou None, opção)])
PARTE_C_UNICA = [
    ("comunicacao", "Como você prefere se comunicar no trabalho?", [
        ("D", "Direto e objetivo, sem rodeios"),
        ("I", "Conversando e trocando ideias"),
        ("S", "Com calma, ouvindo antes de falar"),
        ("C", "Por escrito, com detalhes e precisão"),
    ]),
    ("feedback", "Como você prefere receber feedback?", [
        ("D", "Direto ao ponto, na hora"),
        ("I", "Numa conversa informal"),
        ("S", "Em particular, com calma e contexto"),
        ("C", "Por escrito, com exemplos concretos"),
    ]),
    ("decisao", "Diante de uma decisão difícil, você tende a:", [
        ("D", "Decidir rápido e ajustar no caminho"),
        ("I", "Ouvir opiniões e buscar consenso"),
        ("S", "Pensar no impacto nas pessoas antes"),
        ("C", "Levantar dados e analisar cenários"),
    ]),
    ("lideranca", "Se você liderasse um projeto, seu estilo natural seria:", [
        ("D", "Definir a direção e cobrar resultado"),
        ("I", "Inspirar e engajar as pessoas"),
        ("S", "Servir o time e remover obstáculos"),
        ("C", "Estruturar o plano e garantir o método"),
    ]),
    ("aprendizagem", "Como você prefere aprender algo novo?", [
        (None, "Vendo (diagramas, vídeos, exemplos)"),
        (None, "Ouvindo (explicações, conversas)"),
        (None, "Lendo e escrevendo (documentação, anotações)"),
        (None, "Fazendo (prática, tentativa e erro)"),
    ]),
]
TITULOS_C = {
    "comunicacao": "Comunicação", "feedback": "Feedback", "decisao": "Decisão",
    "lideranca": "Estilo de liderança", "aprendizagem": "Aprendizado (preferência)",
    "motivadores": "O que mais motiva", "valores": "Valores inegociáveis",
}

# Parte C – múltipla escolha (até MAX_MULTI): (id, pergunta, [opções])
MAX_MULTI = 3
PARTE_C_MULTI = [
    ("motivadores", "O que mais te motiva no trabalho? (até 3)", [
        "Desafios técnicos", "Reconhecimento", "Crescimento na carreira",
        "Estabilidade e segurança", "Autonomia", "Trabalho em equipe",
        "Impacto no cliente/negócio", "Aprender coisas novas", "Remuneração",
    ]),
    ("valores", "Quais valores são inegociáveis para você? (até 3)", [
        "Honestidade e transparência", "Excelência e qualidade", "Respeito às pessoas",
        "Colaboração", "Responsabilidade", "Inovação", "Justiça",
        "Equilíbrio vida-trabalho",
    ]),
]

MARGEM_SECUNDARIO = 10   # pontos (0-100) para considerar o 2º fator como secundário
MARGEM_EQUILIBRADO = 10  # se todos os fatores estiverem dentro desta faixa
MARGEM_CONSISTENCIA = 10  # v1.2: distância máxima entre as partes


def questionario_para_tela(seed: int | None = None) -> dict:
    """Monta o questionário embaralhando a ordem das frases em cada bloco.

    A tela recebe só textos e ids; a letra do fator não é enviada ao navegador.
    """
    rng = random.Random(seed)
    blocos = []
    for i, bloco in enumerate(PARTE_A):
        itens = [{"id": f"A{i}{f}", "texto": bloco[f]} for f in FATORES]
        rng.shuffle(itens)
        blocos.append({"numero": i + 1, "itens": itens})
    frases = [{"id": f"B{j}", "texto": t} for j, (_, t, _inv) in enumerate(PARTE_B)]
    rng.shuffle(frases)
    unica = []
    for qid, pergunta, opcoes in PARTE_C_UNICA:
        ops = [{"id": k, "texto": t} for k, (_, t) in enumerate(opcoes)]
        rng.shuffle(ops)
        unica.append({"id": qid, "pergunta": pergunta, "opcoes": ops})
    multi = [{"id": qid, "pergunta": pergunta, "max": MAX_MULTI,
              "opcoes": [{"id": k, "texto": t} for k, t in enumerate(opcoes)]}
             for qid, pergunta, opcoes in PARTE_C_MULTI]
    return {"parte_a": blocos, "parte_b": frases, "escala_b": ESCALA_B,
            "parte_c_unica": unica, "parte_c_multi": multi}


def ler_parte_c(resp: dict) -> dict:
    """Valida a Parte C e devolve {id: texto | [textos]} + pistas por fator."""
    resp = resp or {}
    saida, pistas = {}, {f: 0 for f in FATORES}
    for qid, pergunta, opcoes in PARTE_C_UNICA:
        try:
            k = int(resp.get(qid))
            fator, texto = opcoes[k]
        except (TypeError, ValueError, IndexError):
            raise ValueError(f"Parte 3: responda \"{pergunta}\"") from None
        saida[qid] = texto
        if fator:
            pistas[fator] += 1
    for qid, pergunta, opcoes in PARTE_C_MULTI:
        escolhas = resp.get(qid) or []
        try:
            idx = sorted({int(k) for k in escolhas})
            textos = [opcoes[k] for k in idx]
        except (TypeError, ValueError, IndexError):
            raise ValueError(f"Parte 3: resposta inválida em \"{pergunta}\"") from None
        if not 1 <= len(textos) <= MAX_MULTI:
            raise ValueError(f"Parte 3: escolha de 1 a {MAX_MULTI} opções em \"{pergunta}\"")
        saida[qid] = textos
    return {"respostas": saida, "pistas": pistas}


def _fator_do_id_a(item_id: str) -> str:
    # ids no formato A<índice><fator>, ex.: A12D
    return item_id[-1]


def pontuar(respostas: dict) -> dict:
    """Calcula o perfil.

    respostas = {
        "parte_a": [{"mais": "A0D", "menos": "A0S"}, ...24],
        "parte_b": {"B0": 4, "B1": 2, ...16},
    }
    """
    blocos = respostas.get("parte_a") or []
    if len(blocos) != len(PARTE_A):
        raise ValueError("A Parte A precisa ter as 24 respostas.")
    bruto_a = {f: 0 for f in FATORES}
    bruto_d = {"P": 0, "V": 0}
    for i, r in enumerate(blocos):
        mais, menos = r.get("mais"), r.get("menos")
        if not mais or not menos or mais == menos:
            raise ValueError(f"Bloco {i + 1}: escolha uma frase em MAIS e outra em MENOS.")
        for item_id in (mais, menos):
            if not item_id.startswith(f"A{i}") or _fator_do_id_a(item_id) not in FATORES:
                raise ValueError(f"Bloco {i + 1}: resposta inválida.")
        bruto_a[_fator_do_id_a(mais)] += 1
        bruto_a[_fator_do_id_a(menos)] -= 1
        if _fator_do_id_a(mais) == "D":
            bruto_d[FACETA_D[i]] += 1
        if _fator_do_id_a(menos) == "D":
            bruto_d[FACETA_D[i]] -= 1

    resp_b = respostas.get("parte_b") or {}
    if len(resp_b) != len(PARTE_B):
        raise ValueError("A Parte B precisa ter as 16 respostas.")
    soma_b = {f: 0 for f in FATORES}
    cont_b = {f: 0 for f in FATORES}
    for j, (fator, _, invertida) in enumerate(PARTE_B):
        valor = int(resp_b.get(f"B{j}", 0))
        if valor not in ESCALA_B:
            raise ValueError(f"Frase {j + 1} da Parte B sem resposta.")
        if invertida:
            valor = 6 - valor
        soma_b[fator] += valor
        cont_b[fator] += 1

    n = len(PARTE_A)
    pct_a = {f: round((bruto_a[f] + n) / (2 * n) * 100, 1) for f in FATORES}
    media_b = {f: soma_b[f] / cont_b[f] for f in FATORES}
    pct_b = {f: round((media_b[f] - 1) / 4 * 100, 1) for f in FATORES}
    final = {f: round((pct_a[f] + pct_b[f]) / 2, 1) for f in FATORES}

    ordem = sorted(FATORES, key=lambda f: final[f], reverse=True)
    principal = ordem[0]
    secundario = ordem[1] if final[ordem[0]] - final[ordem[1]] <= MARGEM_SECUNDARIO else None
    equilibrado = max(final.values()) - min(final.values()) <= MARGEM_EQUILIBRADO

    # Consistência (v1.2): fatores empatados contam juntos; só é inconsistente se o
    # principal de uma parte ficar mais de MARGEM_CONSISTENCIA pontos atrás do maior da outra.
    max_a, max_b = max(pct_a.values()), max(pct_b.values())
    tops_a = [f for f in FATORES if pct_a[f] == max_a]
    tops_b = [f for f in FATORES if pct_b[f] == max_b]
    consistente = (min(max_b - pct_b[f] for f in tops_a) <= MARGEM_CONSISTENCIA
                   and min(max_a - pct_a[f] for f in tops_b) <= MARGEM_CONSISTENCIA)
    n_fac = {k: sum(1 for v in FACETA_D.values() if v == k) for k in ("P", "V")}
    faceta_d = {NOMES_FACETA_D[k]: round((bruto_d[k] + n_fac[k]) / (2 * n_fac[k]) * 100, 1) for k in ("P", "V")}

    ritmo = round(((final["D"] + final["I"]) - (final["S"] + final["C"])) / 2, 1)
    foco = round(((final["I"] + final["S"]) - (final["D"] + final["C"])) / 2, 1)

    proximos = [f for f in ordem[2:] if final[principal] - final[f] <= MARGEM_SECUNDARIO] if secundario else []
    if equilibrado:
        rotulo = "Perfil equilibrado"
    elif secundario:
        rotulo = f"{principal}{secundario} – {NOMES_FATORES[principal]} com {NOMES_FATORES[secundario]}"
        if proximos:
            nomes = " e ".join(NOMES_FATORES[f] for f in proximos)
            rotulo += f" · {nomes} também {'próximas' if len(proximos) > 1 else 'próxima'}"
    else:
        rotulo = f"{principal} – {NOMES_FATORES[principal]}"

    return {
        "bruto_a": bruto_a,
        "pct_a": pct_a,
        "media_b": {f: round(media_b[f], 2) for f in FATORES},
        "pct_b": pct_b,
        "final": final,
        "ordem": ordem,
        "principal": principal,
        "secundario": secundario,
        "equilibrado": equilibrado,
        "consistente": consistente,
        "proximos": proximos,
        "faceta_d": faceta_d,
        "ritmo": ritmo,
        "foco": foco,
        "rotulo": rotulo,
    }
