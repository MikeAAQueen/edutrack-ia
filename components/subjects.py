import streamlit as st
import pandas as pd
from services.xano import (
    fetch_subjects,
    create_subject,
    update_subject_absences,
    update_subject,
    fetch_professors,
)


def show_subjects():
    """
    Renders the Subjects management screen. 
    """
    st.title("📚 Gerenciar Disciplinas")

    token = st.session_state.get("user_token", "mock_jwt_token_123")

    professors = fetch_professors(token)
    if not professors:
        st.warning("Cadastre algum professor primeiro antes de gerenciar disciplinas.")
        return
        
    df_professors = pd.DataFrame(professors)
    prof_map = dict(zip(df_professors['id'], df_professors['name']))

    # Sidebar for adding new subject
    st.sidebar.header("➕ Adicionar Nova")
    with st.sidebar.form("add_subject_form"):
        new_name = st.text_input("Nome da Disciplina")
        new_professor_name = st.selectbox("Professor(a)", options=list(prof_map.values()))
        new_workload = st.number_input(
            "Carga Horária (h)", min_value=1, max_value=300, value=60
        )
        submit_btn = st.form_submit_button("Adicionar")

        if submit_btn:
            if not new_name:
                st.sidebar.warning("Preencha todos os campos obrigatórios.")
            else:
                new_professor_id = list(prof_map.keys())[list(prof_map.values()).index(new_professor_name)]
                resp = create_subject(
                    token, new_name, new_professor_id, new_workload
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
        h_cols = st.columns([3, 3, 1, 3, 4])
        h_cols[0].markdown("**Nome**")
        h_cols[1].markdown("**Professor(a)**")
        h_cols[2].markdown("**Carga Horária**")
        # O header de 'Faltas' está alinhado ao centro da sub-coluna do número
        _, faltas_header_col, _ = h_cols[3].columns([1, 2, 1])
        faltas_header_col.markdown(
            "<div class='center-bold'>Faltas</div>", unsafe_allow_html=True
        )
        h_cols[4].markdown("**Status**")
        st.divider()

        # --- One row per subject ---
        for subject in subjects:
            subject_id = subject["id"]
            current_abs = subject.get("absences", 0)
            workload = subject.get("workload", 1)
            perc = (current_abs / workload * 100) if workload > 0 else 0
            risk_text = get_risk_status(perc)

            row = st.columns([3, 3, 1, 3, 4])
            row[0].write(subject["name"])
            
            # Find the professor name using the mapping, fallback to an empty string if not found
            prof_name = prof_map.get(subject.get("professor_id"), "")
            row[1].write(prof_name)
            row[2].markdown(
                f"<div class='center-bold'>{workload}</div>",
                unsafe_allow_html=True,
            )

            # Faltas column with − number ＋
            minus_col, num_col, plus_col = row[3].columns([1, 2, 1])
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

            row[4].write(risk_text)

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
            
            # Find default index for professor
            current_prof_id = selected_row.get("professor_id")
            default_index = 0
            if current_prof_id in prof_map:
                prof_names = list(prof_map.values())
                default_index = prof_names.index(prof_map[current_prof_id])
                
            edit_prof_name = st.selectbox("Professor(a)", options=list(prof_map.values()), index=default_index)
            
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
                    edit_prof_id = list(prof_map.keys())[list(prof_map.values()).index(edit_prof_name)]
                    resp = update_subject(
                        token, selected_id, edit_name, edit_prof_id, edit_wl
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
