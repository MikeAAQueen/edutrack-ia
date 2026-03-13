from fpdf import FPDF
from datetime import date
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend (no display needed)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io


# ── helpers ────────────────────────────────────────────────────────────────────
def _safe(text) -> str:
    if not isinstance(text, str):
        text = str(text)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _absence_status(perc: float) -> str:
    if perc > 25.0:
        return "REPROVADO POR FALTAS"
    elif perc >= 25.0:
        return "NO LIMITE"
    elif perc >= 20.0:
        return "Perto do limite"
    elif perc >= 12.5:
        return "Cuidado"
    return "Sob controle"


def _chart_to_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf


# ── chart builders ─────────────────────────────────────────────────────────────
def _build_grades_chart(subjects, tasks_df):
    """Bar chart: average grade per subject."""
    names, avgs = [], []
    for s in subjects:
        st = tasks_df[tasks_df["subject_id"] == s["id"]] if not tasks_df.empty else pd.DataFrame()
        if not st.empty and "grade" in st.columns:
            g = pd.to_numeric(st["grade"], errors="coerce").dropna()
            avgs.append(float(g.mean()) if not g.empty else 0.0)
        else:
            avgs.append(0.0)
        # Short label
        names.append(s["name"][:18] + ("…" if len(s["name"]) > 18 else ""))

    colors = ["#2ecc71" if a >= 5 else "#e74c3c" for a in avgs]

    fig, ax = plt.subplots(figsize=(8, 3.5))
    bars = ax.bar(names, avgs, color=colors, width=0.5, zorder=3)
    ax.axhline(5, color="#e74c3c", linestyle="--", linewidth=1.2, label="Média mínima (5.0)")
    ax.axhline(7, color="#27ae60", linestyle="--", linewidth=1.0, label="Boa média (7.0)")
    ax.set_ylim(0, 10.5)
    ax.set_ylabel("Média", fontsize=9)
    ax.set_title("Média de Notas por Disciplina", fontsize=11, fontweight="bold")
    ax.legend(fontsize=8)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
    ax.set_axisbelow(True)
    for bar, val in zip(bars, avgs):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15,
                    f"{val:.1f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
    plt.xticks(fontsize=8, rotation=15, ha="right")
    plt.tight_layout()
    return _chart_to_bytes(fig)


def _build_absences_chart(subjects):
    """Bar chart: absence % per subject with 25% limit line."""
    names, percs = [], []
    for s in subjects:
        wl = s.get("workload", 1) or 1
        ab = s.get("absences", 0)
        percs.append((ab / wl) * 100)
        names.append(s["name"][:18] + ("…" if len(s["name"]) > 18 else ""))

    colors = []
    for p in percs:
        if p >= 25:
            colors.append("#e74c3c")
        elif p >= 20:
            colors.append("#e67e22")
        elif p >= 12.5:
            colors.append("#f1c40f")
        else:
            colors.append("#2ecc71")

    fig, ax = plt.subplots(figsize=(8, 3.5))
    bars = ax.bar(names, percs, color=colors, width=0.5, zorder=3)
    ax.axhline(25, color="#e74c3c", linestyle="--", linewidth=1.4, label="Limite de faltas (25%)")
    ax.set_ylim(0, max(max(percs) + 8, 30))
    ax.set_ylabel("Faltas (%)", fontsize=9)
    ax.set_title("Percentual de Faltas por Disciplina", fontsize=11, fontweight="bold")

    # Legend patches
    legend_elements = [
        mpatches.Patch(color="#2ecc71", label="Sob controle (<12.5%)"),
        mpatches.Patch(color="#f1c40f", label="Cuidado (12.5–20%)"),
        mpatches.Patch(color="#e67e22", label="Perto do limite (20–25%)"),
        mpatches.Patch(color="#e74c3c", label="No limite / Reprovado (≥25%)"),
    ]
    ax.legend(handles=legend_elements, fontsize=7, loc="upper right")
    ax.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
    ax.set_axisbelow(True)
    for bar, val in zip(bars, percs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.4,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=8, fontweight="bold")
    plt.xticks(fontsize=8, rotation=15, ha="right")
    plt.tight_layout()
    return _chart_to_bytes(fig)


