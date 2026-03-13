import streamlit as st
import requests
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Custom Exception for Rate Limiting
class RateLimitException(Exception):
    pass

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


def register(name, email, password):
    """
    Cadastra o usuário pelo endpoint de signup do Xano.
    """
    if not AUTH_API_URL:
        return {
            "success": False,
            "error": "A API de Autenticação não foi configurada no .env!",
        }

    url = f"{AUTH_API_URL}/auth/signup"
    payload = {"name": name, "email": email, "password": password}

    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code in (200, 201):
            data = resp.json()
            token = data.get("authToken", "")

            return {
                "success": True,
                "token": token,
                "user": {
                    "id": 0,
                    "name": name,
                    "email": email,
                },
            }
        else:
             return {"success": False, "error": f"Erro no cadastro: {resp.text}"}
    except Exception as e:
        return {"success": False, "error": f"Erro de conexão com a API: {str(e)}"}


# Retry strategy: wait 2^x * 1 second between each retry, up to 10 seconds, max 4 attempts.
# Retries on network errors (requests.exceptions.RequestException) or RateLimitException
def get_retry_decorator():
    return retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=(retry_if_exception_type(requests.exceptions.RequestException) | retry_if_exception_type(RateLimitException)),
        reraise=True
    )

@st.cache_data(ttl=60)
def fetch_subjects(token):
    # Wrapper function to apply the retry internally without breaking st.cache_data signature parsing too much
    @get_retry_decorator()
    def _do_fetch():
        url = f"{XANO_API_URL}/disciplinas"
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 429:
            raise RateLimitException("Too Many Requests")
            
        resp.raise_for_status() # raises HTTPError for bad responses (4xx or 5xx) if not handled
        return resp

    try:
        resp = _do_fetch()
        if resp.status_code == 200:
            data = resp.json()
            # Mapeia as colunas em português para as chaves em inglês que o app usa
            return [{"id": d["id"], "name": d.get("nome", ""), "professor": d.get("professor", ""), "credits": d.get("creditos", 0), "workload": d.get("carga_horaria", 0), "absences": d.get("faltas", 0)} for d in data]
        else:
            return []
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.error("Sua sessão expirou. Faça login novamente.")
        else:
            st.error(f"Erro ao buscar disciplinas: {e.response.text}")
        return []
    except Exception as e:
        st.error(f"Erro de conexão (Disciplinas): Houve instabilidade (Rate Limit ou Rede). Tente novamente em instantes.")
        return []


@st.cache_data(ttl=60)
def fetch_tasks(token):
    @get_retry_decorator()
    def _do_fetch():
        url = f"{XANO_API_URL}/tarefas"
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 429:
            raise RateLimitException("Too Many Requests")
        resp.raise_for_status()
        return resp

    try:
        resp = _do_fetch()
        if resp.status_code == 200:
            data = resp.json()
            # Mapeia as colunas do Xano para as chaves que o app usa
            # id, disciplinas_id, titulo, data_entrega, completado, nota -> id, subject_id, title, due_date, completed, grade
            return [{"id": t["id"], "subject_id": t.get("disciplinas_id"), "title": t.get("titulo", ""), "due_date": t.get("data_entrega", ""), "completed": t.get("completado", False), "grade": t.get("nota")} for t in data]
        else:
            return []
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.error("Sua sessão expirou. Faça login novamente.")
        else:
            st.error(f"Erro ao buscar tarefas: {e.response.text}")
        return []
    except Exception as e:
        st.error(f"Erro de conexão (Tarefas): Houve instabilidade (Rate Limit ou Rede). Tente novamente em instantes.")
        return []


@get_retry_decorator()
def _do_create_subject(url, headers, payload):
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    if resp.status_code == 429:
        raise RateLimitException("Too Many Requests")
    return resp

def create_subject(token, name, professor, credits, workload):
    url = f"{XANO_API_URL}/disciplinas"
    headers = {"Authorization": f"Bearer {token}"}
    # Envia os dados em português para o Xano
    payload = {"nome": name, "professor": professor, "creditos": credits, "carga_horaria": workload, "faltas": 0}
    try:
        resp = _do_create_subject(url, headers, payload)
        if resp.status_code in (200, 201):
            fetch_subjects.clear()
            return {"success": True, "data": resp.json()}
        else:
            return {"success": False, "error": f"Falha na criação: {resp.text}"}
    except Exception as e:
        return {"success": False, "error": f"Erro de conexão/Limite de taxa excedido."}

