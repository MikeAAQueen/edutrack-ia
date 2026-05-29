import streamlit as st
import pandas as pd
from services.xano import (
    fetch_notes,
    create_note,
    update_note,
    delete_note,
    fetch_subjects,
)

def show_notes():
    st.title("🗒️ Anotações")
    token = st.session_state.get("user_token")

    subjects = fetch_subjects(token)
    df_subjects = pd.DataFrame(subjects) if subjects else pd.DataFrame(columns=["id", "name"])
    
    # Mapeamento para disciplinas + opção geral
    subj_map = {0: "Geral (Sem disciplina)"}
    for _, row in df_subjects.iterrows():
        subj_map[row["id"]] = row["name"]

    st.sidebar.header("➕ Nova Anotação")
    with st.sidebar.form("add_note_form"):
        new_title = st.text_input("Título")
        
        subject_options = list(subj_map.values())
        new_subject_name = st.selectbox("Disciplina Vinculada", options=subject_options)
        new_content = st.text_area("Conteúdo", height=150)
        
        submit_btn = st.form_submit_button("Salvar Anotação")
        
        if submit_btn:
            if not new_title:
                st.sidebar.warning("O título é obrigatório.")
            else:
                new_subj_id = list(subj_map.keys())[list(subj_map.values()).index(new_subject_name)]
                if new_subj_id == 0:
                    new_subj_id = None
                
                resp = create_note(token, new_subj_id, new_title, new_content)
                if resp["success"]:
                    st.sidebar.success("Anotação salva com sucesso!")
                    st.rerun()
                else:
                    st.sidebar.error("Erro ao salvar anotação.")

    # Listagem de anotações
    notes = fetch_notes(token)
    if not notes:
        st.info("Nenhuma anotação criada ainda.")
    else:
        for note in notes:
            note_id = note["id"]
            title = note["title"]
            content = note["content"]
            subj_id = note.get("subject_id")
            subj_name = subj_map.get(subj_id, "Geral")
            
            with st.expander(f"📌 {title} — *{subj_name}*"):
                st.write(content)
                
                # Ações
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("✏️ Editar", key=f"edit_{note_id}", use_container_width=True):
                        st.session_state[f"editing_note_{note_id}"] = True
                with col2:
                    if st.button("🗑️ Excluir", key=f"del_{note_id}", type="primary", use_container_width=True):
                        with st.spinner("Excluindo..."):
                            resp = delete_note(token, note_id)
                            if resp["success"]:
                                st.rerun()
                            else:
                                st.error("Erro ao apagar.")

                if st.session_state.get(f"editing_note_{note_id}", False):
                    st.markdown("---")
                    with st.form(f"edit_form_{note_id}"):
                        edit_title = st.text_input("Título", value=title)
                        
                        default_index = 0
                        if subj_id in subj_map:
                            default_index = list(subj_map.keys()).index(subj_id)
                            
                        edit_subj_name = st.selectbox("Disciplina", options=list(subj_map.values()), index=default_index)
                        edit_content = st.text_area("Conteúdo", value=content, height=150)
                        
                        save_col, cancel_col = st.columns(2)
                        if save_col.form_submit_button("Salvar Edição", type="primary", use_container_width=True):
                            edit_subj_id = list(subj_map.keys())[list(subj_map.values()).index(edit_subj_name)]
                            if edit_subj_id == 0:
                                edit_subj_id = None
                                
                            resp = update_note(token, note_id, edit_subj_id, edit_title, edit_content)
                            if resp["success"]:
                                st.session_state[f"editing_note_{note_id}"] = False
                                st.rerun()
                            else:
                                st.error("Erro ao atualizar anotação.")
                        if cancel_col.form_submit_button("Cancelar", use_container_width=True):
                            st.session_state[f"editing_note_{note_id}"] = False
                            st.rerun()
