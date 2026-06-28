import io
import segno
import streamlit as st


@st.dialog("🔗 Share Subject", width="large")
def share_subject_dialog(subject_name, subject_code):

    app_domain = "https://snapclass-main.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.markdown(f"## 📚 {subject_name}")
    st.caption("Invite students by sharing the QR code or link below.")

    st.divider()

    qr = segno.make(join_url)

    out = io.BytesIO()
    qr.save(out, kind="png", scale=8, border=2)

    col1, col2 = st.columns([1.2, 1])

    with col1:

        st.markdown("### 🔗 Join Link")

        st.code(join_url, language="text")

        st.markdown("### 🔑 Subject Code")

        st.code(subject_code, language="text")

        st.info(
            "Share the link or subject code with students using WhatsApp, Email, or any messaging platform."
        )

    with col2:

        st.markdown("### 📱 Scan QR Code")

        st.image(
            out.getvalue(),
            use_container_width=True,
            caption="Students can scan this QR code to join instantly.",
        )

    st.divider()

    st.success("Students can join using either the QR code or the subject code.")