import streamlit as st
import numpy as np
import pandas as pd

from datetime import datetime

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout,
)

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card

from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog

from src.database.config import supabase

from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher,
)

from src.pipelines.face_pipeline import predict_attendance


def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()

    elif (
        "teacher_login_type" not in st.session_state
        or st.session_state.teacher_login_type == "login"
    ):
        teacher_screen_login()

    else:
        teacher_screen_register()


def teacher_dashboard():

    teacher = st.session_state.teacher_data

    left, right = st.columns([2, 1], vertical_alignment="center")

    with left:
        header_dashboard()

    with right:

        st.markdown("### 👋 Welcome")
        st.markdown(f"## {teacher['name']}")

        if st.button(
            "Logout",
            type="secondary",
            width="stretch",
            icon=":material/logout:",
        ):
            st.session_state.is_logged_in = False
            del st.session_state.teacher_data
            st.rerun()

    st.divider()

    teacher_id = teacher["teacher_id"]
    subjects = get_teacher_subjects(teacher_id)

    total_subjects = len(subjects)

    total_students = sum(
        s.get("total_students", 0)
        for s in subjects
    )

    total_classes = sum(
        s.get("total_classes", 0)
        for s in subjects
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "📚 Subjects",
            total_subjects,
        )

    with c2:
        st.metric(
            "👨‍🎓 Students",
            total_students,
        )

    with c3:
        st.metric(
            "📅 Classes",
            total_classes,
        )

    st.divider()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    t1, t2, t3 = st.columns(3)

    with t1:

        if st.button(
            "📷 Attendance",
            width="stretch",
            type="primary"
            if st.session_state.current_teacher_tab == "take_attendance"
            else "secondary",
        ):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with t2:

        if st.button(
            "📚 Subjects",
            width="stretch",
            type="primary"
            if st.session_state.current_teacher_tab == "manage_subjects"
            else "secondary",
        ):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with t3:

        if st.button(
            "📊 Reports",
            width="stretch",
            type="primary"
            if st.session_state.current_teacher_tab == "attendance_records"
            else "secondary",
        ):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    else:
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():

    teacher_id = st.session_state.teacher_data["teacher_id"]

    st.header("📷 Take AI Attendance")

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning(
            "You haven't created any subjects yet."
        )
        return

    subject_options = {
        f"{s['name']} • {s['subject_code']}": s["subject_id"]
        for s in subjects
    }

    left, right = st.columns([3, 1])

    with left:

        selected_subject = st.selectbox(
            "Select Subject",
            list(subject_options.keys()),
        )

    with right:

        if st.button(
            "Add Photos",
            width="stretch",
            type="primary",
            icon=":material/photo_library:",
        ):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject]

    st.divider()

    if st.session_state.attendance_images:

        st.subheader("Added Photos")

        cols = st.columns(4)

        for i, img in enumerate(
            st.session_state.attendance_images
        ):

            with cols[i % 4]:
                st.image(
                    img,
                    use_container_width=True,
                    caption=f"Photo {i+1}",
                )

    has_photos = bool(st.session_state.attendance_images)

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button(
            "Clear Photos",
            width="stretch",
            type="tertiary",
            icon=":material/delete:",
            disabled=not has_photos,
        ):

            st.session_state.attendance_images = []
            st.rerun()

    with c2:

        if st.button(
            "Run Face Analysis",
            width="stretch",
            type="secondary",
            icon=":material/face:",
            disabled=not has_photos,
        ):

            with st.spinner("Scanning classroom photos..."):

                detected_ids = {}

                for idx, img in enumerate(
                    st.session_state.attendance_images
                ):

                    img_np = np.array(img.convert("RGB"))

                    detected, _, _ = predict_attendance(img_np)

                    if detected:

                        for sid in detected.keys():

                            sid = int(sid)

                            detected_ids.setdefault(
                                sid,
                                [],
                            ).append(f"Photo {idx+1}")

                enrolled = (
                    supabase.table("subject_students")
                    .select("*, students(*)")
                    .eq("subject_id", selected_subject_id)
                    .execute()
                ).data

                if not enrolled:

                    st.warning("No students enrolled.")

                else:

                    rows = []
                    logs = []

                    timestamp = datetime.now().strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )

                    for node in enrolled:

                        student = node["students"]

                        sources = detected_ids.get(
                            int(student["student_id"]),
                            [],
                        )

                        present = len(sources) > 0

                        rows.append(
                            {
                                "Name": student["name"],
                                "ID": student["student_id"],
                                "Source": ", ".join(sources)
                                if present
                                else "-",
                                "Status": "✅ Present"
                                if present
                                else "❌ Absent",
                            }
                        )

                        logs.append(
                            {
                                "student_id": student["student_id"],
                                "subject_id": selected_subject_id,
                                "timestamp": timestamp,
                                "is_present": present,
                            }
                        )

                    attendance_result_dialog(
                        pd.DataFrame(rows),
                        logs,
                    )

    with c3:

        if st.button(
            "Voice Attendance",
            width="stretch",
            type="primary",
            icon=":material/mic:",
        ):
            voice_attendance_dialog(
                selected_subject_id
            )


