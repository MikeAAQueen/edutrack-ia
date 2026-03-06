import streamlit as st
from services.xano import authenticate

def show_login():
    """
    Renders the login screen.
    """
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>EduTrack AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Assistente Educacional Personalizado</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.write("Faça login para acessar o sistema")
            email = st.text_input("E-mail", placeholder="admin@edutrack.com")
            password = st.text_input("Senha", type="password", placeholder="123456")
            
            submit = st.form_submit_button("Entrar")
            
            if submit:
                if not email or not password:
                    st.warning("Preencha todos os campos.")
                else:
                    with st.spinner("Autenticando..."):
                        response = authenticate(email, password)
                        if response["success"]:
                            st.session_state.authenticated = True
                            st.session_state.user_token = response["token"]
                            st.session_state.user_name = response["user"]["name"]
                            st.rerun()
                        else:
                            st.error(response["error"])
