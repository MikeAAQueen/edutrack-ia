import streamlit as st
import pandas as pd
from services.xano import fetch_subjects, create_subject

def show_subjects():
    """
    Renders the Subjects management screen.
    """
    st.title("📚 Gerenciar Disciplinas")
    
    token = st.session_state.get('user_token', 'mock_jwt_token_123')
    
    # Sidebar for adding new subject
    st.sidebar.header("➕ Adicionar Nova")
    with st.sidebar.form("add_subject_form"):
        new_name = st.text_input("Nome da Disciplina")
        new_professor = st.text_input("Professor(a)")
        new_credits = st.number_input("Créditos", min_value=1, max_value=20, value=4)
        submit_btn = st.form_submit_button("Adicionar")
        
        if submit_btn:
            if not new_name or not new_professor:
                st.sidebar.warning("Preencha todos os campos obrigatórios.")
            else:
                resp = create_subject(token, new_name, new_professor, new_credits)
                if resp["success"]:
                    st.sidebar.success("Disciplina adicionada com sucesso!")
                    st.rerun()
                else:
                    st.sidebar.error("Erro ao adicionar disciplina.")
    
    # Main area showing subjects
    subjects = fetch_subjects(token)
    
    if not subjects:
        st.info("Nenhuma disciplina cadastrada.")
    else:
        df_subjects = pd.DataFrame(subjects)
        
        # Display using an interactive dataframe
        st.data_editor(
            df_subjects,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", disabled=True),
                "name": st.column_config.TextColumn("Nome"),
                "professor": st.column_config.TextColumn("Professor(a)"),
                "credits": st.column_config.NumberColumn("Créditos", format="%d")
            }
        )
        
        st.divider()
        st.subheader("Excluir Disciplina")
        st.warning("Atenção: Excluir uma disciplina também excluirá todas as tarefas vinculadas a ela.")
        
        col_del1, col_del2 = st.columns([3, 1])
        with col_del1:
            subject_to_delete = st.selectbox(
                "Selecione a disciplina para excluir:", 
                options=df_subjects['id'], 
                format_func=lambda x: df_subjects[df_subjects['id'] == x]['name'].values[0]
            )
        with col_del2:
            st.write("") # Spacing
            st.write("")
            if st.button("🗑️ Excluir", use_container_width=True, type="primary"):
                with st.spinner("Excluindo..."):
                    from services.xano import delete_subject
                    resp = delete_subject(token, subject_to_delete)
                    if resp["success"]:
                        st.success("Disciplina excluída com sucesso!")
                        st.rerun()
                    else:
                        st.error(resp["error"])
