import streamlit as st
from components.auth import show_login
from components.dashboard import show_dashboard
from components.subjects import show_subjects
from components.tasks import show_tasks

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

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_token' not in st.session_state:
        st.session_state.user_token = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = 'Estudante'

    if not st.session_state.authenticated:
        show_login()
    else:
        # App Layout
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
        
        # Logout
        st.sidebar.divider()
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.rerun()

        # Render selected page
        pages[selection]()

if __name__ == "__main__":
    main()
