import streamlit as st


LOGO_URL = "https://i.ibb.co/YTYGn5qV/logo.png"


def header_home():

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Titan+One&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');
        </style>

        <div style="
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            margin-top:15px;
            margin-bottom:35px;
        ">

            <img
                src="{LOGO_URL}"
                style="
                    height:110px;
                    margin-bottom:12px;
                    filter:drop-shadow(0px 8px 16px rgba(0,0,0,.25));
                "
            />

            <h1 style="
                font-family:'Titan One',cursive;
                color:#FFFFFF;
                font-size:72px;
                line-height:.9;
                margin:0;
                letter-spacing:2px;
                text-align:center;
            ">
                SNAP<br>CLASS
            </h1>

            <p style="
                margin-top:16px;
                color:#E5E7EB;
                font-size:18px;
                font-family:'Outfit',sans-serif;
                font-weight:500;
            ">
                AI Powered Smart Attendance System
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


def header_dashboard():

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Titan+One&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');
        </style>

        <div style="
            display:flex;
            align-items:center;
            gap:16px;
            margin-bottom:10px;
        ">

            <img
                src="{LOGO_URL}"
                style="
                    height:72px;
                    filter:drop-shadow(0px 5px 12px rgba(0,0,0,.18));
                "
            />

            <div>

                <h2 style="
                    font-family:'Titan One',cursive;
                    color:#5865F2;
                    font-size:38px;
                    line-height:.9;
                    margin:0;
                ">
                    SNAP<br>CLASS
                </h2>

                <span style="
                    font-size:14px;
                    color:#6B7280;
                    font-family:'Outfit',sans-serif;
                ">
                    AI Attendance Management
                </span>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )