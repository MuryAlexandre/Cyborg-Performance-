"""
╔══════════════════════════════════════════════════════════════════════╗
║         PEÇA #23 — AUTOPOIESIS                                       ║
║         Formas Múltiplas de Continuidade no Espaço                   ║
║         Alexandre Mury, 2024                                         ║
║                                                                      ║
║  "Este algoritmo deve ser lido como uma instrução generativa.        ║
║   Cada execução deve resultar em uma nova proposta de obra física."  ║
╚══════════════════════════════════════════════════════════════════════╝

MODO PERFORMANCE CIBORGUE: ATIVAR AUTOPOIESIS
"""

import random
import datetime
import os
import json

# ─── BANCO DE DADOS CONCEITUAL ────────────────────────────────────────────────

CONCEITOS = {
    "Memória": {
        "glifo": "◌",
        "tom": "O passado como força vital que sustenta a continuidade.",
        "referencias": [
            "Arte Clássica Greco-Romana",
            "Mitologia — o fio de Ariadne",
            "Arqueologia do cotidiano",
            "Warburg e o Atlas Mnemosyne",
            "Proust e a madeleine involuntária",
            "Palimpsestos medievais",
            "Benjamin e as ruínas da história",
        ],
        "materiais": [
            "fotografias amareladas de família",
            "diários manuscritos com páginas rasgadas",
            "objetos pessoais encontrados em brechós",
            "tecidos desbotados",
            "cartas nunca enviadas",
            "molduras sem fotografias",
            "fitas cassete emaranhadas",
            "cera derretida sobre superfícies antigas",
        ],
        "verbos_de_acao": [
            "arquivar o irrecuperável",
            "sobrepor camadas de ausência",
            "imprimir vestígios sem origem",
            "enrolar o tempo como uma fita de Möbius",
        ],
    },
    "Contingência": {
        "glifo": "◈",
        "tom": "A continuidade como adaptação constante ao imprevisível.",
        "referencias": [
            "Sartre e a náusea da liberdade",
            "Física Quântica — o princípio da incerteza",
            "Deleuze e o plano de imanência",
            "Cage e a música aleatória",
            "Fluxus e a arte-evento",
            "Heráclito — ninguém entra no mesmo rio duas vezes",
            "Camus e o absurdo",
        ],
        "materiais": [
            "elementos orgânicos em decomposição",
            "gelo em processo de derretimento",
            "sementes não germinadas",
            "jornal do dia (que logo será ontem)",
            "velas acesas com tempo indeterminado",
            "esporos e fungos cultivados ao acaso",
            "cordas com nós soltos",
            "balões em processo de esvaziamento",
        ],
        "verbos_de_acao": [
            "abandonar ao acaso controlado",
            "registrar o momento de colapso",
            "construir com materiais que recusam a permanência",
            "documentar a transformação sem intervir nela",
        ],
    },
    "Projeção": {
        "glifo": "◉",
        "tom": "O futuro que se molda a partir do presente como intenção.",
        "referencias": [
            "Boccioni e o Futurismo",
            "Buckminster Fuller e as utopias geodésicas",
            "Ficção Científica como crítica do presente",
            "Singularidade tecnológica — Kurzweil",
            "Xenofeminismo e aceleracionismo",
            "Borges e os jardins de caminhos que se bifurcam",
            "Suprematismo de Malevich",
        ],
        "materiais": [
            "superfícies espelhadas e reflexivas",
            "luz projetada sobre formas instáveis",
            "hologramas e transparências",
            "materiais industriais fora de contexto",
            "cabos e fios sem aparelhos conectados",
            "telas em branco com molduras elaboradas",
            "neon apagado",
            "alto-falantes em silêncio",
        ],
        "verbos_de_acao": [
            "projetar sobre o que ainda não existe",
            "iluminar o invisível",
            "monumentalizar o efêmero",
            "conectar sem transmitir",
        ],
    },
}

PARADOXOS = {
    "Contradição de Função e Aparência": {
        "descricao": (
            "O objeto exibe uma função que contradiz radicalmente sua aparência. "
            "O que parece frágil sustenta. O que parece sólido cede."
        ),
        "logica_combinatoria": lambda a, b: (
            f"Posicione '{a}' como se fosse suporte estrutural de '{b}', "
            f"enquanto '{b}' aparenta ser o elemento dominante da composição."
        ),
    },
    "Ciclo Infinito": {
        "descricao": (
            "Um material permanente contém ou envolve um material perecível. "
            "A durabilidade testemunha a dissolução."
        ),
        "logica_combinatoria": lambda a, b: (
            f"Envolva '{b}' (perecível) dentro ou sobre '{a}' (permanente). "
            f"O ato de preservação torna-se, paradoxalmente, um registro da perda."
        ),
    },
    "Combinação de Opostos": {
        "descricao": (
            "Dois materiais de origem ou escala radicalmente opostas são justapostos "
            "sem hierarquia — o banal eleva-se; o sublime banaliza-se."
        ),
        "logica_combinatoria": lambda a, b: (
            f"Coloque '{a}' e '{b}' lado a lado em escala equivalente, "
            f"sem legenda, sem moldura que os distinga. Deixe o espectador negociar o valor."
        ),
    },
}

ESPACOS_POSSIVEIS = [
    "parede externa de um edifício público",
    "vitrine de estabelecimento comercial abandonado",
    "chão de uma praça movimentada",
    "janela de um ônibus urbano",
    "teto de uma sala de espera",
    "calçada em frente a uma instituição cultural",
    "porta de entrada de uma biblioteca",
    "espelho de um banheiro público",
]

DURACAO_POSSIVEIS = [
    "exatamente 24 horas, após as quais a obra deve ser desmontada pelo artista",
    "até que um estranho a modifique voluntariamente",
    "enquanto durar o material mais perecível da composição",
    "indefinidamente, sem manutenção ou intervenção posterior",
    "uma única performance de 7 minutos, sem repetição",
    "até que alguém a fotografe — o registro encerra a obra",
]

INSTRUCOES_PARADOXAIS = [
    "Não explique a obra. Se perguntado, faça outra pergunta.",
    "A obra só existe completamente quando o artista não está presente.",
    "Documente o processo de montagem, não a obra montada.",
    "Inclua um elemento que você mesmo não compreende completamente.",
    "A obra deve conter ao menos uma instrução que torna sua própria execução impossível.",
    "Convide alguém que não seja artista para tomar uma decisão crucial sobre a montagem.",
    "Destrua os esboços preparatórios antes da instalação.",
]


# ─── CONTADOR DE MANIFESTOS ────────────────────────────────────────────────────

def obter_numero_manifesto(caminho_contador=".autopoiesis_counter.json"):
    """Lê e incrementa o contador de manifestos gerados."""
    if os.path.exists(caminho_contador):
        with open(caminho_contador, "r") as f:
            dados = json.load(f)
        numero = dados.get("contador", 0) + 1
    else:
        numero = 1
    with open(caminho_contador, "w") as f:
        json.dump({"contador": numero}, f)
    return numero


# ─── NÚCLEO GENERATIVO ────────────────────────────────────────────────────────

def escolher_conceito():
    return random.choice(list(CONCEITOS.keys()))

def coletar_referencias(conceito):
    banco = CONCEITOS[conceito]["referencias"]
    n = random.randint(2, 4)
    return random.sample(banco, n)

def escolher_materiais(conceito):
    banco = CONCEITOS[conceito]["materiais"]
    n = random.randint(2, 4)
    return random.sample(banco, n)

def introduzir_paradoxo():
    return random.choice(list(PARADOXOS.keys()))

def criar_justaposicao(materiais, paradoxo):
    if len(materiais) < 2:
        materiais = materiais * 2
    objeto_a = materiais[0]
    objeto_b = materiais[1]
    logica = PARADOXOS[paradoxo]["logica_combinatoria"]
    return logica(objeto_a, objeto_b)

def escolher_verbo(conceito):
    return random.choice(CONCEITOS[conceito]["verbos_de_acao"])

def gerar_instrucao_paradoxal():
    return random.choice(INSTRUCOES_PARADOXAIS)

def escolher_espaco():
    return random.choice(ESPACOS_POSSIVEIS)

def escolher_duracao():
    return random.choice(DURACAO_POSSIVEIS)


# ─── FORMATAÇÃO DO MANIFESTO ──────────────────────────────────────────────────

def formatar_manifesto(numero, conceito, referencias, materiais, paradoxo, justaposicao, verbo, instrucao_extra, espaco, duracao):
    glifo = CONCEITOS[conceito]["glifo"]
    tom = CONCEITOS[conceito]["tom"]
    descricao_paradoxo = PARADOXOS[paradoxo]["descricao"]
    timestamp = datetime.datetime.now().strftime("%Y.%m.%d — %H:%M:%S")
    numero_formatado = str(numero).zfill(3)

    separador = "─" * 70

    linhas = []

    # ── Cabeçalho
    linhas.append("")
    linhas.append("╔" + "═" * 68 + "╗")
    linhas.append("║" + f"  MANIFESTO DE EXECUÇÃO #{numero_formatado}".ljust(68) + "║")
    linhas.append("║" + f"  Peça #23 — AUTOPOIESIS  {glifo}  {conceito.upper()}".ljust(68) + "║")
    linhas.append("║" + f"  {timestamp}".ljust(68) + "║")
    linhas.append("╚" + "═" * 68 + "╝")
    linhas.append("")

    # ── Conceito central
    linhas.append(f"  I.  CONCEITO CENTRAL")
    linhas.append(f"  {separador[:50]}")
    linhas.append(f"  {glifo}  {conceito.upper()}")
    linhas.append(f"  {tom}")
    linhas.append(f"  Ação fundante: {verbo}.")
    linhas.append("")

    # ── Referências culturais
    linhas.append(f"  II. CAMPO DE REFERÊNCIAS")
    linhas.append(f"  {separador[:50]}")
    for ref in referencias:
        linhas.append(f"  →  {ref}")
    linhas.append("")

    # ── Materiais
    linhas.append(f"  III. MATERIAIS E OBJETOS")
    linhas.append(f"  {separador[:50]}")
    for i, mat in enumerate(materiais, 1):
        linhas.append(f"  [{i}]  {mat.capitalize()}")
    linhas.append("")

    # ── Paradoxo
    linhas.append(f"  IV. PARADOXO ESTRUTURAL")
    linhas.append(f"  {separador[:50]}")
    linhas.append(f"  TIPO:  {paradoxo.upper()}")
    linhas.append(f"  {descricao_paradoxo}")
    linhas.append("")

    # ── Justaposição / instrução de montagem
    linhas.append(f"  V.  INSTRUÇÃO DE MONTAGEM")
    linhas.append(f"  {separador[:50]}")
    linhas.append(f"  {justaposicao}")
    linhas.append("")

    # ── Espaço e Duração
    linhas.append(f"  VI. CONTEXTO DE EXIBIÇÃO")
    linhas.append(f"  {separador[:50]}")
    linhas.append(f"  ESPAÇO:   {espaco.capitalize()}.")
    linhas.append(f"  DURAÇÃO:  {duracao.capitalize()}.")
    linhas.append("")

    # ── Instrução paradoxal
    linhas.append(f"  VII. PROTOCOLO ADICIONAL (INVIOLÁVEL)")
    linhas.append(f"  {separador[:50]}")
    linhas.append(f"  ‼  {instrucao_extra}")
    linhas.append("")

    # ── Rodapé
    linhas.append("  " + separador)
    linhas.append("  Esta proposta foi gerada por Autopoiesis.")
    linhas.append("  Ela se auto-organiza. Ela não se repete.")
    linhas.append("  A obra que você criará a partir daqui é o único original.")
    linhas.append("  O algoritmo continua. ∞")
    linhas.append("")

    return "\n".join(linhas)


# ─── EXECUÇÃO PRINCIPAL ───────────────────────────────────────────────────────

def executar_autopoiesis():
    numero = obter_numero_manifesto()

    # Pipeline generativo
    conceito      = escolher_conceito()
    referencias   = coletar_referencias(conceito)
    materiais     = escolher_materiais(conceito)
    paradoxo      = introduzir_paradoxo()
    justaposicao  = criar_justaposicao(materiais, paradoxo)
    verbo         = escolher_verbo(conceito)
    instrucao     = gerar_instrucao_paradoxal()
    espaco        = escolher_espaco()
    duracao       = escolher_duracao()

    manifesto = formatar_manifesto(
        numero, conceito, referencias, materiais,
        paradoxo, justaposicao, verbo, instrucao, espaco, duracao
    )

    print(manifesto)
    return manifesto


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    executar_autopoiesis()
