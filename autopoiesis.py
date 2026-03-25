"""
╔══════════════════════════════════════════════════════════════════════╗
║ PEÇA #23 — AUTOPOIESIS ║
║ Formas Múltiplas de Continuidade no Espaço ║
║ Alexandre Mury, 2024 ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import random
import datetime
import os
import json
import argparse
import sys
import requests

# ─── BANCO DE DADOS CONCEITUAL (mantido igual) ───────────────────────────────
# ... (cole aqui todo o CONCEITOS, PARADOXOS, ESPACOS_POSSIVEIS, DURACAO_POSSIVEIS, INSTRUCOES_PARADOXAIS exatamente como estava no seu arquivo)

# (Para não ficar gigante, assuma que você mantém as seções CONCEITOS até INSTRUCOES_PARADOXAIS iguais ao que enviou antes)

# ─── LLM LOCAL (OLLAMA) ─────────────────────────────────────────────────────
def chamar_llm_autopoiesis(conceito: str, temperatura: float = 0.9) -> dict:
    prompt = f"""Você é um colaborador poético-irônico da obra "Autopoiesis" de Alexandre Mury (2024).
Conceito ativado: {conceito}

Gere APENAS um JSON válido:

{{
  "referencias": ["ref1 — breve descrição", "ref2", "ref3"],
  "materiais": ["material1 (poético)", "material2", "material3", "material4"],
  "verbos_acao": ["verbo1", "verbo2", "verbo3"],
  "paradoxo": "Descrição completa do paradoxo",
  "instrucao_montagem": "Instrução poética de montagem com impossibilidade sutil",
  "protocolo_inviolavel": "Instrução que torna a execução impossível ou contingente"
}}

Mantenha precariedade, ironia e continuidade sem fim. Evite materiais muito perigosos."""

    try:
        r = requests.post(
            "http://127.0.0.1:11434/api/chat",
            json={
                "model": "qwen3:14b",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": temperatura}
            },
            timeout=120
        )
        content = r.json()["message"]["content"].strip()
        if "```" in content:
            content = content.split("```")[1].replace("json", "").strip()
        return json.loads(content)
    except Exception as e:
        print(f"[Autopoiesis] Ollama não respondeu → usando listas fixas. Erro: {e}")
        return {}

# ─── CONTADOR (mantido igual) ───────────────────────────────────────────────
def obter_numero_manifesto(...):  # mantenha sua função original

# ─── MODO INTERATIVO (mantido igual) ────────────────────────────────────────

# ─── NÚCLEO GENERATIVO ATUALIZADO ───────────────────────────────────────────
def gerar_manifesto_dados(conceito, usar_llm=False):
    # Listas fixas
    refs = random.sample(CONCEITOS[conceito]["referencias"], k=random.randint(2,4))
    mats = random.sample(CONCEITOS[conceito]["materiais"], k=random.randint(2,4))
    verbo = random.choice(CONCEITOS[conceito]["verbos_de_acao"])
    paradoxo_nome = random.choice(list(PARADOXOS.keys()))
    instrucao = random.choice(INSTRUCOES_PARADOXAIS)
    espaco = random.choice(ESPACOS_POSSIVEIS)
    duracao = random.choice(DURACAO_POSSIVEIS)

    if usar_llm:
        llm_data = chamar_llm_autopoiesis(conceito)
        if llm_data:
            refs = list(set(refs + llm_data.get("referencias", [])))[:5]
            mats = list(set(mats + llm_data.get("materiais", [])))[:6]
            if llm_data.get("verbos_acao"):
                verbo = random.choice(CONCEITOS[conceito]["verbos_de_acao"] + llm_data["verbos_acao"])
            if llm_data.get("protocolo_inviolavel"):
                instrucao = llm_data["protocolo_inviolavel"]

    # Justaposição
    a, b = (mats * 2)[:2]
    justaposicao = PARADOXOS[paradoxo_nome]["logica_combinatoria"](a, b)

    return {
        "conceito": conceito,
        "glifo": CONCEITOS[conceito]["glifo"],
        "tom": CONCEITOS[conceito]["tom"],
        "referencias": refs,
        "materiais": mats,
        "paradoxo": paradoxo_nome,
        "descricao_p": PARADOXOS[paradoxo_nome]["descricao"],
        "justaposicao": justaposicao,
        "verbo": verbo,
        "instrucao": instrucao,
        "espaco": espaco,
        "duracao": duracao,
    }

# ─── formatar_texto, salvar_txt, salvar_pdf (mantenha exatamente como estavam) ───

# ─── MAIN CORRIGIDO ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Autopoiesis")
    parser.add_argument("--conceito", choices=["Memória", "Contingência", "Projeção"], default=None)
    parser.add_argument("--txt", action="store_true")
    parser.add_argument("--pdf", action="store_true")
    parser.add_argument("--llm", action="store_true", help="Usar Ollama para expandir o manifesto")

    args = parser.parse_args()

    conceito = args.conceito or modo_interativo()

    numero = obter_numero_manifesto()
    dados = gerar_manifesto_dados(conceito, usar_llm=args.llm)
    timestamp = datetime.datetime.now().strftime("%Y.%m.%d — %H:%M:%S")

    texto = formatar_texto(numero, dados, timestamp)
    print(texto)

    if args.txt:
        salvar_txt(numero, texto)
    if args.pdf:
        salvar_pdf(numero, dados, timestamp)

if __name__ == "__main__":
    main()
