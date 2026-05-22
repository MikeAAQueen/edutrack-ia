import streamlit as st
import pandas as pd
from services.xano import fetch_professors, create_professor, delete_professor, update_professor

def show_professors():
    """
    Renders the Professors management screen.
    """
    st.title("👨‍🏫 Gerenciar Professores")
    
    token = st.session_state.get('user_token', 'mock_jwt_token_123')
    
    # Sidebar for adding new professor
    st.sidebar.header("➕ Adicionar Novo")
    with st.sidebar.form("add_professor_form"):
        new_name = st.text_input("Nome do Professor")
        new_email = st.text_input("Email (Opcional)")
        submit_btn = st.form_submit_button("Adicionar")
        
        if submit_btn:
            if not new_name:
                st.sidebar.warning("O nome do professor é obrigatório.")
            else:
                resp = create_professor(token, new_name, new_email)
                if resp["success"]:
                    st.sidebar.success("Professor adicionado com sucesso!")
                    st.rerun()
                else:
                    st.sidebar.error("Erro ao adicionar professor.")
    
    # Main area showing professors
    professors = fetch_professors(token)
    
    if not professors:
        st.info("Nenhum professor cadastrado. Comece adicionando um ao lado.")
    else:
        df_professors = pd.DataFrame(professors)
        
        # Display using an interactive dataframe
        st.data_editor(
            df_professors,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": None,
                "name": st.column_config.TextColumn("Nome", disabled=True),
                "email": st.column_config.TextColumn("Email", disabled=True)
            }
        )
        
        st.divider()
        st.subheader("GERENCIAR PROFESSORES")
        
        st.warning("⚠️ **Atenção**: Excluir um professor também excluirá permanentemente todas as suas **disciplinas e tarefas atreladas** (Deleção em Cascata).")
        
        selected_id = st.selectbox(
            "Selecione um professor:", 
            options=df_professors['id'], 
            format_func=lambda x: df_professors[df_professors['id'] == x]['name'].values[0],
            key="manage_professor_select"
        )
        
        selected_row = df_professors[df_professors["id"] == selected_id].iloc[0]

        @st.dialog(f"Editar: {selected_row['name']}")
        def edit_dialog():
            edit_name = st.text_input("Nome do Professor", value=selected_row["name"])
            edit_email = st.text_input("Email", value=selected_row["email"])
            
            st.divider()
            btn_col1, btn_col2 = st.columns(2)
            if btn_col1.button("OK ✔️", use_container_width=True, type="primary"):
                with st.spinner("Salvando..."):
                    resp = update_professor(token, selected_id, edit_name, edit_email)
                if resp["success"]:
                    st.success("Professor atualizado!")
                    st.rerun()
                else:
                    st.error(resp.get("error", "Erro ao salvar."))
            if btn_col2.button("Cancelar", use_container_width=True):
                st.rerun()

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("✏️ Editar", use_container_width=True):
                edit_dialog()
        with btn_col2:
            if st.button("🗑️ Excluir", use_container_width=True, type="primary"):
                with st.spinner("Excluindo..."):
                    resp = delete_professor(token, selected_id)
                    if resp["success"]:
                        st.success("Professor excluído com sucesso!")
                        st.rerun()
                    else:
                        st.error(resp["error"])
