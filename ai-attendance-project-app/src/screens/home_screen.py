import streamlit as st

from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import (
    style_background_home,
    style_base_layout,
)


def home_screen():

    style_background_home()
    style_base_layout()

    header_home()

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.markdown(
            """
            <h2 style="
                text-align:center;
                color:#222222;
                font-weight:700;
                margin-bottom:20px;
            ">
                👨‍🎓 Student Portal
            </h2>
            """,
            unsafe_allow_html=True,
        )

        _, img_col, _ = st.columns([1, 2, 1])

        with img_col:
            st.image(
                "https://i.ibb.co/844D9Lrt/mascot-student.png",
                width=170,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "Enter Student Portal",
            type="primary",
            icon=":material/school:",
            width="stretch",
        ):
            st.session_state["login_type"] = "student"
            st.rerun()

    with col2:

        st.markdown(
            """
            <h2 style="
                text-align:center;
                color:#222222;
                font-weight:700;
                margin-bottom:20px;
            ">
                👨‍🏫 Teacher Portal
            </h2>
            """,
            unsafe_allow_html=True,
        )

        _, img_col, _ = st.columns([1, 2, 1])

        with img_col:
            st.image(
                "https://i.ibb.co/CsmQQV6X/mascot-prof.png",
                width=180,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "Enter Teacher Portal",
            type="primary",
            icon=":material/menu_book:",
            width="stretch",
        ):
            st.session_state["login_type"] = "teacher"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    footer_home()