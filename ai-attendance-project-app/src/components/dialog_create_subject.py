import streamlit as st
from src.database.db import create_subject


@st.dialog("📚 Create New Subject", width="large")
def create_subject_dialog(teacher_id):

    st.markdown("### Create a New Course")
    st.caption("Fill in the details below to create a new subject.")

    st.divider()

    sub_id = st.text_input(
        "📌 Subject Code",
        placeholder="Example: CS101"
    )

    sub_name = st.text_input(
        "📖 Subject Name",
        placeholder="Example: Introduction to Computer Science"
    )

    sub_section = st.text_input(
        "🏫 Section",
        placeholder="Example: A"
    )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        if st.button(
            "Create Subject",
            type="primary",
            width="stretch",
            icon=":material/add_circle:"
        ):

            if not sub_id or not sub_name or not sub_section:
                st.warning("Please fill all the fields.")
                return

            try:
                create_subject(
                    sub_id.strip().upper(),
                    sub_name.strip(),
                    sub_section.strip().upper(),
                    teacher_id,
                )

                st.toast(
                    "🎉 Subject created successfully!",
                    icon="✅"
                )

                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")

    with c2:
        if st.button(
            "Clear",
            width="stretch",
            icon=":material/refresh:"
        ):
            st.rerun()