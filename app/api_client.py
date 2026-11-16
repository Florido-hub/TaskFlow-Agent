import os
from datetime import date
from uuid import UUID

import requests

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("TASKFLOW_API_URL")

def create_new_task(
    titulo: str,
    descricao: str,
    prioridade: str,
    data_prevista: str
):
    try:
        date.fromisoformat(data_prevista)
    except ValueError:
        raise ValueError("A data deve estar no formato YYYY-MM-DD.")

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

    if not response.status_code == 201:
        raise Exception(
            f"Erro ao criar tarefa: {response.status_code} - {response.text}"
        )

    if response.text.strip():
        return response.json()

    return "Task criada com sucesso."

def update_task(
    task_id: str,
    titulo: str,
    descricao: str,
    prioridade: str,
    data_prevista: str
):
    try:
        UUID(task_id)
    except ValueError:
        raise ValueError("O ID informado não é um UUID válido.")

    try:
        date.fromisoformat(data_prevista)
    except ValueError:
        raise ValueError("A data deve estar no formato YYYY-MM-DD.")

    response = requests.patch(
        f"{BASE_URL}/tasks/{task_id}",
        json={
            "title": titulo,
            "description": descricao,
            "priority": prioridade,
            "dueDate": data_prevista
        },
        timeout=15
    )

    if not response.status_code == 204:
        raise Exception(
            f"Erro ao atualizar tarefa: {response.status_code} - {response.text}"
        )

    return "Tarefa atualizada com sucesso."


def start_task(task_id: str):
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

def complete_task(task_id: str):
    try:
        UUID(task_id)
    except ValueError:
        raise ValueError("O ID informado não é um UUID válido.")

    response = requests.patch(
        f"{BASE_URL}/tasks/{task_id}/complete",
        timeout=15
    )

    if not response.ok:
        raise Exception(
            f"Erro ao concluir tarefa: {response.status_code} - {response.text}"
        )

    if response.text.strip():
        return response.json()

    return "Tarefa concluída com sucesso."


def get_tasks():
    response = requests.get(
        f"{BASE_URL}/tasks",
        timeout=15
    )

    response.raise_for_status()

    return response.json()


def delete_task(task_id: str):
    try:
        UUID(task_id)
    except ValueError:
        raise ValueError("O ID informado não é um UUID válido.")

    response = requests.delete(
        f"{BASE_URL}/tasks/{task_id}",
        timeout=15
    )

    if not response.status_code == 204:
        raise Exception(
            f"Erro ao deletar tarefa: {response.status_code} - {response.text}"
        )

    return "Tarefa deletada com sucesso."