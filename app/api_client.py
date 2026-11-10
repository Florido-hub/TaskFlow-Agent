import os
import requests

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("TASKFLOW_API_URL")


def listar_tarefas():
    response = requests.get(
        f"{BASE_URL}/tasks",
        timeout=15
    )

    response.raise_for_status()

    return response.json()