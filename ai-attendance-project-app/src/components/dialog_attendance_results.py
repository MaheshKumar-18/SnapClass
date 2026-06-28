import streamlit as st
from src.database.db import create_attendance


def show_attendance_result(df, logs):

    st.markdown("## 📋 Attendance Preview")
    st.caption("Review the AI-generated attendance before saving.")

    st.divider()

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
    )

    st.divider()

    present = len(df[df["Status"].str.contains("Present")])
    absent = len(df) - present

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("👥 Total Students", len(df))

    with c2:
        st.metric("✅ Present", present)

    with c3:
        st.metric("❌ Absent", absent)

    st.divider()

    b1, b2 = st.columns(2)

    with b1:

        if st.button(
            "Discard",
            width="stretch",
            icon=":material/delete:",
        ):

            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []

            st.toast(
                "Attendance discarded.",
                icon="🗑️",
            )

            st.rerun()

    with b2:

        if st.button(
            "Confirm & Save",
            type="primary",
            width="stretch",
            icon=":material/save:",
        ):

            try:

                create_attendance(logs)

                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None

                st.toast(
                    "Attendance saved successfully!",
                    icon="✅",
                )

                st.rerun()

            except Exception as e:
                st.error(f"Failed to save attendance.\n\n{e}")


@st.dialog("📊 Attendance Results", width="large")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)