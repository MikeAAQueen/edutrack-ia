import streamlit as st
import pandas as pd
from services.xano import (
    fetch_subjects,
    create_subject,
    update_subject_absences,
    update_subject,
)


def show_subjects():
    """
    Renders the Subjects management screen. 
    """
    st.title("📚 Gerenciar Disciplinas")

    token = st.session_state.get("user_token", "mock_jwt_token_123")

    # Sidebar for adding new subject
    st.sidebar.header("➕ Adicionar Nova")
    with st.sidebar.form("add_subject_form"):
        new_name = st.text_input("Nome da Disciplina")
        new_professor = st.text_input("Professor(a)")
        new_credits = st.number_input("Créditos", min_value=1, max_value=20, value=4)
        new_workload = st.number_input(
            "Carga Horária (h)", min_value=1, max_value=300, value=60
        )
        submit_btn = st.form_submit_button("Adicionar")

        if submit_btn:
            if not new_name or not new_professor:
                st.sidebar.warning("Preencha todos os campos obrigatórios.")
            else:
                resp = create_subject(
                    token, new_name, new_professor, new_credits, new_workload
                )
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

        # Calcula o percentual de faltas e define o status de risco
        def get_risk_status(perc):
            if perc > 25.0:
                return "🟥 VOCÊ ESTÁ REPROVADO"
            elif perc == 25.0:
                return "🟥 VOCÊ ESTÁ NO LIMITE DAS FALTAS"
            elif perc >= 20.0:
                return "🟧 Você está perto do limite de faltas"
            elif perc >= 12.5:
                return "🟨 Cuidado com as faltas"
            else:
                return "🟦 Faltas sob controle"

        def set_absences_callback(subj_id, new_abs):
            # Using session_state user_token directly here because the callback receives it on execution
            update_subject_absences(st.session_state.get("user_token"), subj_id, new_abs)

        # --- Header Row ---
        h_cols = st.columns([3, 2, 1, 1, 3, 4])
        h_cols[0].markdown("**Nome**")
        h_cols[1].markdown("**Professor(a)**")
        h_cols[2].markdown("**Créditos**")
        h_cols[3].markdown("**Carga Horária**")
        # O header de 'Faltas' está alinhado ao centro da sub-coluna do número
        _, faltas_header_col, _ = h_cols[4].columns([1, 2, 1])
        faltas_header_col.markdown(
            "<div class='center-bold'>Faltas</div>", unsafe_allow_html=True
        )
        h_cols[5].markdown("**Status**")
        st.divider()

        # --- One row per subject ---
        for subject in subjects:
            subject_id = subject["id"]
            current_abs = subject.get("absences", 0)
            workload = subject.get("workload", 1)
            perc = (current_abs / workload * 100) if workload > 0 else 0
            risk_text = get_risk_status(perc)

            row = st.columns([3, 2, 1, 1, 3, 4])
            row[0].write(subject["name"])
            row[1].write(subject["professor"])
            row[2].markdown(
                f"<div class='center-bold'>{subject.get('credits', '-')}</div>",
                unsafe_allow_html=True,
            )
            row[3].markdown(
                f"<div class='center-bold'>{workload}</div>",
                unsafe_allow_html=True,
            )

            # Faltas column with − number ＋
            minus_col, num_col, plus_col = row[4].columns([1, 2, 1])
            minus_col.button(
                "−", key=f"minus_{subject_id}", use_container_width=True,
                on_click=set_absences_callback, args=(subject_id, max(0, current_abs - 1))
            )

            num_col.markdown(
                f"<div class='center-bold-pad'>{current_abs}</div>",
                unsafe_allow_html=True,
            )

            plus_col.button(
                "＋", key=f"plus_{subject_id}", use_container_width=True,
                on_click=set_absences_callback, args=(subject_id, current_abs + 1)
            )

            row[5].write(risk_text)

        st.divider()
        st.subheader("GERENCIAR DISCIPLINAS")

        selected_id = st.selectbox(
            "Selecione uma disciplina:",
            options=df_subjects["id"],
            format_func=lambda x: df_subjects[df_subjects["id"] == x]["name"].values[0],
            key="manage_subject_select",
        )

        # Determine selected subject data
        selected_row = df_subjects[df_subjects["id"] == selected_id].iloc[0]

        # ----- EDIT DIALOG -----
        @st.dialog(f"Editar: {selected_row['name']}")
        def edit_dialog():
            edit_name = st.text_input("Nome da Disciplina", value=selected_row["name"])
            edit_prof = st.text_input("Professor(a)", value=selected_row["professor"])
            edit_cred = st.number_input(
                "Créditos",
                min_value=1,
                max_value=20,
                value=int(selected_row["credits"]),
            )
            edit_wl = st.number_input(
                "Carga Horária (h)",
                min_value=1,
                max_value=300,
                value=int(selected_row["workload"]),
            )
            st.divider()
            btn_col1, btn_col2 = st.columns(2)
            if btn_col1.button("OK ✔️", use_container_width=True, type="primary"):
                with st.spinner("Salvando..."):
                    resp = update_subject(
                        token, selected_id, edit_name, edit_prof, edit_cred, edit_wl
                    )
                if resp["success"]:
                    st.success("Disciplina atualizada!")
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
                    from services.xano import delete_subject

                    resp = delete_subject(token, selected_id)
                    if resp["success"]:
                        st.success("Disciplina excluída com sucesso!")
                        st.rerun()
                    else:
                        st.error(resp["error"])
