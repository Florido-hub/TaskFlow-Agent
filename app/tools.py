import os

from dotenv import load_dotenv
from langchain.tools import tool

from app.api_client import listar_tarefas

load_dotenv()

BASE_URL = os.getenv("TASKFLOW_API_URL")


@tool
def somar(a: int, b: int) -> int:
    """ferramenta de teste que soma dois números inteiros."""
    return a + b

@tool
def consultar_tarefas() -> str:
    """
    Consulta as tarefas cadastradas no TaskFlow.
    Utilize quando o usuário perguntar sobre suas tarefas.
    """

    tarefas = listar_tarefas()

    return str(tarefas)