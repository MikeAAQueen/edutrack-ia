import streamlit as st
from services.xano import authenticate, register

def show_login():
    """
    Renders the login and registration screens.
    """
    st.markdown("<h1 class='auth-title'>EduTrack AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='auth-subtitle'>Assistente Educacional Personalizado</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab_login, tab_register = st.tabs(["Login", "Cadastro"])

        with tab_login:
            with st.form("login_form"):
                st.write("Faça login para acessar o sistema")
                email = st.text_input("E-mail", placeholder="seuemail@exemplo.com", key="login_email")
                password = st.text_input("Senha", type="password", placeholder="Sua senha", key="login_pass")
                
                submit = st.form_submit_button("Entrar")
                
                if submit:
                    if not email or not password:
                        st.warning("Preencha todos os campos do login.")
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

        with tab_register:
            with st.form("register_form"):
                st.write("Crie sua conta no EduTrack AI")
                reg_name = st.text_input("Nome completo", placeholder="Seu nome")
                reg_email = st.text_input("E-mail", placeholder="seuemail@exemplo.com", key="reg_email")
                reg_password = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres", key="reg_pass")
                reg_password_confirm = st.text_input("Confirmar Senha", type="password", placeholder="Repita a senha")
                
                submit_reg = st.form_submit_button("Cadastrar")
                
                if submit_reg:
                    if not reg_name or not reg_email or not reg_password or not reg_password_confirm:
                        st.warning("Preencha todos os campos do cadastro.")
                    elif reg_password != reg_password_confirm:
                        st.warning("As senhas informadas não coincidem.")
                    else:
                        with st.spinner("Criando conta e autenticando..."):
                            response = register(reg_name, reg_email, reg_password)
                            if response["success"]:
                                st.session_state.authenticated = True
                                st.session_state.user_token = response["token"]
                                st.session_state.user_name = response["user"]["name"]
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(response["error"])
