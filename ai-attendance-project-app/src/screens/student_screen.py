import streamlit as st

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout,
)

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.components.dialog_enroll import enroll_dialog

from PIL import Image
import numpy as np
import time

from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier,
)

from src.pipelines.voice_pipeline import (
    get_voice_embedding,
)

from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject,
)


def student_dashboard():

    student_data = st.session_state.student_data
    student_id = student_data["student_id"]

    left, right = st.columns([2, 1], vertical_alignment="center")

    with left:
        header_dashboard()

    with right:

        st.markdown("### 👋 Welcome")
        st.markdown(f"## {student_data['name']}")

        if st.button(
            "Logout",
            type="secondary",
            width="stretch",
            icon=":material/logout:",
        ):
            st.session_state["is_logged_in"] = False
            del st.session_state.student_data
            st.rerun()

    st.divider()

    with st.spinner("Loading dashboard..."):

        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:

        sid = log["subject_id"]

        if sid not in stats_map:
            stats_map[sid] = {
                "total": 0,
                "attended": 0,
            }

        stats_map[sid]["total"] += 1

        if log.get("is_present"):
            stats_map[sid]["attended"] += 1

    total_subjects = len(subjects)

    total_classes = sum(
        s["total"]
        for s in stats_map.values()
    )

    attended_classes = sum(
        s["attended"]
        for s in stats_map.values()
    )

    percentage = (
        round(attended_classes / total_classes * 100)
        if total_classes
        else 0
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "📚 Subjects",
            total_subjects,
        )

    with c2:
        st.metric(
            "📅 Classes",
            total_classes,
        )

    with c3:
        st.metric(
            "📈 Attendance",
            f"{percentage}%",
        )

    st.divider()

    h1, h2 = st.columns([2, 1])

    with h1:
        st.header("Your Subjects")

    with h2:

        if st.button(
            "Enroll Subject",
            type="primary",
            width="stretch",
            icon=":material/add:",
        ):
            enroll_dialog()

    st.divider()

    cols = st.columns(2)

    for index, node in enumerate(subjects):

        sub = node["subjects"]

        sid = sub["subject_id"]

        stats = stats_map.get(
            sid,
            {
                "total": 0,
                "attended": 0,
            },
        )

        def unenroll_button(
            sid=sid,
            name=sub["name"],
        ):

            if st.button(
                "Unenroll",
                key=f"un_{sid}",
                width="stretch",
                type="tertiary",
                icon=":material/delete:",
            ):

                unenroll_student_to_subject(
                    student_id,
                    sid,
                )

                st.toast(
                    f"Removed from {name}",
                    icon="✅",
                )

                st.rerun()

        with cols[index % 2]:

            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=[
                    (
                        "📅",
                        "Total",
                        stats["total"],
                    ),
                    (
                        "✅",
                        "Attended",
                        stats["attended"],
                    ),
                ],
                footer_callback=unenroll_button,
            )

    footer_dashboard()


def student_screen():

    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    left, right = st.columns(
        [2, 1],
        vertical_alignment="center",
    )

    with left:
        header_dashboard()

    with right:

        if st.button(
            "Back Home",
            type="secondary",
            width="stretch",
            icon=":material/home:",
        ):

            st.session_state["login_type"] = None
            st.rerun()

    st.header("Student Face Login")

    st.caption(
        "Position your face in front of the camera."
    )

    st.divider()

    show_registration = False

    photo_source = st.camera_input(
        "Capture Face"
    )
    if photo_source:

        img = np.array(Image.open(photo_source))

        with st.spinner("Scanning face..."):

            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:

                st.warning("No face detected.")

            elif num_faces > 1:

                st.warning("Multiple faces detected.")

            else:

                if detected:

                    student_id = list(detected.keys())[0]

                    students = get_all_students()

                    student = next(
                        (
                            s
                            for s in students
                            if s["student_id"] == student_id
                        ),
                        None,
                    )

                    if student:

                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student

                        st.toast(
                            f"Welcome back, {student['name']}!",
                            icon="👋",
                        )

                        time.sleep(1)

                        st.rerun()

                else:

                    st.info(
                        "Face not recognized. Please create a new account."
                    )

                    show_registration = True

    if show_registration:

        st.divider()

        with st.container(border=True):

            st.header("Create Student Profile")

            st.caption(
                "Register your face and optional voice profile."
            )

            new_name = st.text_input(
                "Full Name",
                placeholder="John Doe",
            )

            st.subheader("🎤 Voice Enrollment (Optional)")

            st.info(
                "Recording your voice improves voice attendance accuracy."
            )

            audio_data = None

            try:

                audio_data = st.audio_input(
                    "Say: My name is John. I am present."
                )

            except Exception:

                st.warning(
                    "Voice recording is unavailable."
                )

            if st.button(
                "Create Account",
                type="primary",
                width="stretch",
                icon=":material/person_add:",
            ):

                if not new_name:

                    st.warning(
                        "Please enter your name."
                    )

                else:

                    with st.spinner(
                        "Creating your account..."
                    ):

                        img = np.array(
                            Image.open(photo_source)
                        )

                        encodings = get_face_embeddings(
                            img
                        )

                        if encodings:

                            face_embedding = (
                                encodings[0].tolist()
                            )

                            voice_embedding = None

                            if audio_data:

                                voice_embedding = (
                                    get_voice_embedding(
                                        audio_data.read()
                                    )
                                )

                            response = create_student(
                                new_name.strip(),
                                face_embedding=face_embedding,
                                voice_embedding=voice_embedding,
                            )

                            if response:

                                train_classifier()

                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response[0]

                                st.toast(
                                    "Account created successfully!",
                                    icon="🎉",
                                )

                                time.sleep(1)

                                st.rerun()

                        else:

                            st.error(
                                "Unable to extract facial features. Please try again."
                            )

    footer_dashboard()

