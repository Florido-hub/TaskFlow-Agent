import os
import requests

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("TASKFLOW_API_URL")

def criar_nova_tarefa(
    titulo: str,
    descricao: str,
    prioridade: str,
    data_prevista: str
):
    response = requests.post(
        f"{BASE_URL}/tasks",
        json={
            "title": titulo,
            "description": descricao,
            "priority": prioridade,
            "dueDate": data_prevista
        },
        timeout=15
    )

    if not response.ok:
        raise Exception(
            f"Erro ao criar tarefa: {response.status_code} - {response.text}"
        )

    return response




def listar_tarefas():
    response = requests.get(
        f"{BASE_URL}/tasks",
        timeout=15
    )

    response.raise_for_status()

    return response.json()