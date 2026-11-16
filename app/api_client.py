import os
from uuid import UUID

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


def iniciar_tarefa(task_id: str):
    try:
        UUID(task_id)
    except ValueError:
        raise ValueError("O ID informado não é um UUID válido.")

    response = requests.patch(
        f"{BASE_URL}/tasks/{task_id}/start",
        timeout=15
    )

    if not response.ok:
        raise Exception(
            f"Erro ao iniciar tarefa: {response.status_code} - {response.text}"
        )

    if response.text.strip():
        return response.json()

    return "Tarefa iniciada com sucesso."


def listar_tarefas():
    response = requests.get(
        f"{BASE_URL}/tasks",
        timeout=15
    )

    response.raise_for_status()

    return response.json()