"""Conteúdo de interpretação de cada perfil DISC.

Fonte: material "Como conduzir cada pessoa em cada atividade" (Instituto da
Liderança – Planner do Líder), págs. 2, 3, 5, 8 e 9, com base na Análise de
Comportamento EXTRA. Texto adaptado para leitura do próprio participante.
"""

PERFIS = {
    "D": {
        "nome": "Dominância",
        "cor": "#D9453B",
        "emocao": "Raiva",
        "resumo": "Foco em resultado, decisão e desafio. Age rápido e gosta de ter autonomia para fazer acontecer.",
        "caracteristicas": "Decidido(a), prático(a), questionador(a).",
        "motiva": "Desafio, reconhecimento e resultados.",
        "competencias": ["Empreendedorismo", "Criatividade e inovação", "Orientação para resultados", "Visão estratégica"],
        "forcas": [
            "Encontra soluções novas, criativas e lógicas.",
            "É ousado(a) para entrar em áreas totalmente novas.",
            "Transforma a estratégia em plano de ação detalhado.",
        ],
        "atencao": "Pode soar duro(a) e exigir solução rápida; busca se destacar; tem pouca paciência com rotina e conversa longa.",
        "como_prefere": {
            "Apoio emocional": "Precisa de pouco; prefere desafio.",
            "Prazo": "Gosta que a meta seja definida e que o caminho fique com você.",
            "Orientações": "Aceita com moderação; prefere entender o objetivo.",
            "Acompanhamento": "Rejeita microgerenciamento.",
            "Reuniões": "Curtas e objetivas; reuniões longas parecem perda de tempo.",
        },
        "vulnerabilidades": [
            "Dificuldade de ouvir e de respeitar o ritmo dos outros.",
            "Pode atropelar pessoas para chegar ao resultado.",
            "Tende a assumir tudo e a se sobrecarregar.",
        ],
        "estresse": [
            "Perder o controle ou a autonomia.",
            "Lentidão, burocracia e reunião longa.",
            "Ser contrariado(a) ou ver falta de resultado.",
            "Ser microgerenciado(a).",
        ],
        "desenvolver": [
            ("Escuta e empatia", "Conhecer o liderado, Reconhecimento da evolução"),
            ("Trabalho em equipe e delegação", "Comece-Pare-Continue, Atividades"),
            ("Planejamento e organização", "Meta SMART, Matriz de prioridades"),
            ("Feedback construtivo", "Feedback Sanduíche, Feedforward"),
        ],
    },
    "I": {
        "nome": "Influência",
        "cor": "#F39A1E",
        "emocao": "Alegria",
        "resumo": "Foco em pessoas, comunicação e entusiasmo. Conecta, anima e influencia por meio de relacionamentos.",
        "caracteristicas": "Positivo(a), comunicativo(a); valoriza conexão e palavras de afirmação.",
        "motiva": "Ajudar, interagir com o grupo e participar de treinamentos.",
        "competencias": ["Comunicação", "Relacionamento interpessoal", "Influência e persuasão", "Liderança"],
        "forcas": [
            "Mantém contato ativo com pessoas por vários canais.",
            "Influencia por meio de relacionamentos positivos.",
            "Ajuda a desenvolver as competências das pessoas.",
        ],
        "atencao": "Pode se guiar demais pela intuição e pela emoção; lida com muitas coisas ao mesmo tempo e pode perder o foco.",
        "como_prefere": {
            "Apoio emocional": "Precisa sempre; gosta de contato e se inspira no líder.",
            "Prazo": "Funciona melhor com acompanhamento próximo dos prazos.",
            "Orientações": "Resiste a ordens diretas; prefere ser envolvido(a).",
            "Acompanhamento": "Precisa de acompanhamento próximo.",
            "Reuniões": "Valoriza espaço para conversar.",
        },
        "vulnerabilidades": [
            "Necessidade de aprovação e de reconhecimento.",
            "Dispersão e promessas além do que consegue entregar.",
            "Evita assuntos difíceis para manter o clima bom.",
        ],
        "estresse": [
            "Isolamento ou falta de interação.",
            "Crítica ou rejeição, principalmente em público.",
            "Rotina solitária e excesso de detalhe.",
            "Falta de reconhecimento.",
        ],
        "desenvolver": [
            ("Foco e priorização", "Matriz de prioridades, Diário de Gestão"),
            ("Planejamento e organização", "Meta SMART, Atividades"),
            ("Constância e controle de atividades", "Plano de ação, Execução e acompanhamento da meta"),
            ("Análise com dados", "Dashboards, Painel consolidado"),
        ],
    },
    "S": {
        "nome": "Estabilidade",
        "cor": "#5B8C2A",
        "emocao": "Medo",
        "resumo": "Foco em constância, cooperação e confiança. Sustenta a operação e é apoio para a equipe.",
        "caracteristicas": "Cuidadoso(a), leal, bom(boa) ouvinte; alguém em quem se pode confiar.",
        "motiva": "Propósito; segurança e bem-estar das pessoas próximas.",
        "competencias": ["Foco no cliente", "Trabalho em equipe", "Resiliência", "Produtividade"],
        "forcas": [
            "Desenvolve rotinas e procedimentos de trabalho.",
            "Sabe ouvir e colaborar para o sucesso da equipe.",
            "Mantém a consistência da operação.",
        ],
        "atencao": "Pode atuar mais lentamente, apegar-se à rotina e resistir a mudanças.",
        "como_prefere": {
            "Apoio emocional": "Atenção e reconhecimento da importância do que faz.",
            "Prazo": "Prefere que o prazo seja acordado junto.",
            "Orientações": "Precisa de direção clara.",
            "Acompanhamento": "Percebe o acompanhamento como apoio.",
            "Reuniões": "Valoriza feedback e oportunidade de ajudar.",
        },
        "vulnerabilidades": [
            "Dificuldade de dizer não e de se posicionar.",
            "Guarda incômodos em vez de falar.",
            "Resistência a mudanças e demora para decidir.",
        ],
        "estresse": [
            "Mudanças bruscas e falta de aviso.",
            "Conflito e ambiente hostil.",
            "Pressão por velocidade sem recursos e informações.",
            "Sentir que o trabalho não tem propósito.",
        ],
        "desenvolver": [
            ("Adaptação a mudanças e iniciativa", "Projetos e iniciativas, Feedforward"),
            ("Decisão e agilidade", "Matriz de prioridades, Plano de ação"),
            ("Visão estratégica", "Mini-BSC, Criação do plano"),
            ("Posicionamento e assertividade", "Feedback Sanduíche, Ferramenta Avião"),
        ],
    },
    "C": {
        "nome": "Conformidade",
        "cor": "#2F6BC1",
        "emocao": "Aversão",
        "resumo": "Foco em qualidade, precisão e método. Analisa a fundo e busca fazer certo da primeira vez.",
        "caracteristicas": "Crítico(a), seletivo(a), detalhista e observador(a).",
        "motiva": "Desafio técnico; ter tudo planejado.",
        "competencias": ["Análise", "Controle de atividades", "Planejamento e organização", "Solução de problemas"],
        "forcas": [
            "Compreende toda a situação, até o último detalhe.",
            "É persistente na solução de problemas lógicos e difíceis.",
            "Identifica problemas de imprecisão de informação.",
        ],
        "atencao": "Pode demorar a decidir, ter dificuldade de separar o geral do particular e ser difícil de aproximar.",
        "como_prefere": {
            "Apoio emocional": "Precisa de muito pouco.",
            "Prazo": "Prioridades e cronograma claros.",
            "Orientações": "Aceita como parte do processo.",
            "Acompanhamento": "Dispensa acompanhamento próximo.",
            "Reuniões": "Com pauta e objetividade; pouca paciência com divagação.",
        },
        "vulnerabilidades": [
            "Perfeccionismo e autocrítica excessiva.",
            "Adia a decisão à espera de mais dados.",
            "Tende a se isolar e a evitar contato.",
        ],
        "estresse": [
            "Erros, retrabalho e falta de processo.",
            "Regras e prioridades mudando sem explicação.",
            "Cobrança sem prazo claro ou sem informação.",
            "Ambiente desorganizado.",
        ],
        "desenvolver": [
            ("Decisão com informação suficiente", "Matriz de prioridades, Plano de ação"),
            ("Visão do todo", "Mini-BSC, Ferramenta Avião"),
            ("Relacionamento e comunicação", "Conhecer o liderado, Reuniões e feedbacks"),
            ("Flexibilidade e trabalho em equipe", "Comece-Pare-Continue, Reconhecimento da evolução"),
        ],
    },
}

