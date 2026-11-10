import requests
from langchain.agents import create_agent
from app.tools import consultar_tarefas, somar
from langchain_ollama import ChatOllama

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
caminho_env = Path(__file__).resolve().parent / ".env"
load_dotenv(caminho_env)

TEMPERATURA = 0.1
TIMEOUT = 600

# Modelo
model = ChatOllama(
    model=os.getenv("OLLAMA_MODEL"),
    base_url=os.getenv("OLLAMA_URL"),
    temperature=TEMPERATURA,
    timeout=TIMEOUT
)


def _carregar_system_prompt() -> str:
    """Carrega as instruções do agente a partir de prompt.txt."""

    caminho_prompt = BASE_DIR / "prompt.txt"

    return caminho_prompt.read_text(encoding="utf-8").strip()


def _criar_agent():
    return create_agent(
        model=model,
        tools=[consultar_tarefas],
        system_prompt=_carregar_system_prompt()
    )

agent = _criar_agent()


def perguntar(pergunta: str) -> str:
    """Envia uma pergunta ao TaskFlow Agent e retorna a resposta."""

    try:
        resposta = agent.invoke({
            "messages": [
                {"role": "user", "content": pergunta}
            ]
        })

        return resposta["messages"][-1].content.strip()

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Não foi possível conectar ao Ollama. "
            "Verifique se ele está rodando (ollama serve) "
            f"e se o modelo foi baixado (ollama pull {os.getenv('OLLAMA_MODEL')})."
        )


def _modo_interativo() -> None:
    """Executa o chatbot no terminal."""

    print(
        f"TaskFlow Agent — provedor: Ollama | "
        f"modelo: {os.getenv('OLLAMA_MODEL')}"
    )
    print("Digite sua pergunta (ou 'sair' para encerrar).\n")

    while True:
        try:
            pergunta = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break
        if not pergunta:
            continue
        if pergunta.lower() in {"sair", "exit", "quit"}:
            print("Até logo!")
            break
        try:
            print(f"\nBot: {perguntar(pergunta)}\n")
        except Exception as erro:
            print(f"\n[erro] {erro}\n")


if __name__ == "__main__":
    _modo_interativo()