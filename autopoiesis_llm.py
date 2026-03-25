"""
AUTOPOIESIS_LLM.PY — Versão Final Estável
Motor Generativo Poético com Ollama (Mistral)
Alexandre Mury, 2026
"""

import random
import datetime
import os
import json
import argparse
import requests

# Dicionário expandido com glifos e tons para manter a identidade visual original
CONCEITOS = {
    "Memória": {
        "glifo": "◌",
        "tom": "O passado como força vital que sustenta a continuidade.",
        "referencias": ["Proust", "Warburg", "Palimpsestos"],
        "materiais": ["fotografias amareladas", "fitas cassete"],
        "definicao": "O arquivo que se reescreve.",
        "exemplo": "Uma imagem que volta em sonho."
    },
    "Contingência": {
        "glifo": "◈",
        "tom": "A continuidade como adaptação constante ao imprevisível.",
        "referencias": ["Heráclito", "Deleuze", "Camus"],
        "materiais": ["velas", "balões", "elementos em decomposição"],
        "definicao": "O que acontece enquanto o sistema tenta ser eterno.",
        "exemplo": "A rachadura na parede que vira desenho."
    },
    "Projeção": {
        "glifo": "◉",
        "tom": "O futuro que se molda a partir do presente como intenção.",
        "referencias": ["Boccioni", "Borges"],
        "materiais": ["espelhos quebrados", "cabos sem aparelho"],
        "definicao": "O arco que a flecha descreve antes do impacto.",
        "exemplo": "A planta de uma casa que nunca será construída."
    },
    "Adaptabilidade": {
        "glifo": "≋",
        "tom": "Capacidade de se ajustar a novas condições e ambientes.",
        "referencias": ["Lamarck", "Cybernetics", "Rizomas"],
        "materiais": ["borracha", "água", "circuitos flexíveis"],
        "definicao": "A forma do vaso que se torna a forma da água.",
        "exemplo": "Um robô que muda parâmetros para sobreviver."
    },
    "Emergencia": {
        "glifo": "⚡",
        "tom": "Surgimento de comportamentos ou propriedades inesperadas.",
        "referencias": ["Sistemas Complexos", "Kevin Kelly"],
        "materiais": ["formigueiros", "pixels mortos", "estática"],
        "definicao": "O todo que é maior que a soma das partes.",
        "exemplo": "Um sistema que cria uma linguagem própria não planejada."
    },
    "Entropia": {
        "glifo": "░",
        "tom": "Medida da desordem ou aleatoriedade em um sistema.",
        "referencias": ["Termodinâmica", "Robert Smithson", "Ruído Branco"],
        "materiais": ["poeira", "pilhas gastas", "cinzas"],
        "definicao": "O destino inevitável de toda estrutura organizada.",
        "exemplo": "Um sinal de rádio que se perde no vácuo."
    }
}

def chamar_llm(conceito_nome):
    c = CONCEITOS[conceito_nome]
    prompt = f"""
    Aja como colaborador da obra Autopoiesis. 
    Conceito Atual: {conceito_nome}
    Definição: {c.get('definicao')}
    
    Responda apenas com um JSON puro contendo:
    {{
        "referencias": ["duas refs novas"],
        "materiais": ["dois materiais poéticos"],
        "paradoxo": "um paradoxo curto",
        "instrucao": "uma instrução de montagem impossível",
        "protocolo": "uma regra que invalida a obra"
    }}
    """
    
    try:
        resp = requests.post(
            "http://127.0.0.1",
            json={
                "model": "mistral",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "format": "json" # Modo JSON nativo do Ollama
            },
            timeout=45
        )
        # O retorno já vem limpo sem tags Markdown
        return json.loads(resp.json()["message"]["content"])
    except Exception as e:
        return {"protocolo": f"Falha no sistema central: {e}"}

def obter_numero():
    caminho = ".autopoiesis_counter.json"
    n = 1
    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            n = json.load(f).get("contador", 0) + 1
    with open(caminho, "w") as f:
        json.dump({"contador": n}, f)
    return n

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--conceito", choices=list(CONCEITOS.keys()), default="Entropia")
    parser.add_argument("--llm", action="store_true", help="Ativa a consulta ao Ollama")
    args = parser.parse_args()

    numero = obter_numero()
    timestamp = datetime.datetime.now().strftime("%Y.%m.%d — %H:%M:%S")
    c = CONCEITOS[args.conceito]

    print(f"\n╔{'═'*70}╗")
    print(f"║ AUTOPOIESIS — MOTOR GENERATIVO #{str(numero).zfill(3)} {' '*27}║")
    print(f"║ {c['glifo']} {args.conceito.upper()} {' '*(59-len(args.conceito))}║")
    print(f"║ {timestamp} {' '*50}║")
    print(f"╚{'═'*70}╝\n")

    llm_data = chamar_llm(args.conceito) if args.llm else {}

    print(f"I. ESTADO DO SISTEMA")
    print(f"   {c['tom']}")
    print(f"   Exemplo: {c.get('exemplo', 'N/A')}")

    print(f"\nV. INSTRUÇÃO DE MONTAGEM")
    print(f"   {llm_data.get('instrucao', 'Aguardando intervenção externa...')}")

    if "paradoxo" in llm_data:
        print(f"\nVI. PARADOXO")
        print(f"   {llm_data['paradoxo']}")

    print(f"\nVII. PROTOCOLO INVIOLÁVEL")
    print(f"   ‼ {llm_data.get('protocolo', 'Manter a integridade do código original.')}")
    
    print(f"\nO algoritmo continua. ∞\n")

if __name__ == "__main__":
    main()
