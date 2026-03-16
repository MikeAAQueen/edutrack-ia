import streamlit as st
import pandas as pd
import plotly.express as px
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

    # Visualizations
    if not df_tasks.empty and subjects:
        st.subheader("Análise Geral")
        
        # Merge task with subject name
        df_subjects = pd.DataFrame(subjects)
        df_subjects = df_subjects.rename(columns={'id': 'subject_id', 'name': 'subject_name'})
        df_merged = pd.merge(df_tasks, df_subjects, on='subject_id')
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("**Distribuição por Status**")
            # Pie chart for task status
            status_counts = df_tasks['completed'].map({True: 'Concluída', False: 'Pendente'}).value_counts().reset_index()
            status_counts.columns = ['Status', 'Quantidade']
            
            fig_pie = px.pie(
                status_counts, 
                values='Quantidade', 
                names='Status',
                color='Status',
                color_discrete_map={'Concluída': '#2ECC40', 'Pendente': '#FF851B'},
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_chart2:
            st.markdown("**Média de Notas por Disciplina**")
            
            # Ensure 'grade' column exists and is numeric
            if 'grade' in df_merged.columns:
                df_merged['grade'] = pd.to_numeric(df_merged['grade'], errors='coerce')
                
                # Filter out tasks without a grade yet
                graded_tasks = df_merged.dropna(subset=['grade'])
                
                if not graded_tasks.empty:
                    avg_grades = graded_tasks.groupby('subject_name')['grade'].mean().reset_index()
                    avg_grades = avg_grades.rename(columns={'subject_name': 'Disciplina', 'grade': 'Média'})
                    
                    fig_bar = px.bar(
                        avg_grades, 
                        x='Disciplina', 
                        y='Média',
                        color='Média',
                        color_continuous_scale='Viridis',
                        text_auto='.1f'
                    )
                    fig_bar.update_layout(yaxis_range=[0, 10]) # Assuming grades 0-10
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("Ainda não há tarefas avaliadas com notas.")
            else:
                 st.info("Ainda não há tarefas avaliadas com notas.")
            
        st.divider()
        st.markdown("**Volume de Tarefas por Disciplina**")
        
        # Count tasks per subject
        tasks_per_subject = df_merged.groupby('subject_name')['id'].count().reset_index()
        tasks_per_subject = tasks_per_subject.rename(columns={'id': 'Quantidade_Tarefas', 'subject_name': 'Disciplina'})
        
        fig_bar_count = px.bar(
            tasks_per_subject,
            x='Disciplina',
            y='Quantidade_Tarefas',
            color='Disciplina',
            text_auto=True
        )
        st.plotly_chart(fig_bar_count, use_container_width=True)
            
    else:
        st.info("Ainda não há tarefas ou disciplinas cadastradas para exibir no gráfico.")
