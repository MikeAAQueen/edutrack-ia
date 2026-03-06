import streamlit as st
import pandas as pd
from services.xano import fetch_tasks, fetch_subjects, update_task_status
from utils.report import generate_pdf_report

def show_tasks():
    """
    Renders the Tasks management screen.
    """
    st.title("📝 Gerenciar Tarefas")
    
    token = st.session_state.get('user_token', 'mock_jwt_token_123')
    
    tasks = fetch_tasks(token)
    subjects = fetch_subjects(token)
    
    if not subjects:
        st.warning("Cadastre alguma disciplina primeiro.")
        return
        
    df_tasks = pd.DataFrame(tasks)
    df_subjects = pd.DataFrame(subjects)
    
    subject_map = dict(zip(df_subjects['id'], df_subjects['name']))
    
    # Filters
    st.subheader("Filtros")
    col1, col2 = st.columns(2)
    
    with col1:
        status_filter = st.multiselect(
            "Filtrar por Status",
            ["Pendentes", "Concluídas"],
            ["Pendentes", "Concluídas"]
        )
        
    with col2:
        subject_filter = st.multiselect(
            "Filtrar por Disciplina",
            options=subject_map.values(),
            default=list(subject_map.values())
        )
        
    st.divider()
    
    if df_tasks.empty:
        st.info("Nenhuma tarefa cadastrada.")
        return
        
    # Apply filters
    filtered_tasks = df_tasks.copy()
    
    if "Pendentes" not in status_filter:
        filtered_tasks = filtered_tasks[filtered_tasks['completed'] == True]
    if "Concluídas" not in status_filter:
        filtered_tasks = filtered_tasks[filtered_tasks['completed'] == False]
        
    # Map subject names for filtering
    filtered_tasks['subject_name'] = filtered_tasks['subject_id'].map(subject_map)
    filtered_tasks = filtered_tasks[filtered_tasks['subject_name'].isin(subject_filter)]
    
    if filtered_tasks.empty:
        st.info("Nenhuma tarefa corresponde aos filtros selecionados.")
        return
    
    # Display tasks
    for index, row in filtered_tasks.iterrows():
        col_task, col_check = st.columns([4, 1])
        
        with col_task:
            st.markdown(f"**{row['title']}** - 📅 {row['due_date']} (📚 {row['subject_name']})")
        
        with col_check:
            # Checkbox for task completion
            is_completed = st.checkbox("Concluída", value=row['completed'], key=f"check_{row['id']}")
            
            if is_completed != row['completed']:
                with st.spinner("Atualizando..."):
                    resp = update_task_status(token, row['id'], is_completed)
                    if resp["success"]:
                        st.rerun()
                    else:
                        st.error("Erro ao atualizar.")
    
    st.divider()
    
    # Report generation
    st.subheader("Relatórios")
    st.write("Baixe o relatório completo de suas tarefas.")
    
    if st.button("Gerar Relatório PDF"):
        pdf_bytes = generate_pdf_report(filtered_tasks, st.session_state.get('user_name', 'Estudante'))
        st.download_button(
            label="Baixar Arquivo PDF",
            data=pdf_bytes,
            file_name="relatorio_tarefas.pdf",
            mime="application/pdf"
        )
