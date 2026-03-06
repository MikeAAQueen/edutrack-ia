import streamlit as st
import pandas as pd
from services.xano import fetch_subjects, fetch_tasks
from utils.progress import calculate_progress

def show_dashboard():
    """
    Renders the Dashboard screen.
    """
    st.title("📊 Dashboard")
    st.write("Bem-vindo ao seu painel de controle.")
    
    token = st.session_state.get('user_token', 'mock_jwt_token_123')
    
    subjects = fetch_subjects(token)
    tasks = fetch_tasks(token)
    
    # Calculate metrics
    total_subjects = len(subjects)
    df_tasks = pd.DataFrame(tasks)
    
    total_tasks = 0
    pending_tasks = 0
    
    if not df_tasks.empty:
        total_tasks = len(df_tasks)
        pending_tasks = len(df_tasks[df_tasks['completed'] == False])
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Disciplinas", total_subjects)
    with col2:
        st.metric("Tarefas Pendentes", pending_tasks)
    with col3:
        progress_percentage = calculate_progress(df_tasks)
        st.metric("Progresso Geral", f"{progress_percentage:.1f}%")

    st.divider()

    # Bar chart for tasks per subject
    if not df_tasks.empty and subjects:
        st.subheader("Tarefas por Disciplina")
        
        # Merge task with subject name
        df_subjects = pd.DataFrame(subjects)
        # Rename id to subject_id for merge
        df_subjects = df_subjects.rename(columns={'id': 'subject_id', 'name': 'subject_name'})
        
        df_merged = pd.merge(df_tasks, df_subjects, on='subject_id')
        
        # Count tasks per subject
        tasks_per_subject = df_merged.groupby('subject_name')['id'].count().reset_index()
        tasks_per_subject = tasks_per_subject.rename(columns={'id': 'Quantidade_Tarefas', 'subject_name': 'Disciplina'})
        
        # st.bar_chart expects index to be the x-axis
        tasks_per_subject = tasks_per_subject.set_index('Disciplina')
        st.bar_chart(tasks_per_subject)
    else:
        st.info("Ainda não há tarefas cadastradas para exibir no gráfico.")
