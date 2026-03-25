"""
╔══════════════════════════════════════════════════════════════════════╗
║         PEÇA #23 — AUTOPOIESIS                                       ║
║         Formas Múltiplas de Continuidade no Espaço                   ║
║         Alexandre Mury, 2024                                         ║
╚══════════════════════════════════════════════════════════════════════╝

USO:
  python autopoiesis.py                          → modo interativo
  python autopoiesis.py --conceito Memória       → conceito fixo
  python autopoiesis.py --conceito Projeção --pdf        → salva PDF
  python autopoiesis.py --conceito Contingência --txt    → salva TXT
  python autopoiesis.py --conceito Memória --pdf --txt   → salva ambos
"""

import random
import datetime
import os
import json
import argparse
import sys

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
            "Dois materiais de origem ou escala radicalmente opostas são "
            "justapostos sem hierarquia — o banal eleva-se; o sublime banaliza-se."
        ),
        "logica_combinatoria": lambda a, b: (
            f"Coloque '{a}' e '{b}' lado a lado em escala equivalente, "
            f"sem legenda, sem moldura que os distinga. "
            f"Deixe o espectador negociar o valor."
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

# ─── LLM LOCAL (OLLAMA) - VERSÃO AGRESSIVA GRÁTIS ─────────────────────────────

import requests
import json

def chamar_llm_autopoiesis(conceito: str, temperatura: float = 0.92) -> dict:
    """
    Expande o pseudocódigo original usando Ollama (100% grátis e local).
    Gera referências, materiais, paradoxos e instruções novas e poéticas.
    """
    prompt = f"""Você é um colaborador poético-irônico da obra "Autopoiesis" de Alexandre Mury (2024).
Seu papel é expandir o pseudocódigo original de forma conceitual, viva e paradoxal.

Conceito ativado: {conceito}

Gere **apenas** um JSON válido com esta estrutura exata:

{{
  "referencias": ["ref1 — breve descrição poética", "ref2", "ref3"],
  "materiais": ["material1 (qualidade poética)", "material2", "material3", "material4"],
  "verbos_acao": ["verbo1", "verbo2", "verbo3"],
  "paradoxo": "Descrição completa do paradoxo estrutural (belo, contraditório, autopoético)",
  "instrucao_montagem": "Instrução de montagem por justaposição, poética, com uma camada sutil de impossibilidade",
  "protocolo_inviolavel": "Uma instrução que torna a execução impossível ou extremamente contingente"
}}

Mantenha o espírito: precariedade, continuidade sem fim, ironia conceitual, tensão entre humano e máquina.
Evite materiais extremamente perigosos.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen3:14b",   # ← altere se usar outro modelo (ex: qwen3:8b, gemma3:12b)
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": temperatura, "num_ctx": 8192}
            },
            timeout=180
        )
        content = response.json()["message"]["content"].strip()

        # Limpeza caso o modelo coloque ```json
        if content.startswith("```"):
            content = content.split("```")[1].strip()
            if content.startswith("json"):
                content = content[4:].strip()

        return json.loads(content)
    except Exception as e:
        print(f"[Autopoiesis] LLM fallback ativado: {e}")
        return {}   # volta para as listas fixas antigas
      
# ─── CONTADOR PERSISTENTE ─────────────────────────────────────────────────────

def obter_numero_manifesto(caminho_contador=".autopoiesis_counter.json"):
    if os.path.exists(caminho_contador):
        with open(caminho_contador, "r") as f:
            dados = json.load(f)
        numero = dados.get("contador", 0) + 1
    else:
        numero = 1
    with open(caminho_contador, "w") as f:
        json.dump({"contador": numero}, f)
    return numero

# ─── MODO INTERATIVO ──────────────────────────────────────────────────────────

def modo_interativo():
    """Apresenta menu visual no terminal e retorna o conceito escolhido."""
    opcoes = list(CONCEITOS.keys())

    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║   AUTOPOIESIS — ESCOLHA O CONCEITO CENTRAL  ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()
    for i, nome in enumerate(opcoes, 1):
        glifo = CONCEITOS[nome]["glifo"]
        tom   = CONCEITOS[nome]["tom"]
        print(f"  [{i}]  {glifo}  {nome.upper()}")
        print(f"       {tom}")
        print()
    print("  [0]  Escolha aleatória (deixar o algoritmo decidir)")
    print()

    while True:
        try:
            entrada = input("  → Digite o número da sua escolha: ").strip()
            n = int(entrada)
            if n == 0:
                return random.choice(opcoes)
            elif 1 <= n <= len(opcoes):
                return opcoes[n - 1]
            else:
                print(f"  ⚠  Digite um número entre 0 e {len(opcoes)}.")
        except (ValueError, EOFError):
            print("  ⚠  Entrada inválida. Tente novamente.")

# ─── NÚCLEO GENERATIVO ────────────────────────────────────────────────────────

def gerar_manifesto_dados(conceito):
    referencias  = random.sample(CONCEITOS[conceito]["referencias"], random.randint(2, 4))
    materiais    = random.sample(CONCEITOS[conceito]["materiais"],    random.randint(2, 4))
    paradoxo     = random.choice(list(PARADOXOS.keys()))
    mats         = materiais if len(materiais) >= 2 else materiais * 2
    justaposicao = PARADOXOS[paradoxo]["logica_combinatoria"](mats[0], mats[1])
    verbo        = random.choice(CONCEITOS[conceito]["verbos_de_acao"])
    instrucao    = random.choice(INSTRUCOES_PARADOXAIS)
    espaco       = random.choice(ESPACOS_POSSIVEIS)
    duracao      = random.choice(DURACAO_POSSIVEIS)
    return {
        "conceito":     conceito,
        "glifo":        CONCEITOS[conceito]["glifo"],
        "tom":          CONCEITOS[conceito]["tom"],
        "referencias":  referencias,
        "materiais":    materiais,
        "paradoxo":     paradoxo,
        "descricao_p":  PARADOXOS[paradoxo]["descricao"],
        "justaposicao": justaposicao,
        "verbo":        verbo,
        "instrucao":    instrucao,
        "espaco":       espaco,
        "duracao":      duracao,
    }

# ─── FORMATAÇÃO TEXTO ─────────────────────────────────────────────────────────

def formatar_texto(numero, d, timestamp):
    sep  = "─" * 50
    num  = str(numero).zfill(3)
    L    = []

    L.append("")
    L.append("╔" + "═" * 68 + "╗")
    L.append("║" + f"  MANIFESTO DE EXECUÇÃO #{num}".ljust(68) + "║")
    L.append("║" + f"  Peça #23 — AUTOPOIESIS  {d['glifo']}  {d['conceito'].upper()}".ljust(68) + "║")
    L.append("║" + f"  {timestamp}".ljust(68) + "║")
    L.append("╚" + "═" * 68 + "╝")
    L.append("")

    L.append(f"  I.  CONCEITO CENTRAL")
    L.append(f"  {sep}")
    L.append(f"  {d['glifo']}  {d['conceito'].upper()}")
    L.append(f"  {d['tom']}")
    L.append(f"  Ação fundante: {d['verbo']}.")
    L.append("")

    L.append(f"  II. CAMPO DE REFERÊNCIAS")
    L.append(f"  {sep}")
    for ref in d["referencias"]:
        L.append(f"  →  {ref}")
    L.append("")

    L.append(f"  III. MATERIAIS E OBJETOS")
    L.append(f"  {sep}")
    for i, mat in enumerate(d["materiais"], 1):
        L.append(f"  [{i}]  {mat.capitalize()}")
    L.append("")

    L.append(f"  IV. PARADOXO ESTRUTURAL")
    L.append(f"  {sep}")
    L.append(f"  TIPO:  {d['paradoxo'].upper()}")
    L.append(f"  {d['descricao_p']}")
    L.append("")

    L.append(f"  V.  INSTRUÇÃO DE MONTAGEM")
    L.append(f"  {sep}")
    L.append(f"  {d['justaposicao']}")
    L.append("")

    L.append(f"  VI. CONTEXTO DE EXIBIÇÃO")
    L.append(f"  {sep}")
    L.append(f"  ESPAÇO:   {d['espaco'].capitalize()}.")
    L.append(f"  DURAÇÃO:  {d['duracao'].capitalize()}.")
    L.append("")

    L.append(f"  VII. PROTOCOLO ADICIONAL (INVIOLÁVEL)")
    L.append(f"  {sep}")
    L.append(f"  ‼  {d['instrucao']}")
    L.append("")

    L.append("  " + "─" * 68)
    L.append("  Esta proposta foi gerada por Autopoiesis.")
    L.append("  Ela se auto-organiza. Ela não se repete.")
    L.append("  A obra que você criará a partir daqui é o único original.")
    L.append("  O algoritmo continua. ∞")
    L.append("")

    return "\n".join(L)

# ─── SALVAR TXT ───────────────────────────────────────────────────────────────

def salvar_txt(numero, texto):
    nome = f"manifesto_{str(numero).zfill(3)}.txt"
    with open(nome, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"  ✓  TXT salvo → {nome}")
    return nome

# ─── SALVAR PDF ───────────────────────────────────────────────────────────────

def salvar_pdf(numero, d, timestamp):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
    )
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER

    nome = f"manifesto_{str(numero).zfill(3)}.pdf"
    num  = str(numero).zfill(3)

    # ── Paleta por conceito
    paletas = {
        "Memória":     {"fundo": colors.HexColor("#1a1410"), "acento": colors.HexColor("#c8a96e"), "texto": colors.HexColor("#e8ddd0")},
        "Contingência":{"fundo": colors.HexColor("#0f1a14"), "acento": colors.HexColor("#6ec8a0"), "texto": colors.HexColor("#d0e8dc")},
        "Projeção":    {"fundo": colors.HexColor("#0f1020"), "acento": colors.HexColor("#7090e8"), "texto": colors.HexColor("#d0d8f0")},
    }
    pal = paletas.get(d["conceito"], paletas["Memória"])

    doc = SimpleDocTemplate(
        nome,
        pagesize=A4,
        leftMargin=22*mm, rightMargin=22*mm,
        topMargin=20*mm,  bottomMargin=20*mm,
    )

    W, H = A4

    # ── Estilos
    s_titulo = ParagraphStyle("titulo",
        fontName="Helvetica-Bold", fontSize=9,
        textColor=pal["acento"], alignment=TA_CENTER,
        spaceAfter=2, leading=13)

    s_cabecalho = ParagraphStyle("cabecalho",
        fontName="Helvetica", fontSize=7.5,
        textColor=pal["texto"], alignment=TA_CENTER,
        spaceAfter=2, leading=11)

    s_secao = ParagraphStyle("secao",
        fontName="Helvetica-Bold", fontSize=8,
        textColor=pal["acento"], spaceBefore=10, spaceAfter=3)

    s_corpo = ParagraphStyle("corpo",
        fontName="Helvetica", fontSize=8.5,
        textColor=pal["texto"], spaceAfter=4, leading=13)

    s_item = ParagraphStyle("item",
        fontName="Helvetica", fontSize=8.5,
        textColor=pal["texto"], leftIndent=12, spaceAfter=3, leading=12)

    s_destaque = ParagraphStyle("destaque",
        fontName="Helvetica-Bold", fontSize=8.5,
        textColor=pal["acento"], spaceAfter=3)

    s_rodape = ParagraphStyle("rodape",
        fontName="Helvetica-Oblique", fontSize=7.5,
        textColor=colors.HexColor("#888888"), alignment=TA_CENTER,
        spaceBefore=6, leading=11)

    hr = lambda: HRFlowable(width="100%", thickness=0.4,
                            color=pal["acento"], spaceAfter=6, spaceBefore=2)

    def sp(n=1): return Spacer(1, n * 4)

    story = []

    # ── Fundo escuro via canvas callback
    def fundo_escuro(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(pal["fundo"])
        canvas.rect(0, 0, W, H, fill=1, stroke=0)
        canvas.restoreState()

    # ── Cabeçalho
    story.append(sp(2))
    story.append(Paragraph(f"MANIFESTO DE EXECUÇÃO #{num}", s_titulo))
    story.append(Paragraph(
        f"Peça #23 — AUTOPOIESIS  {d['glifo']}  {d['conceito'].upper()}", s_titulo))
    story.append(Paragraph(timestamp, s_cabecalho))
    story.append(sp(2))
    story.append(hr())

    # I. Conceito
    story.append(Paragraph("I.  CONCEITO CENTRAL", s_secao))
    story.append(Paragraph(f"{d['glifo']}  <b>{d['conceito'].upper()}</b>", s_destaque))
    story.append(Paragraph(d["tom"], s_corpo))
    story.append(Paragraph(f"Ação fundante: {d['verbo']}.", s_corpo))
    story.append(hr())

    # II. Referências
    story.append(Paragraph("II.  CAMPO DE REFERÊNCIAS", s_secao))
    for ref in d["referencias"]:
        story.append(Paragraph(f"→  {ref}", s_item))
    story.append(hr())

    # III. Materiais
    story.append(Paragraph("III.  MATERIAIS E OBJETOS", s_secao))
    for i, mat in enumerate(d["materiais"], 1):
        story.append(Paragraph(f"[{i}]  {mat.capitalize()}", s_item))
    story.append(hr())

    # IV. Paradoxo
    story.append(Paragraph("IV.  PARADOXO ESTRUTURAL", s_secao))
    story.append(Paragraph(f"TIPO:  {d['paradoxo'].upper()}", s_destaque))
    story.append(Paragraph(d["descricao_p"], s_corpo))
    story.append(hr())

    # V. Instrução
    story.append(Paragraph("V.  INSTRUÇÃO DE MONTAGEM", s_secao))
    story.append(Paragraph(d["justaposicao"], s_corpo))
    story.append(hr())

    # VI. Contexto
    story.append(Paragraph("VI.  CONTEXTO DE EXIBIÇÃO", s_secao))
    story.append(Paragraph(f"ESPAÇO:   {d['espaco'].capitalize()}.", s_corpo))
    story.append(Paragraph(f"DURAÇÃO:  {d['duracao'].capitalize()}.", s_corpo))
    story.append(hr())

    # VII. Protocolo
    story.append(Paragraph("VII.  PROTOCOLO ADICIONAL (INVIOLÁVEL)", s_secao))
    story.append(Paragraph(f"‼  {d['instrucao']}", s_destaque))
    story.append(hr())

    # Rodapé
    story.append(sp(3))
    story.append(Paragraph(
        "Esta proposta foi gerada por Autopoiesis.<br/>"
        "Ela se auto-organiza. Ela não se repete.<br/>"
        "A obra que você criará a partir daqui é o único original.<br/>"
        "O algoritmo continua.  ∞",
        s_rodape))

    doc.build(story, onFirstPage=fundo_escuro, onLaterPages=fundo_escuro)
    print(f"  ✓  PDF salvo → {nome}")
    return nome

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Autopoiesis — Gerador de Manifestos de Arte",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--conceito",
        choices=["Memória", "Contingência", "Projeção"],
        default=None,
        help="Conceito central fixo (ex: --conceito Memória)\n"
             "Se omitido, entra no modo interativo.",
    )
    parser.add_argument(
        "--txt",
        action="store_true",
        help="Salvar manifesto como arquivo .txt",
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Salvar manifesto como arquivo .pdf",
    )

    args = parser.parse_args()

    # Determinar conceito
    if args.conceito:
        conceito = args.conceito
    else:
        conceito = modo_interativo()

    numero    = obter_numero_manifesto()
    dados     = gerar_manifesto_dados(conceito)
    timestamp = datetime.datetime.now().strftime("%Y.%m.%d — %H:%M:%S")
    texto     = formatar_texto(numero, dados, timestamp)

    # Sempre imprime no terminal
    print(texto)

    # Salvar arquivos se solicitado
    if args.txt:
        salvar_txt(numero, texto)

    if args.pdf:
        salvar_pdf(numero, dados, timestamp)

    if not args.txt and not args.pdf:
        print("  (use --txt e/ou --pdf para salvar em arquivo)")
        print()


if __name__ == "__main__":
    main()
