import streamlit as st
from components.auth import show_login
from components.dashboard import show_dashboard
from components.professors import show_professors
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
    
    # Configurando as páginas
    dashboard_page = st.Page(show_dashboard, title="Dashboard", icon="📊")
    professors_page = st.Page(show_professors, title="Professores", icon="👨‍🏫")
    subjects_page = st.Page(show_subjects, title="Disciplinas", icon="📚")
    tasks_page = st.Page(show_tasks, title="Tarefas", icon="📝")
    
    # Roteador nativo oculto (para podermos desenhar a sidebar na ordem que quisermos)
    pg = st.navigation(
        [dashboard_page, professors_page, subjects_page, tasks_page],
        position="hidden"
    )
    
    # Renderizando a Sidebar na ordem correta
    st.sidebar.title("🎓 EduTrack AI")
    st.sidebar.markdown(f"**Bem-vindo, {st.session_state.get('user_name', 'Estudante')}!**")
    st.sidebar.divider()
    
    st.sidebar.caption("Navegação")
    st.sidebar.page_link(dashboard_page)
    st.sidebar.page_link(professors_page)
    st.sidebar.page_link(subjects_page)
    st.sidebar.page_link(tasks_page)
    
    # Logout usando callback (melhor prática para evitar re-runs imperativos)
    st.sidebar.divider()
    st.sidebar.button("Logout", on_click=handle_logout, use_container_width=True)

    # Render selected page
    pg.run()

if __name__ == "__main__":
    main()