def _build_tasks_chart(subjects, tasks_df):
    """Stacked bar chart: done vs pending tasks per subject."""
    names, done_counts, pend_counts = [], [], []
    for s in subjects:
        st = tasks_df[tasks_df["subject_id"] == s["id"]] if not tasks_df.empty else pd.DataFrame()
        done = int(st["completed"].sum()) if not st.empty else 0
        pend = len(st) - done if not st.empty else 0
        names.append(s["name"][:18] + ("…" if len(s["name"]) > 18 else ""))
        done_counts.append(done)
        pend_counts.append(pend)

    fig, ax = plt.subplots(figsize=(8, 3.5))
    x = range(len(names))
    b1 = ax.bar(x, done_counts, color="#2ecc71", width=0.5, label="Concluídas", zorder=3)
    b2 = ax.bar(x, pend_counts, bottom=done_counts, color="#e74c3c", width=0.5, label="Pendentes", zorder=3)
    ax.set_xticks(list(x))
    ax.set_xticklabels(names, fontsize=8, rotation=15, ha="right")
    ax.set_ylabel("Qtd. Tarefas", fontsize=9)
    ax.set_title("Tarefas Concluídas vs Pendentes por Disciplina", fontsize=11, fontweight="bold")
    ax.legend(fontsize=9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
    ax.set_axisbelow(True)
    plt.tight_layout()
    return _chart_to_bytes(fig)


# ── embed helper ───────────────────────────────────────────────────────────────
def _embed_chart(pdf: FPDF, buf: io.BytesIO, title: str, w=190):
    import tempfile, os
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(buf.read())
        tmp_path = tmp.name
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 7, _safe(title), ln=True)
    pdf.image(tmp_path, x=10, w=w)
    pdf.ln(4)
    os.unlink(tmp_path)


