import streamlit as st


def style_background_home():

    st.markdown("""
    <style>

    .stApp{
        background:#222222 !important;
    }

    .stApp div[data-testid="stColumn"]{
        background:#E0E3FF !important;
        padding:2.5rem !important;
        border-radius:28px !important;
        box-shadow:0 12px 35px rgba(0,0,0,.18);
        transition:.3s;
    }

    .stApp div[data-testid="stColumn"]:hover{
        transform:translateY(-5px);
    }

    </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():

    st.markdown("""
    <style>

    .stApp{
        background:#F5F7FB !important;
    }

    </style>
    """, unsafe_allow_html=True)


def style_base_layout():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Titan+One&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100;200;300;400;500;600;700;800&display=swap');

    /* Hide Streamlit UI */

    #MainMenu,
    footer,
    header{
        visibility:hidden;
    }

    .block-container{
        max-width:1200px;
        padding-top:1.2rem !important;
        padding-bottom:2rem !important;
    }

    html,
    body,
    [class*="css"]{
        font-family:'Outfit',sans-serif;
    }

    h1{
        font-family:'Titan One',cursive !important;
        color:#F8FAFC !important;
        font-size:3.8rem !important;
        margin-bottom:0rem !important;
    }

    h2{
        font-family:'Outfit',sans-serif !important;
        font-size:2rem !important;
        font-weight:700 !important;
        color:#1E293B !important;
    }

    h3{
        font-family:'Outfit',sans-serif !important;
        font-size:1.4rem !important;
        font-weight:700 !important;
        color:#1E293B !important;
    }

    p{
        font-family:'Outfit',sans-serif;
    }

    /* ---------------- Buttons ---------------- */

    .stButton > button{

        width:100%;
        height:48px;

        border-radius:14px;

        border:none;

        background:#5865F2;
        color:white;

        font-weight:600;
        font-size:15px;

        transition:.25s;

    }

    .stButton > button:hover{

        background:#4752C4;

        transform:translateY(-2px);

        box-shadow:0 12px 24px rgba(88,101,242,.35);

    }

    button[kind="secondary"]{

        background:#EB459E !important;
        color:white !important;

    }

    button[kind="secondary"]:hover{

        background:#D93B90 !important;

    }

    button[kind="tertiary"]{

        background:#EF4444 !important;
        color:white !important;

    }

    button[kind="tertiary"]:hover{

        background:#DC2626 !important;

    }

    /* ---------------- Inputs ---------------- */

    .stTextInput input,
    .stNumberInput input{

        border-radius:12px !important;

        border:1px solid #D7DCE5 !important;

        padding:.55rem !important;

    }

    .stSelectbox div{

        border-radius:12px;

    }

    textarea{

        border-radius:12px !important;

    }

    section[data-testid="stFileUploader"]{

        border-radius:14px;

    }

    /* ---------------- Metrics ---------------- */

    [data-testid="metric-container"]{

        background:white;

        border-radius:16px;

        border:1px solid #E5E7EB;

        padding:18px;

        box-shadow:0 4px 12px rgba(0,0,0,.05);

    }

    /* ---------------- Dialog ---------------- */

    [data-testid="stDialog"]{

        border-radius:22px;

    }

    /* ---------------- Divider ---------------- */

    hr{

        margin-top:1.2rem !important;
        margin-bottom:1.2rem !important;

    }

    </style>
    """, unsafe_allow_html=True)