import streamlit as st
import time

def authenticate(email, password):
    """
    Mock authentication function for initial development.
    Replace with actual Xano API call later.
    """
    # Simulate API call latency
    time.sleep(1)
    
    # Mock credentials
    if email == "admin@edutrack.com" and password == "123456":
        return {
            "success": True,
            "token": "mock_jwt_token_123",
            "user": {
                "id": 1,
                "name": "Administrador",
                "email": email
            }
        }
    else:
        return {
            "success": False,
            "error": "Credenciais inválidas. Tente admin@edutrack.com / 123456"
        }

# Initial mock data for development
MOCK_SUBJECTS = [
    {"id": 1, "name": "Matemática", "professor": "Prof. Silva", "credits": 4},
    {"id": 2, "name": "Física", "professor": "Prof. Oliveira", "credits": 4},
    {"id": 3, "name": "Programação", "professor": "Prof. Souza", "credits": 6},
]

MOCK_TASKS = [
    {"id": 1, "subject_id": 1, "title": "Lista de Exercícios 1", "due_date": "2023-11-10", "completed": True},
    {"id": 2, "subject_id": 1, "title": "Prova N1", "due_date": "2023-11-20", "completed": False},
    {"id": 3, "subject_id": 3, "title": "Projeto MVP", "due_date": "2023-11-25", "completed": False},
    {"id": 4, "subject_id": 2, "title": "Relatório de Laboratório", "due_date": "2023-11-15", "completed": True},
]

@st.cache_data(ttl=60)
def fetch_subjects(token):
    """
    Mock fetching subjects from Xano.
    """
    time.sleep(0.5)
    return MOCK_SUBJECTS

@st.cache_data(ttl=60)
def fetch_tasks(token):
    """
    Mock fetching tasks from Xano.
    """
    time.sleep(0.5)
    return MOCK_TASKS

def create_subject(token, name, professor, credits):
    """
    Mock creating a subject.
    """
    new_id = len(MOCK_SUBJECTS) + 1
    new_subject = {
        "id": new_id,
        "name": name,
        "professor": professor,
        "credits": credits
    }
    MOCK_SUBJECTS.append(new_subject)
    # Clear cache to reflect new data
    fetch_subjects.clear()
    return {"success": True, "data": new_subject}

def update_task_status(token, task_id, completed):
    """
    Mock updating task status.
    """
    for task in MOCK_TASKS:
        if task["id"] == task_id:
            task["completed"] = completed
            # Clear cache
            fetch_tasks.clear()
            return {"success": True}
    return {"success": False, "error": "Task not found"}