# ── main function ───────────────────────────────────────────────────────────────
def generate_pdf_report(tasks_df: pd.DataFrame, subjects: list, user_name: str) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    today = date.today().strftime("%d/%m/%Y")

    # ── CAPA ──────────────────────────────────────────────────────────────────
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 12, _safe("EduTrack AI"), ln=True, align="C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 8, _safe("Relatorio Academico Completo"), ln=True, align="C")
    pdf.cell(0, 8, _safe(f"Aluno: {user_name}   |   Data: {today}"), ln=True, align="C")
    pdf.ln(6)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    # Ensure subject_name column
    if not tasks_df.empty and "subject_name" not in tasks_df.columns:
        tasks_df = tasks_df.copy()
        tasks_df["subject_name"] = tasks_df["subject_id"].map(
            {s["id"]: s["name"] for s in subjects}
        )

    # ── SECAO: GRAFICOS ───────────────────────────────────────────────────────
    pdf.set_font("Arial", "B", 14)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 9, _safe("1. GRAFICOS DE DESEMPENHO"), ln=True, fill=True)
    pdf.ln(4)

    _embed_chart(pdf, _build_grades_chart(subjects, tasks_df),
                 "Media de Notas por Disciplina")
    _embed_chart(pdf, _build_tasks_chart(subjects, tasks_df),
                 "Tarefas Concluidas vs Pendentes por Disciplina")
    _embed_chart(pdf, _build_absences_chart(subjects),
                 "Percentual de Faltas por Disciplina (limite: 25%)")

    # ── SECAO: RESUMO GERAL ───────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 9, _safe("2. RESUMO GERAL DAS DISCIPLINAS"), ln=True, fill=True)
    pdf.ln(4)

    col_w = [52, 20, 18, 18, 22, 20, 34]
    headers = ["Disciplina", "Tarefas", "Feitas", "Pend.", "Media", "Faltas%", "Status Faltas"]
    pdf.set_font("Arial", "B", 9)
    pdf.set_fill_color(60, 60, 60)
    pdf.set_text_color(255, 255, 255)
    for w, h in zip(col_w, headers):
        pdf.cell(w, 7, _safe(h), border=1, fill=True)
    pdf.ln()
    pdf.set_text_color(0, 0, 0)

    pdf.set_font("Arial", "", 9)
    alt = False
    for s in subjects:
        st = tasks_df[tasks_df["subject_id"] == s["id"]] if not tasks_df.empty else pd.DataFrame()
        total   = len(st)
        done    = int(st["completed"].sum()) if total else 0
        pending = total - done
        grades  = pd.to_numeric(st["grade"].dropna() if total and "grade" in st.columns else pd.Series([], dtype=float), errors="coerce").dropna()
        avg_g   = f"{grades.mean():.1f}" if not grades.empty else "-"
        wl      = s.get("workload", 1) or 1
        ab      = s.get("absences", 0)
        perc    = (ab / wl) * 100
        status  = _absence_status(perc)

        bg = (245, 245, 245) if alt else (255, 255, 255)
        pdf.set_fill_color(*bg)
        row_vals = [s["name"], str(total), str(done), str(pending), avg_g, f"{perc:.1f}%", status]
        for w, v in zip(col_w, row_vals):
            pdf.cell(w, 7, _safe(v), border=1, fill=True)
        pdf.ln()
        alt = not alt

    pdf.ln(8)

    # ── SECAO: DETALHE POR DISCIPLINA ─────────────────────────────────────────
    pdf.set_font("Arial", "B", 14)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 9, _safe("3. DETALHAMENTO POR DISCIPLINA"), ln=True, fill=True)
    pdf.ln(4)

    for s in subjects:
        sid = s["id"]
        st  = tasks_df[tasks_df["subject_id"] == sid] if not tasks_df.empty else pd.DataFrame()
        wl  = s.get("workload", 1) or 1
        ab  = s.get("absences", 0)
        perc = (ab / wl) * 100
        status = _absence_status(perc)
        done   = int(st["completed"].sum()) if not st.empty else 0
        total  = len(st)
        pend   = total - done
        grades = pd.to_numeric(st["grade"].dropna() if not st.empty and "grade" in st.columns else pd.Series([], dtype=float), errors="coerce").dropna()
        avg_g  = f"{grades.mean():.1f}" if not grades.empty else "Sem notas"

        # Subject heading
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(70, 130, 180)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 8, _safe(f"  {s['name']}  —  Prof. {s['professor']}"), ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 10)
        pdf.ln(2)

        stats = (f"Creditos: {s.get('credits','?')}  |  Carga Horaria: {wl}h  |  "
                 f"Faltas: {ab}/{int(wl*0.25)} ({perc:.1f}%)  |  Status: {status}")
        pdf.cell(0, 7, _safe(stats), ln=True)

        task_line = (f"Tarefas: {total} total  |  {done} concluidas  |  "
                     f"{pend} pendentes  |  Media notas: {avg_g}")
        pdf.cell(0, 7, _safe(task_line), ln=True)
        pdf.ln(3)

        if st.empty:
            pdf.set_font("Arial", "I", 9)
            pdf.cell(0, 6, _safe("   Nenhuma tarefa cadastrada."), ln=True)
        else:
            t_cols = [78, 28, 18, 26, 34]
            t_hdrs = ["Titulo", "Prazo", "Nota", "Status", "Situacao Nota"]
            pdf.set_font("Arial", "B", 8)
            pdf.set_fill_color(200, 200, 200)
            for w, h in zip(t_cols, t_hdrs):
                pdf.cell(w, 6, _safe(h), border=1, fill=True)
            pdf.ln()

            pdf.set_font("Arial", "", 8)
            row_alt = False
            for _, task in st.iterrows():
                raw_g = task.get("grade")
                try:
                    gv = float(raw_g) if raw_g is not None and pd.notna(raw_g) else None
                except (ValueError, TypeError):
                    gv = None
                g_str  = f"{gv:.1f}" if gv is not None else "-"
                sit    = "Aprovado" if gv is not None and gv >= 5.0 else ("Reprovado" if gv is not None else "-")
                done_s = "Concluida" if task.get("completed") else "Pendente"

                bg = (248, 248, 248) if row_alt else (255, 255, 255)
                pdf.set_fill_color(*bg)
                for w, v in zip(t_cols, [str(task.get("title", "")), str(task.get("due_date", "-")), g_str, done_s, sit]):
                    pdf.cell(w, 6, _safe(v), border=1, fill=True)
                pdf.ln()
                row_alt = not row_alt

        pdf.ln(8)

    # ── OUTPUT ────────────────────────────────────────────────────────────────
    pdf_string = pdf.output(dest="S")
    if isinstance(pdf_string, str):
        return pdf_string.encode("latin-1")
    return bytes(pdf_string)
