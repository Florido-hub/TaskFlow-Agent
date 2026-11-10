from langchain.tools import tool

from app.api_client import *

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


@tool
def criar_tarefa(
    titulo: str,
    descricao: str,
    prioridade: str,
    data_prevista: str
) -> str:
    """
    Cria uma nova tarefa no TaskFlow.

    Utilize quando o usuário solicitar a criação de uma tarefa.

    Interprete as informações fornecidas pelo usuário e extraia:
    - Título da tarefa.
    - Descrição.
    - Prioridade: HIGH, MEDIUM ou LOW.
    - Data prevista no formato ISO 8601 (YYYY-MM-DD).

    A data pode ser informada em linguagem natural ou em diferentes
    formatos. Converta-a para YYYY-MM-DD antes de chamar a ferramenta.

    Se alguma informação obrigatória estiver ausente ou ambígua,
    não execute a criação. Solicite os dados faltantes ao usuário.
    """

    tarefa = criar_nova_tarefa(
        titulo,
        descricao,
        prioridade,
        data_prevista
    )

    return str(tarefa)