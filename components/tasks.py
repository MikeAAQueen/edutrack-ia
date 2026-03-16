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
    
    # Sidebar for adding new task
    st.sidebar.header("➕ Nova Tarefa")
    
    tasks = fetch_tasks(token)
    subjects = fetch_subjects(token)
    
    if not subjects:
        st.warning("Cadastre alguma disciplina primeiro.")
        return
        
    df_tasks = pd.DataFrame(tasks)
    df_subjects = pd.DataFrame(subjects)
    
    subject_map = dict(zip(df_subjects['id'], df_subjects['name']))
    
    with st.sidebar.form("add_task_form"):
        new_title = st.text_input("Título da Tarefa")
        new_subject_name = st.selectbox("Disciplina", options=list(subject_map.values()))
        new_due_date = st.date_input("Data de Entrega")
        
        submit_btn = st.form_submit_button("Adicionar Tarefa")
        
        if submit_btn:
            if not new_title:
                st.sidebar.warning("Preencha o título da tarefa.")
            else:
                from services.xano import create_task
                
                # Find subject ID from name
                new_subject_id = list(subject_map.keys())[list(subject_map.values()).index(new_subject_name)]
                
                # Format date to string YYYY-MM-DD
                formatted_date = new_due_date.strftime("%Y-%m-%d")
                
                resp = create_task(token, new_subject_id, new_title, formatted_date)
                if resp["success"]:
                    st.sidebar.success("Tarefa adicionada!")
                    st.rerun()
                else:
                    st.sidebar.error("Erro ao adicionar tarefa.")
    
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
        
    def on_task_change(task_id, check_key, grade_key):
        is_completed = st.session_state.get(check_key, False)
        grade_val = st.session_state.get(grade_key, 0.0)
        grade_payload = grade_val if grade_val > 0 else None
        
        if is_completed:
            st.balloons()
            
        update_task_status(st.session_state.get('user_token'), task_id, is_completed, grade_payload)
        
    # Map subject names for filtering
    filtered_tasks['subject_name'] = filtered_tasks['subject_id'].map(subject_map)
    filtered_tasks = filtered_tasks[filtered_tasks['subject_name'].isin(subject_filter)]
    
    if filtered_tasks.empty:
        st.info("Nenhuma tarefa corresponde aos filtros selecionados.")
        # Try to show report generation even if empty to avoid syntax errors
    else:
        # Display tasks
        for index, row in filtered_tasks.iterrows():
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{row['title']}**")
                    st.caption(f"📅 {row['due_date']} | 📚 {row['subject_name']}")
                
                with col2:
                    # Grade input
                    current_grade = row.get('grade')
                    nota_val = float(current_grade) if pd.notna(current_grade) and current_grade is not None else 0.0
                    
                    grade_key = f"grade_{row['id']}"
                    check_key = f"check_{row['id']}"

                    st.number_input(
                        "Nota", 
                        min_value=0.0, 
                        max_value=10.0, 
                        value=nota_val, 
                        step=0.5,
                        key=grade_key,
                        on_change=on_task_change,
                        args=(row['id'], check_key, grade_key)
                    )
                    
                with col3:
                    # Checkbox and Delete
                    st.container(height=28, border=False) # Spacing to align with middle of col1
                    st.checkbox(
                        "Concluída", 
                        value=row['completed'], 
                        key=check_key,
                        on_change=on_task_change,
                        args=(row['id'], check_key, grade_key)
                    )
                    
                    if st.button("🗑️", key=f"del_{row['id']}", help="Excluir tarefa"):
                        with st.spinner("Excluindo..."):
                            from services.xano import delete_task
                            resp = delete_task(token, row['id'])
                            if resp["success"]:
                                st.rerun()
                            else:
                                st.error("Erro ao excluir.")
    
    st.divider()

    # Report generation
    st.subheader("Relatórios")
    st.write("Baixe o relatório completo de suas tarefas.")

    if st.button("Gerar Relatório PDF"):
        # Passa todas as tarefas (não apenas o filtrado) e a lista completa de disciplinas
        all_tasks_df = pd.DataFrame(tasks)
        if not all_tasks_df.empty:
            all_tasks_df["subject_name"] = all_tasks_df["subject_id"].map(subject_map)
        pdf_bytes = generate_pdf_report(all_tasks_df, subjects, st.session_state.get("user_name", "Estudante"))
        st.download_button(
            label="Baixar Arquivo PDF",
            data=pdf_bytes,
            file_name="relatorio_edutrack.pdf",
            mime="application/pdf"
        )
