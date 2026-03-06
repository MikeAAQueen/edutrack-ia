from fpdf import FPDF
import io

def generate_pdf_report(filtered_tasks, user_name):
    """
    Generates a PDF report using fpdf.
    Returns the PDF as a byte string ready for st.download_button.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"Relatório Semanal de Tarefas - EduTrack AI", ln=1, align='C')
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(200, 10, txt=f"Gerado para: {user_name}", ln=1, align='C')
    
    pdf.ln(10)
    
    # Pendentes
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Tarefas Pendentes", ln=1)
    
    pdf.set_font("Arial", '', 12)
    pendentes = filtered_tasks[filtered_tasks['completed'] == False]
    
    if pendentes.empty:
        pdf.cell(200, 10, txt="Nenhuma tarefa pendente.", ln=1)
    else:
        for idx, row in pendentes.iterrows():
            txt = f"- {row['title']} (Disciplina: {row.get('subject_name', row['subject_id'])}) - Prazo: {row['due_date']}"
            pdf.cell(200, 10, txt=txt, ln=1)
            
    pdf.ln(5)
    
    # Concluidas
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Tarefas Concluídas", ln=1)
    
    pdf.set_font("Arial", '', 12)
    concluidas = filtered_tasks[filtered_tasks['completed'] == True]
    
    if concluidas.empty:
        pdf.cell(200, 10, txt="Nenhuma tarefa concluída.", ln=1)
    else:
        for idx, row in concluidas.iterrows():
            txt = f"- {row['title']} (Disciplina: {row.get('subject_name', row['subject_id'])})"
            pdf.cell(200, 10, txt=txt, ln=1)
            
    # Output to buffer instead of file
    # fpdf2 allows output as string with output(dest='S')
    pdf_string = pdf.output(dest='S')
    
    if isinstance(pdf_string, str):
        return pdf_string.encode('latin-1')
    return pdf_string
