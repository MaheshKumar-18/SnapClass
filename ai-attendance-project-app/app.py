
import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog


def configure_page():

    st.set_page_config(
        page_title="SnapClass | AI Smart Attendance",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def initialize_session():

    defaults = {
        "login_type": None,
        "is_logged_in": False,
        "user_role": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def route_pages():

    match st.session_state.login_type:

        case "teacher":
            teacher_screen()

        case "student":
            student_screen()

        case _:
            home_screen()


def handle_join_link():

    join_code = st.query_params.get("join-code")

    if not join_code:
        return

    if st.session_state.login_type != "student":

        st.session_state.login_type = "student"
        st.rerun()

    if (
        st.session_state.get("is_logged_in")
        and st.session_state.get("user_role") == "student"
    ):

        auto_enroll_dialog(join_code)


def main():

    configure_page()

    initialize_session()

    route_pages()

    handle_join_link()


if __name__ == "__main__":
    main()