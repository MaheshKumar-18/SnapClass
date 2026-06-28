import streamlit as st


def footer_home():

    st.markdown("""
    <div style="
        margin-top:50px;
        padding:20px 0;
        text-align:center;
        font-family:'Outfit',sans-serif;
        color:#E5E7EB;
        font-size:15px;
        border-top:1px solid rgba(255,255,255,.15);
    ">

        <div style="
            font-weight:600;
            letter-spacing:.5px;
        ">
            ⚡ Developed by <span style="color:#FFFFFF;">Mahesh Kumar</span>
        </div>

        <div style="
            margin-top:8px;
            font-size:13px;
            color:#BFC5D2;
        ">
            SnapClass • AI Powered Smart Attendance System
        </div>

    </div>
    """, unsafe_allow_html=True)


def footer_dashboard():

    st.markdown("""
    <div style="
        margin-top:50px;
        padding:20px 0;
        text-align:center;
        font-family:'Outfit',sans-serif;
        color:#6B7280;
        font-size:15px;
        border-top:1px solid #E5E7EB;
    ">

        <div style="
            font-weight:600;
        ">
            ⚡ Developed by <span style="color:#5865F2;">Mahesh Kumar</span>
        </div>

        <div style="
            margin-top:8px;
            font-size:13px;
            color:#9CA3AF;
        ">
            SnapClass • AI Powered Smart Attendance System
        </div>

    </div>
    """, unsafe_allow_html=True)