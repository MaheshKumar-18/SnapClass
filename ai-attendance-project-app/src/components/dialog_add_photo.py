import streamlit as st
from PIL import Image


@st.dialog("📷 Add Classroom Photos", width="large")
def add_photos_dialog():

    st.markdown("### AI Attendance Photo Collection")
    st.caption(
        "Capture photos using your camera or upload classroom images for AI attendance."
    )

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        if st.button(
            "📸 Camera",
            type="primary" if st.session_state.photo_tab == "camera" else "secondary",
            width="stretch",
        ):
            st.session_state.photo_tab = "camera"

    with c2:
        if st.button(
            "🖼 Upload Images",
            type="primary" if st.session_state.photo_tab == "upload" else "secondary",
            width="stretch",
        ):
            st.session_state.photo_tab = "upload"

    st.divider()

    # ---------------- Camera ---------------- #

    if st.session_state.photo_tab == "camera":

        cam_photo = st.camera_input(
            "Capture Classroom Photo",
            key="dialog_cam",
        )

        if cam_photo:

            st.session_state.attendance_images.append(Image.open(cam_photo))

            st.toast(
                "📸 Photo added successfully!",
                icon="✅",
            )

            st.rerun()

    # ---------------- Upload ---------------- #

    else:

        uploaded_files = st.file_uploader(
            "Choose classroom images",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="dialog_upload",
        )

        if uploaded_files:

            for file in uploaded_files:
                st.session_state.attendance_images.append(Image.open(file))

            st.toast(
                f"✅ {len(uploaded_files)} photo(s) uploaded successfully!",
                icon="🎉",
            )

            st.rerun()

    st.divider()

    st.info(
        f"Currently Added Photos : **{len(st.session_state.attendance_images)}**"
    )

    if st.button(
        "Done",
        type="primary",
        width="stretch",
        icon=":material/check_circle:",
    ):
        st.rerun()