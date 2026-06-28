import time
import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("📚 Enroll in Subject", width="large")
def enroll_dialog():

    st.markdown("## Join a Subject")
    st.caption(
        "Enter the subject code shared by your teacher to join the class."
    )

    st.divider()

    join_code = st.text_input(
        "Subject Code",
        placeholder="Example: CS101",
    )

    st.divider()

    if st.button(
        "Enroll Now",
        type="primary",
        width="stretch",
        icon=":material/school:",
    ):

        join_code = join_code.strip().upper()

        if not join_code:
            st.warning("Please enter a subject code.")
            return

        with st.spinner("Checking subject..."):

            res = (
                supabase.table("subjects")
                .select("subject_id, name, subject_code")
                .eq("subject_code", join_code)
                .execute()
            )

            if not res.data:
                st.error("Subject not found.")
                return

            subject = res.data[0]

            student_id = st.session_state.student_data["student_id"]

            check = (
                supabase.table("subject_students")
                .select("*")
                .eq("subject_id", subject["subject_id"])
                .eq("student_id", student_id)
                .execute()
            )

            if check.data:
                st.info(
                    f"You are already enrolled in **{subject['name']}**."
                )
                return

            enroll_student_to_subject(
                student_id,
                subject["subject_id"],
            )

            st.success(
                f"🎉 Successfully enrolled in {subject['name']}!"
            )

            time.sleep(1)

            st.rerun()