@get_retry_decorator()
def _do_update_subject(url, headers, payload):
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    if resp.status_code == 404:  # Tenta como PATCH se o POST não existir ou for diferente
        resp = requests.patch(url, json=payload, headers=headers, timeout=10)
    if resp.status_code == 429:
        raise RateLimitException("Too Many Requests")
    return resp

def update_subject_absences(token, subject_id, absences):
    url = f"{XANO_API_URL}/disciplinas/{subject_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"faltas": absences}

    try:
        resp = _do_update_subject(url, headers, payload)

        if resp.status_code in (200, 201):
            fetch_subjects.clear()
            return {"success": True}
        else:
            return {
                "success": False,
                "error": f"Erro ao atualizar: {resp.status_code} - {resp.text}",
            }
    except Exception as e:
        return {"success": False, "error": f"Erro de conexão/Limite de taxa excedido."}

def update_subject(token, subject_id, name, professor, credits, workload):
    """Atualiza todos os campos editáveis de uma disciplina."""
    url = f"{XANO_API_URL}/disciplinas/{subject_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "nome": name,
        "professor": professor,
        "creditos": credits,
        "carga_horaria": workload,
    }
    try:
        resp = _do_update_subject(url, headers, payload)
        if resp.status_code in (200, 201):
            fetch_subjects.clear()
            return {"success": True}
        else:
            return {"success": False, "error": f"Erro ao atualizar: {resp.status_code} - {resp.text}"}
    except Exception as e:
        return {"success": False, "error": f"Erro de conexão/Limite de taxa excedido."}

@get_retry_decorator()
def _do_update_task(url, headers, payload):
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    if resp.status_code == 404:  # Tenta como PATCH se o POST não existir ou for diferente
        resp = requests.patch(url, json=payload, headers=headers, timeout=10)
    if resp.status_code == 429:
        raise RateLimitException("Too Many Requests")
    return resp

def update_task_status(token, task_id, completed, grade=None):
    url = f"{XANO_API_URL}/tarefas/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"completado": completed}
    if grade is not None:
        payload["nota"] = grade

    try:
        resp = _do_update_task(url, headers, payload)

        if resp.status_code in (200, 201):
            fetch_tasks.clear()
            return {"success": True}
        else:
            return {
                "success": False,
                "error": f"Erro ao atualizar: {resp.status_code} - {resp.text}",
            }
    except Exception as e:
        return {"success": False, "error": f"Erro de conexão/Limite de taxa excedido."}

@get_retry_decorator()
def _do_delete(url, headers):
    resp = requests.delete(url, headers=headers, timeout=10)
    if resp.status_code == 429:
        raise RateLimitException("Too Many Requests")
    return resp

def delete_subject(token, subject_id):
    url = f"{XANO_API_URL}/disciplinas/{subject_id}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = _do_delete(url, headers)
        if resp.status_code in (200, 204):
            fetch_subjects.clear()
            # Precisamos limpar as tasks tbm p/ evitar inconsistências
            fetch_tasks.clear()
            return {"success": True}
        else:
            return {"success": False, "error": f"Falha ao apagar: {resp.text}"}
    except Exception as e:
        return {"success": False, "error": f"Erro de conexão/Limite de taxa excedido."}

@get_retry_decorator()
def _do_create_task(url, headers, payload):
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    if resp.status_code == 429:
        raise RateLimitException("Too Many Requests")
    return resp
    
def create_task(token, subject_id, title, due_date):
    url = f"{XANO_API_URL}/tarefas"
    headers = {"Authorization": f"Bearer {token}"}
    
    # Send Portuguese to Xano API
    payload = {
        "disciplinas_id": subject_id,
        "titulo": title,
        "data_entrega": due_date,
        "completado": False
    }
    
    try:
        resp = _do_create_task(url, headers, payload)
        if resp.status_code in (200, 201):
            fetch_tasks.clear()
            return {"success": True, "data": resp.json()}
        else:
            return {"success": False, "error": f"Falha na criação: {resp.text}"}
    except Exception as e:
        return {"success": False, "error": f"Erro de conexão/Limite de taxa excedido."}

def delete_task(token, task_id):
    url = f"{XANO_API_URL}/tarefas/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = _do_delete(url, headers)
        if resp.status_code in (200, 204):
            fetch_tasks.clear()
            return {"success": True}
        else:
            return {"success": False, "error": f"Falha ao apagar: {resp.text}"}
    except Exception as e:
        return {"success": False, "error": f"Erro de conexão/Limite de taxa excedido."}
