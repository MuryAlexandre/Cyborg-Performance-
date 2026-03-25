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

# ─── BANCO DE DADOS CONCEITUAL ────────────────────────────────────────────────
# (Cole aqui exatamente o seu CONCEITOS, PARADOXOS, ESPACOS_POSSIVEIS, 
#  DURACAO_POSSIVEIS e INSTRUCOES_PARADOXAIS que você já tinha antes.
#  Para não ficar gigante, vou assumir que você vai colar eles no lugar certo.
#  Se quiser, posso te mandar só a parte nova. Por enquanto continue com os seus.)

# ─── LLM LOCAL (OLLAMA) ─────────────────────────────────────────────────────
def chamar_llm_autopoiesis(conceito: str, temperatura: float = 0.9) -> dict:
    prompt = f"""Você é um colaborador poético-irônico da obra "Autopoiesis" de Alexandre Mury (2024).
Conceito ativado: {conceito}

Gere **APENAS** um JSON válido com esta estrutura:

{{
  "referencias": ["ref1 — breve descrição poética", "ref2", "ref3"],
  "materiais": ["material1 (qualidade poética)", "material2", "material3", "material4"],
  "verbos_acao": ["verbo1", "verbo2", "verbo3"],
  "paradoxo": "Descrição completa do paradoxo estrutural",
  "instrucao_montagem": "Instrução de montagem poética com impossibilidade sutil",
  "protocolo_inviolavel": "Instrução que torna a execução impossível ou extremamente contingente"
}}

Mantenha o espírito de precariedade, continuidade sem fim e ironia conceitual. Evite materiais muito perigosos."""

    try:
        r = requests.post(
            "http://127.0.0.1:11434/api/chat",
            json={
                "model": "qwen3:14b",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": temperatura}
            },
            timeout=150
        )
        content = r.json()["message"]["content"].strip()
        if content.startswith("```"):
            content = content.split("```")[1].strip()
            if content.startswith("json"):
                content = content[4:].strip()
        return json.loads(content)
    except Exception as e:
        print(f"[Autopoiesis] Ollama não respondeu → usando listas fixas. ({e})")
        return {}

# ─── SUAS FUNÇÕES ANTIGAS (obter_numero_manifesto, modo_interativo, 
#     formatar_texto, salvar_txt, salvar_pdf) ───────────────────────────────
# Cole aqui todas as suas funções originais (do seu arquivo anterior)

# ─── NÚCLEO GENERATIVO ATUALIZADO ───────────────────────────────────────────
def gerar_manifesto_dados(conceito, usar_llm=False):
    # ... (use a versão que eu te mandei na mensagem anterior)
    # Se precisar, me avise que mando só esta função completa

    # Por enquanto, para testar rápido, vamos usar uma versão mínima:
    refs = random.sample(CONCEITOS[conceito]["referencias"], k=3)
    mats = random.sample(CONCEITOS[conceito]["materiais"], k=3)
    verbo = random.choice(CONCEITOS[conceito]["verbos_de_acao"])
    paradoxo_nome = random.choice(list(PARADOXOS.keys()))
    instrucao = random.choice(INSTRUCOES_PARADOXAIS)
    espaco = random.choice(ESPACOS_POSSIVEIS)
    duracao = random.choice(DURACAO_POSSIVEIS)

    if usar_llm:
        llm = chamar_llm_autopoiesis(conceito)
        if llm:
            refs += llm.get("referencias", [])[:2]
            mats += llm.get("materiais", [])[:2]
            if llm.get("protocolo_inviolavel"):
                instrucao = llm["protocolo_inviolavel"]

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

# ─── MAIN COM --llm ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Autopoiesis")
    parser.add_argument("--conceito", choices=["Memória", "Contingência", "Projeção"], default=None)
    parser.add_argument("--txt", action="store_true")
    parser.add_argument("--pdf", action="store_true")
    parser.add_argument("--llm", action="store_true", help="Ativar Ollama para expandir o manifesto")

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

if __name__ == "__main__":
    main()
