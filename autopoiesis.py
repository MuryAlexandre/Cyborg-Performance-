"""
╔══════════════════════════════════════════════════════════════════════╗
║ PEÇA #23 — AUTOPOIESIS ║
║ Formas Múltiplas de Continuidade no Espaço ║
║ Alexandre Mury, 2024 ║
╚══════════════════════════════════════════════════════════════════════╝
USO:
  python autopoiesis.py → modo interativo
  python autopoiesis.py --conceito Memória --llm → usa LLM + listas fixas
  python autopoiesis.py --conceito Contingência --pdf --llm
"""
import random
import datetime
import os
import json
import argparse
import sys
import requests

# ─── BANCO DE DADOS CONCEITUAL ────────────────────────────────────────────────
CONCEITOS = { ... }   # (mantido exatamente igual ao que você enviou)

PARADOXOS = { ... }   # (mantido igual)

ESPACOS_POSSIVEIS = [ ... ]   # (mantido igual)

DURACAO_POSSIVEIS = [ ... ]   # (mantido igual)

INSTRUCOES_PARADOXAIS = [ ... ]   # (mantido igual)

# ─── LLM LOCAL (OLLAMA) - VERSÃO AGRESSIVA GRÁTIS ─────────────────────────────
def chamar_llm_autopoiesis(conceito: str, temperatura: float = 0.92) -> dict:
    """Expande o pseudocódigo original usando Ollama (100% grátis)."""
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
                "model": "qwen3:14b",   # mude para qwen3:8b se quiser mais leve
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": temperatura, "num_ctx": 8192}
            },
            timeout=180
        )
        content = response.json()["message"]["content"].strip()

        if content.startswith("```"):
            content = content.split("```")[1].strip()
            if content.startswith("json"):
                content = content[4:].strip()

        return json.loads(content)
    except Exception as e:
        print(f"[Autopoiesis] LLM fallback ativado (Ollama não encontrado): {e}")
        return {}

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
    # (mantido exatamente igual ao que você enviou)
    ...

# ─── NÚCLEO GENERATIVO ATUALIZADO ─────────────────────────────────────────────
def gerar_manifesto_dados(conceito, usar_llm=False):
    # Parte fixa (sementes do pseudocódigo original)
    referencias = random.sample(CONCEITOS[conceito]["referencias"], random.randint(2, 4))
    materiais = random.sample(CONCEITOS[conceito]["materiais"], random.randint(2, 4))
    paradoxo_nome = random.choice(list(PARADOXOS.keys()))
    verbo = random.choice(CONCEITOS[conceito]["verbos_de_acao"])
    instrucao = random.choice(INSTRUCOES_PARADOXAIS)
    espaco = random.choice(ESPACOS_POSSIVEIS)
    duracao = random.choice(DURACAO_POSSIVEIS)

    # Expansão com LLM (se ativado)
    if usar_llm:
        dados_llm = chamar_llm_autopoiesis(conceito)
        if dados_llm:
            referencias = list(set(referencias + dados_llm.get("referencias", [])))[:5]
            materiais = list(set(materiais + dados_llm.get("materiais", [])))[:6]
            verbo = random.choice(CONCEITOS[conceito]["verbos_de_acao"] + dados_llm.get("verbos_acao", []))
            if "paradoxo" in dados_llm:
                paradoxo_nome = "Paradoxo Gerado pelo LLM"
                PARADOXOS["Paradoxo Gerado pelo LLM"] = {
                    "descricao": dados_llm.get("paradoxo", ""),
                    "logica_combinatoria": lambda a, b: dados_llm.get("instrucao_montagem", "")
                }
            if "protocolo_inviolavel" in dados_llm:
                instrucao = dados_llm["protocolo_inviolavel"]

    # Justaposição
    mats = materiais if len(materiais) >= 2 else materiais * 2
    justaposicao = PARADOXOS[paradoxo_nome]["logica_combinatoria"](mats[0], mats[1])

    return {
        "conceito": conceito,
        "glifo": CONCEITOS[conceito]["glifo"],
        "tom": CONCEITOS[conceito]["tom"],
        "referencias": referencias,
        "materiais": materiais,
        "paradoxo": paradoxo_nome,
        "descricao_p": PARADOXOS[paradoxo_nome]["descricao"],
        "justaposicao": justaposicao,
        "verbo": verbo,
        "instrucao": instrucao,
        "espaco": espaco,
        "duracao": duracao,
    }

# ─── FORMATAÇÃO TEXTO ─────────────────────────────────────────────────────────
def formatar_texto(numero, d, timestamp):
    # (mantido exatamente igual ao que você enviou)
    ...

# ─── SALVAR TXT e PDF ─────────────────────────────────────────────────────────
# (mantidos exatamente iguais)

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Autopoiesis — Gerador de Manifestos de Arte",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--conceito", choices=["Memória", "Contingência", "Projeção"], default=None)
    parser.add_argument("--txt", action="store_true")
    parser.add_argument("--pdf", action="store_true")
    parser.add_argument("--llm", action="store_true", help="Ativar expansão com Ollama (LLM local grátis)")

    args = parser.parse_args()

    if args.conceito:
        conceito = args.conceito
    else:
        conceito = modo_interativo()

    numero = obter_numero_manifesto()
    dados = gerar_manifesto_dados(conceito, usar_llm=args.llm)
    timestamp = datetime.datetime.now().strftime("%Y.%m.%d — %H:%M:%S")

    texto = formatar_texto(numero, dados, timestamp)
    print(texto)

    if args.txt:
        salvar_txt(numero, texto)
    if args.pdf:
        salvar_pdf(numero, dados, timestamp)
    if not args.txt and not args.pdf:
        print(" (use --txt e/ou --pdf para salvar em arquivo)")

if __name__ == "__main__":
    main()
