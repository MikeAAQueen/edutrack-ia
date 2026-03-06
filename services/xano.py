import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Carrega variáveis do .env (se existir)
load_dotenv()

# Pegamos a Base URL do Xano para as tabelas e para autenticação
XANO_API_URL = os.getenv(
    "XANO_API_URL", "https://x8ki-letl-twmt.n7.xano.io/api:QXhhKOtR"
).rstrip("/")
AUTH_API_URL = os.getenv("AUTH_API_URL", "").rstrip("/")


def authenticate(email, password):
    """
    Autentica o usuário pelo endpoint de login do Xano.
    """
    if not AUTH_API_URL:
        return {
            "success": False,
            "error": "A API de Autenticação não foi configurada no .env!",
        }

    url = f"{AUTH_API_URL}/auth/login"
    payload = {"email": email, "password": password}

    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            token = data.get("authToken", "")

            return {
                "success": True,
                "token": token,
                "user": {
                    "id": 0,
                    "name": email.split("@")[0].capitalize(),
                    "email": email,
                },
            }
        else:
            return {"success": False, "error": f"Credenciais inválidas: {resp.text}"}
    except Exception as e:
        return {"success": False, "error": f"Erro de conexão com a API: {str(e)}"}


@st.cache_data(ttl=60)
def fetch_subjects(token):
    url = f"{XANO_API_URL}/subjects"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 401:
            st.error("Sua sessão expirou. Faça login novamente.")
            return []
        else:
            st.error(f"Erro ao buscar disciplinas: {resp.text}")
            return []
    except Exception as e:
        st.error(f"Erro de conexão: {str(e)}")
        return []


@st.cache_data(ttl=60)
def fetch_tasks(token):
    url = f"{XANO_API_URL}/tasks"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 401:
            st.error("Sua sessão expirou. Faça login novamente.")
            return []
        else:
            st.error(f"Erro ao buscar tarefas: {resp.text}")
            return []
    except Exception as e:
        st.error(f"Erro de conexão: {str(e)}")
        return []


def create_subject(token, name, professor, credits):
    url = f"{XANO_API_URL}/subjects"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"name": name, "professor": professor, "credits": credits}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        if resp.status_code in (200, 201):
            fetch_subjects.clear()
            return {"success": True, "data": resp.json()}
        else:
            return {"success": False, "error": f"Falha na criação: {resp.text}"}
    except Exception as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}


def update_task_status(token, task_id, completed):
    url = f"{XANO_API_URL}/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"completed": completed}

    try:
        # Padrão de update do Xano muitas vezes é POST ou PATCH
        resp = requests.post(url, json=payload, headers=headers, timeout=10)

        if resp.status_code == 404:  # Tenta como PATCH se o POST não existir
            resp = requests.patch(url, json=payload, headers=headers, timeout=10)

        if resp.status_code in (200, 201):
            fetch_tasks.clear()
            return {"success": True}
        else:
            return {
                "success": False,
                "error": f"Erro ao atualizar: {resp.status_code} - {resp.text}",
            }
    except Exception as e:
        return {"success": False, "error": f"Erro de conexão: {str(e)}"}