# Encaixe por tipo de atividade (pág. 5). Classes: otimo, bom, regular, apoio
ENCAIXE = [
    ("Atividade sem processo definido", {"D": ("Ótimo", "otimo"), "I": ("Precisa de acompanhamento", "apoio"), "S": ("Regular", "regular"), "C": ("Bom", "bom")}),
    ("Atividade que exige criar processos", {"D": ("Bom", "bom"), "I": ("Precisa de um modelo", "apoio"), "S": ("Regular", "regular"), "C": ("Ótimo", "otimo")}),
    ("Entrega que exige agilidade", {"D": ("Ótimo", "otimo"), "I": ("Bom", "bom"), "S": ("Precisa de recursos e informações", "apoio"), "C": ("Regular", "regular")}),
    ("Precisão: detalhes", {"D": ("Excelente para enxergar detalhes", "otimo"), "I": ("Falta de atenção", "apoio"), "S": ("Regular", "regular"), "C": ("Ótimo", "otimo")}),
    ("Precisão: consistência da operação", {"D": ("Regular", "regular"), "I": ("Precisa de ajuda", "apoio"), "S": ("Excelente", "otimo"), "C": ("Ótimo", "otimo")}),
    ("Precisão: dados e informação", {"D": ("Ótimo", "otimo"), "I": ("Precisa de ajuda", "apoio"), "S": ("Regular", "regular"), "C": ("Excelente", "otimo")}),
]

AVISO = (
    "Este resultado é um guia de conversa, não um rótulo. Perfil é tendência, não "
    "limite: todas as pessoas usam os quatro estilos em algum grau. O questionário é "
    "uma ferramenta interna de desenvolvimento, não validada para seleção ou "
    "avaliação de desempenho."
)

RESUMO_EQUILIBRADO = (
    "Os quatro estilos aparecem em intensidade parecida. Você tende a adaptar o "
    "comportamento a cada situação; o detalhamento a seguir usa o estilo com maior "
    "pontuação como referência."
)


def resumo(resultado: dict) -> str:
    return RESUMO_EQUILIBRADO if resultado.get("equilibrado") else PERFIS[resultado["principal"]]["resumo"]
