""""
AUTOPOIESIS_LLM.PY — Versão com Ollama (100% grátis)
Alexandre Mury, 2026
"""

import random
import datetime
import os
import json
import argparse
import requests

CONCEITOS = {
    "Memória": {
        "glifo": "◌",
        "tom": "O passado como força vital que sustenta a continuidade.",
        "referencias": ["Proust e a madeleine", "Warburg — Atlas Mnemosyne", "Palimpsestos medievais"],
        "materiais": ["fotografias amareladas", "fitas cassete emaranhadas", "cartas nunca enviadas"],
        "verbos": ["enrolar o tempo como fita de Möbius", "sobrepor camadas de ausência"]
    },
    "Contingência": {
        "glifo": "◈",
        "tom": "A continuidade como adaptação constante ao imprevisível.",
        "referencias": ["Heráclito — o rio", "Deleuze — plano de imanência", "Camus — o absurdo"],
        "materiais": ["velas com tempo indeterminado", "balões em esvaziamento", "elementos em decomposição"],
        "verbos": ["construir com o que recusa permanência", "registrar o colapso"]
    },
    "Projeção": {
        "glifo": "◉",
        "tom": "O futuro que se molda a partir do presente como intenção.",
        "referencias": ["Boccioni — Formas únicas de continuidade", "Borges — caminhos que se bifurcam"],
        "materiais": ["espelhos quebrados", "neon apagado", "cabos sem aparelho"],
        "verbos": ["projetar o que ainda não existe", "iluminar o invisível"]
    }
}

def chamar_llm(conceito):
    prompt = f"""Você é colaborador poético da obra Autopoiesis de Alexandre Mury.
Conceito: {conceito}

Responda APENAS com JSON válido:

{{
  "referencias": ["ref1", "ref2"],
  "materiais": ["material poético 1", "material poético 2"],
  "paradoxo": "descrição curta do paradoxo",
  "instrucao": "instrução de montagem com impossibilidade",
  "protocolo": "instrução que torna a execução impossível"
}}"""

    try:
        resp = requests.post(
            "http://127.0.0.1:11434/api/chat",
            json={
                "model": "mistral",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            },
            timeout=90
        )
        texto = resp.json()["message"]["content"].strip()
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0].strip()
        elif "```" in texto:
            texto = texto.split("```")[1].split("```")[0].strip()
        return json.loads(texto)
    except Exception as e:
        print(f"❌ Ollama não respondeu: {e}")
        return {}

def obter_numero():
    caminho = ".autopoiesis_counter.json"
    if os.path.exists(caminho):
        with open(caminho) as f:
            n = json.load(f).get("contador", 0) + 1
    else:
        n = 1
    with open(caminho, "w") as f:
        json.dump({"contador": n}, f)
    return n

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--conceito", choices=["Memória", "Contingência", "Projeção"], default="Contingência")
    parser.add_argument("--llm", action="store_true")
    args = parser.parse_args()

    conceito = args.conceito
    numero = obter_numero()
    timestamp = datetime.datetime.now().strftime("%Y.%m.%d — %H:%M:%S")

    print(f"\n╔{'═'*70}╗")
    print(f"║ AUTOPOIESIS — MOTOR GENERATIVO #{str(numero).zfill(3)} {' '*27}║")
    print(f"║ {CONCEITOS[conceito]['glifo']} {conceito.upper()} {' '*59}║")
    print(f"║ {timestamp} {' '*50}║")
    print(f"╚{'═'*70}╝\n")

    if args.llm:
        print("🔄 Chamando Ollama (mistral)...\n")
        llm_data = chamar_llm(conceito)
    else:
        llm_data = {}

    refs = CONCEITOS[conceito]["referencias"] + llm_data.get("referencias", [])
    mats = CONCEITOS[conceito]["materiais"] + llm_data.get("materiais", [])
    protocolo = llm_data.get("protocolo", "A obra deve conter ao menos uma instrução que torna sua própria execução impossível.")

    print(f"I. CONCEITO\n   {CONCEITOS[conceito]['tom']}")
    print(f"\nV. INSTRUÇÃO DE MONTAGEM")
    print("   " + (llm_data.get("instrucao") or "Justaposição gerada pelo sistema..."))
    print(f"\nVII. PROTOCOLO INVIOLÁVEL")
    print(f"   ‼ {protocolo}")
    print(f"\nO algoritmo continua. ∞\n")

if __name__ == "__main__":
    main()