def teacher_tab_manage_subjects():

    teacher_id = st.session_state.teacher_data[
        "teacher_id"
    ]

    left, right = st.columns([2, 1])

    with left:
        st.header("📚 Manage Subjects")

    with right:

        if st.button(
            "Create Subject",
            width="stretch",
            type="primary",
            icon=":material/add:",
        ):
            create_subject_dialog(
                teacher_id
            )

    st.divider()

    subjects = get_teacher_subjects(
        teacher_id
    )

    if not subjects:

        st.info(
            "No subjects found. Create your first subject."
        )

        return

    for sub in subjects:

        stats = [
            (
                "👨‍🎓",
                "Students",
                sub["total_students"],
            ),
            (
                "📅",
                "Classes",
                sub["total_classes"],
            ),
        ]

        def share_btn(
            subject=sub,
        ):

            if st.button(
                "Share Join Code",
                key=f"share_{subject['subject_code']}",
                width="stretch",
                icon=":material/share:",
            ):

                share_subject_dialog(
                    subject["name"],
                    subject["subject_code"],
                )

        subject_card(
            name=sub["name"],
            code=sub["subject_code"],
            section=sub["section"],
            stats=stats,
            footer_callback=share_btn,
        )
def teacher_tab_attendance_records():

    teacher_id = st.session_state.teacher_data["teacher_id"]

    st.header("📊 Attendance Reports")

    with st.spinner("Loading attendance records..."):

        records = get_attendance_for_teacher(
            teacher_id
        )

    if not records:

        st.info(
            "No attendance records found."
        )
        return

    rows = []

    for row in records:

        rows.append(
            {
                "Student": row["students"]["name"],
                "Subject": row["subjects"]["name"],
                "Date": row["timestamp"][:10],
                "Time": row["timestamp"][11:16],
                "Status": "Present"
                if row["is_present"]
                else "Absent",
            }
        )

    df = pd.DataFrame(rows)

    c1, c2 = st.columns(2)

    with c1:

        subject_filter = st.selectbox(
            "Filter by Subject",
            ["All"] + sorted(df["Subject"].unique()),
        )

    with c2:

        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Present", "Absent"],
        )

    if subject_filter != "All":
        df = df[df["Subject"] == subject_filter]

    if status_filter != "All":
        df = df[df["Status"] == status_filter]

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Export CSV",
        csv,
        "attendance_report.csv",
        "text/csv",
        type="primary",
        use_container_width=True,
    )


def teacher_screen_login():

    header_dashboard()

    st.header("Teacher Login")

    teacher_id = st.text_input(
        "Teacher ID"
    )

    password = st.text_input(
        "Password",
        type="password",
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "Login",
            type="primary",
            width="stretch",
        ):

            teacher = teacher_login(
                teacher_id,
                password,
            )

            if teacher:

                st.session_state.teacher_data = teacher
                st.session_state.is_logged_in = True

                st.rerun()

            else:

                st.error(
                    "Invalid Teacher ID or Password."
                )

    with c2:

        if st.button(
            "Create Account",
            width="stretch",
        ):

            st.session_state.teacher_login_type = (
                "register"
            )
            st.rerun()
def teacher_screen_register():

    header_dashboard()

    st.header("Create Teacher Account")

    name = st.text_input(
        "Full Name"
    )

    teacher_id = st.text_input(
        "Teacher ID"
    )

    password = st.text_input(
        "Password",
        type="password",
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "Register",
            type="primary",
            width="stretch",
        ):

            if (
                not name
                or not teacher_id
                or not password
                or not confirm_password
            ):

                st.warning(
                    "Please fill all fields."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif check_teacher_exists(
                teacher_id
            ):

                st.error(
                    "Teacher ID already exists."
                )

            else:

                create_teacher(
                    teacher_id,
                    name,
                    password,
                )

                st.success(
                    "Teacher account created successfully."
                )

                st.session_state.teacher_login_type = (
                    "login"
                )

                st.rerun()

    with c2:

        if st.button(
            "Back to Login",
            width="stretch",
        ):

            st.session_state.teacher_login_type = (
                "login"
            )

            st.rerun()

    footer_dashboard()