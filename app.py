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

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

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
