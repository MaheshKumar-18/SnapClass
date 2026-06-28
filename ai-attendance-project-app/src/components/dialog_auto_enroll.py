import time
import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("⚡ Quick Enrollment", width="large")
def auto_enroll_dialog(subject_code):

    student_id = st.session_state.student_data["student_id"]

    with st.spinner("Loading subject..."):

        res = (
            supabase.table("subjects")
            .select("subject_id, name, subject_code")
            .eq("subject_code", subject_code)
            .execute()
        )

    if not res.data:

        st.error("❌ Subject not found.")

        if st.button(
            "Close",
            width="stretch",
            icon=":material/close:",
        ):
            st.query_params.clear()
            st.rerun()

        return

    subject = res.data[0]

    check = (
        supabase.table("subject_students")
        .select("*")
        .eq("subject_id", subject["subject_id"])
        .eq("student_id", student_id)
        .execute()
    )

    if check.data:

        st.info(f"✅ You are already enrolled in **{subject['name']}**.")

        if st.button(
            "Done",
            type="primary",
            width="stretch",
            icon=":material/check_circle:",
        ):
            st.query_params.clear()
            st.rerun()

        return

    st.markdown(f"## 📚 {subject['name']}")
    st.caption("Would you like to join this subject?")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "Cancel",
            width="stretch",
            icon=":material/close:",
        ):
            st.query_params.clear()
            st.rerun()

    with c2:

        if st.button(
            "Join Subject",
            type="primary",
            width="stretch",
            icon=":material/school:",
        ):

            enroll_student_to_subject(
                student_id,
                subject["subject_id"],
            )

            st.success(
                f"🎉 Successfully joined {subject['name']}!"
            )

            st.query_params.clear()

            time.sleep(1)

            st.rerun()