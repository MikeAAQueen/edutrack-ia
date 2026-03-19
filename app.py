import streamlit as st
from components.auth import show_login
from components.dashboard import show_dashboard
from components.subjects import show_subjects
from components.tasks import show_tasks

# Configuração da página DEVE ser o primeiro comando Streamlit
st.set_page_config(
    page_title="EduTrack AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injetar CSS globalmente
st.markdown("""
<style>
    .auth-title { text-align: center; color: #4CAF50; }
    .auth-subtitle { text-align: center; }
    .center-bold { text-align: center; font-size: 1.1em; font-weight: bold; }
    .center-bold-pad { text-align: center; font-size: 1.1em; padding-top: 6px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Inicializa as variáveis de estado da sessão, se não existirem."""
    default_states = {
        'authenticated': False,
        'user_token': None,
        'user_name': 'Estudante'
    }
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value

def handle_logout():
    """Callback para realizar o logout limpando o estado da sessão."""
    st.session_state.clear()

def main():
    init_session_state()

    # Se não estiver autenticado, exibe o login e interrompe a execução do resto do app
    if not st.session_state.authenticated:
        show_login()
        st.stop()
    
    # App Layout (Apenas para usuários autenticados)
    st.sidebar.title("🎓 EduTrack AI")
    st.sidebar.markdown(f"**Bem-vindo, {st.session_state.get('user_name', 'Estudante')}!**")
    st.sidebar.divider()
    
    # Navigation
    pages = {
        "Dashboard": show_dashboard,
        "Disciplinas": show_subjects,
        "Tarefas": show_tasks
    }
    
    selection = st.sidebar.radio("Navegação", list(pages.keys()))
    
    # Logout usando callback (melhor prática para evitar re-runs imperativos)
    st.sidebar.divider()
    st.sidebar.button("Logout", on_click=handle_logout, use_container_width=True)

    # Render selected page
    pages[selection]()

if __name__ == "__main__":
    main()
