import os
from pathlib import Path
from uuid import uuid4

import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

from app.tools import (
    consultar_tarefas,
    criar_tarefa,
    atualizar_tarefa,
    iniciar_tarefa,
    concluir_tarefa,
)

BASE_DIR = Path(__file__).parent

load_dotenv(BASE_DIR / ".env")

TEMPERATURA = 0.1
TIMEOUT = 600

AI_PROVIDER = os.getenv("AI_PROVIDER")

def criar_modelo() -> ChatGoogleGenerativeAI | ChatOllama:
    """Inicializa o modelo local utilizado pelo agente.
    Configure o AI_PROVIDER no .env
    """

    if AI_PROVIDER == "google":
        api_key = os.getenv("GOOGLE_API_KEY")
        model_name = os.getenv("GEMINI_MODEL")

        if not api_key or not model_name:
            raise ValueError(
                "Configure GOOGLE_API_KEY e GEMINI_MODEL no .env."
            )

        return ChatGoogleGenerativeAI(
            model=model_name,
            api_key=api_key,
            temperature=TEMPERATURA,
            timeout=TIMEOUT,
            max_retries=2,
        )

    elif AI_PROVIDER == "ollama":
        from langchain_ollama import ChatOllama

        model_name = os.getenv("OLLAMA_MODEL")
        ollama_url = os.getenv("OLLAMA_URL")

        if not model_name or not ollama_url:
            raise ValueError(
                "Configure OLLAMA_MODEL e OLLAMA_URL no .env."
            )

        return ChatOllama(
            model=model_name,
            base_url=ollama_url,
            temperature=TEMPERATURA,
            timeout=TIMEOUT,
        )

    raise ValueError(f"Provider não suportado: {AI_PROVIDER}")


checkpointer = InMemorySaver()
model = criar_modelo()


def _carregar_system_prompt() -> str:
    """Carrega as instruções do agente a partir de prompt.txt."""

    caminho_prompt = BASE_DIR / "prompt.txt"

    if not caminho_prompt.exists():
        raise FileNotFoundError(
            f"Arquivo de prompt não encontrado: {caminho_prompt}"
        )

    return caminho_prompt.read_text(encoding="utf-8").strip()


def _criar_agent():
    """Cria o agente utilizando o metodo do Langchain"""

    ferramentas = [
        consultar_tarefas,
        criar_tarefa,
        atualizar_tarefa,
        iniciar_tarefa,
        concluir_tarefa,
    ]

    return create_agent(
        model=model,
        tools=ferramentas,
        system_prompt=_carregar_system_prompt(),
        checkpointer=checkpointer
    )

agent = _criar_agent()


def perguntar(pergunta: str, sessao: str) -> str:
    """Envia uma pergunta ao TaskFlow Agent e retorna a resposta."""

    try:
        if not pergunta.strip():
            raise ValueError("A pergunta não pode estar vazia.")

        config = {
            "configurable": {
                "thread_id": sessao
            }
        }

        resposta = agent.invoke(
            {
                "messages": [
                    {"role": "user", "content": pergunta.strip()}
                ]
            },
            config=config
        )

        mensagem_final = resposta["messages"][-1]

        return mensagem_final.content.strip()

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Não foi possível conectar ao Ollama. "
            "Verifique se ele está rodando (ollama serve) "
            f"e se o modelo foi baixado (ollama pull {os.getenv('OLLAMA_MODEL')})."
        )


def _modo_interativo() -> None:
    """Executa o chatbot no terminal."""

    sessao = str(uuid4())

    print(
        f"TaskFlow Agent — provedor: `{AI_PROVIDER}`"
    )
    print("Digite sua pergunta (ou 'sair' para encerrar).\n")

    while True:
        try:
            pergunta = input("Você: ").strip()

            if pergunta.lower() in {"sair", "exit", "quit"}:
                print("Até logo!")
                break

            if not pergunta:
                continue

            resposta = perguntar(pergunta, sessao)
            print(f"\nBot: {resposta}\n")

        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break

        except Exception as erro:
            print(f"\n[erro] {erro}\n")



if __name__ == "__main__":
    _modo_interativo()