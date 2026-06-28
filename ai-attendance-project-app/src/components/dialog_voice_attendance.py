import streamlit as st
import pandas as pd
from datetime import datetime

from src.database.config import supabase
from src.pipelines.voice_pipeline import process_bulk_audio
from src.components.dialog_attendance_results import show_attendance_result


@st.dialog("🎤 Voice Attendance", width="large")
def voice_attendance_dialog(selected_subject_id):

    st.markdown("## 🎙️ Voice Attendance")
    st.caption(
        "Record students saying 'I am present' or their names. AI will recognize enrolled students automatically."
    )

    st.divider()

    audio_data = st.audio_input("🎤 Record Classroom Audio")

    if st.button(
        "Analyze Audio",
        type="primary",
        width="stretch",
        icon=":material/graphic_eq:",
    ):

        if audio_data is None:
            st.warning("Please record classroom audio first.")
            return

        with st.spinner("🔍 Analyzing classroom audio..."):

            enrolled_res = (
                supabase.table("subject_students")
                .select("*, students(*)")
                .eq("subject_id", selected_subject_id)
                .execute()
            )

            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No students are enrolled in this subject.")
                return

            candidates_dict = {
                s["students"]["student_id"]: s["students"]["voice_embedding"]
                for s in enrolled_students
                if s["students"].get("voice_embedding")
            }

            if not candidates_dict:
                st.error("None of the enrolled students have voice profiles.")
                return

            audio_bytes = audio_data.read()

            detected_scores = process_bulk_audio(
                audio_bytes,
                candidates_dict,
            )

            results = []
            attendance_logs = []

            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:

                student = node["students"]

                score = detected_scores.get(
                    student["student_id"],
                    0.0,
                )

                is_present = score > 0

                results.append(
                    {
                        "Student": student["name"],
                        "ID": student["student_id"],
                        "Confidence": (
                            f"{score:.2f}" if is_present else "-"
                        ),
                        "Status": (
                            "✅ Present"
                            if is_present
                            else "❌ Absent"
                        ),
                    }
                )

                attendance_logs.append(
                    {
                        "student_id": student["student_id"],
                        "subject_id": selected_subject_id,
                        "timestamp": timestamp,
                        "is_present": is_present,
                    }
                )

            st.session_state.voice_attendance_results = (
                pd.DataFrame(results),
                attendance_logs,
            )

            st.success(
                f"Analysis complete! {len(results)} students processed."
            )

    if st.session_state.get("voice_attendance_results"):

        st.divider()

        df_results, logs = (
            st.session_state.voice_attendance_results
        )

        show_attendance_result(
            df_results,
            logs,
        )