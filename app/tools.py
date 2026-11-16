from langchain.tools import tool

from app.api_client import create_new_task, get_tasks, update_task, complete_task, start_task, delete_task

@tool
def consultar_tarefas() -> str:
    """
    Consulta as tarefas cadastradas no TaskFlow.
    Utilize quando o usuário perguntar sobre as suas tarefas.
    """

    tarefas = get_tasks()

    return str(tarefas)


@tool
def iniciar_tarefa(task_id : str) -> str:
    """
    Inicia uma tarefa existente no TaskFlow.

    Recebe o UUID da tarefa que deve ser iniciada.
    Utilize quando o usuário solicitar o início de uma tarefa.
    """

    tarefa = start_task(task_id)

    return (str(tarefa))

@tool
def concluir_tarefa(task_id : str) -> str:
    """
    Concluir uma tarefa existente no TaskFlow.

    Recebe o UUID da tarefa que deve ser completada.
    Utilize quando o usuário solicitar a conclusão de uma tarefa.
    """

    tarefa = complete_task(task_id)

    return str(tarefa)


@tool
def criar_tarefa(
    titulo: str,
    descricao: str,
    prioridade: str,
    data_prevista: str
) -> str:
    """
    Cria uma tarefa no TaskFlow.

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

    tarefa = create_new_task(
        titulo,
        descricao,
        prioridade,
        data_prevista
    )

    return str(tarefa)

@tool
def atualizar_tarefa(
        task_id: str,
        titulo: str,
        descricao: str,
        prioridade: str,
        data_prevista: str
) -> str:
    """
    atualiza uma tarefa no TaskFlow.

    Utilize quando o usuário solicitar a atualização de uma tarefa.

    Interprete as informações fornecidas pelo usuário e extraia:
    - Título da tarefa.
    - Descrição.
    - Prioridade: HIGH, MEDIUM ou LOW.
    - Data prevista no formato ISO 8601 (YYYY-MM-DD).

    A data pode ser informada em linguagem natural ou em diferentes
    formatos. Converta-a para YYYY-MM-DD antes de chamar a ferramenta.

    Se alguma informação obrigatória estiver ausente ou ambígua,
    não execute a atualização. Solicite os dados faltantes ao usuário.
     """

    tarefa = update_task(
        task_id,
        titulo,
        descricao,
        prioridade,
        data_prevista
    )

    return str(tarefa)

@tool
def deletar_tarefa(task_id : str) -> str:
    """
    Exclui uma tarefa existente no TaskFlow.

    Recebe o UUID da tarefa que deve ser excluída.

    Antes de utilizar esta ferramenta:
    - Consulte as tarefas para identificar o registro correto.
    - Solicite confirmação explícita do usuário.
    - Não invente ou suponha UUIDs.

    Utilize somente após a confirmação do usuário.
    """
    tarefa = delete_task(task_id)

    return str(tarefa)