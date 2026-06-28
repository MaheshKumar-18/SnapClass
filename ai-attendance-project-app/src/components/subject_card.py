import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):

    total = 0
    attended = 0

    if stats:
        total = stats[0][2]
        attended = stats[1][2]

    percentage = round((attended / total) * 100) if total else 0

    if percentage >= 75:
        color = "#22C55E"
        emoji = "🟢"
    elif percentage >= 50:
        color = "#F59E0B"
        emoji = "🟡"
    else:
        color = "#EF4444"
        emoji = "🔴"

    with st.container(border=True):

        st.markdown(f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">
            <div>
                <h2 style="
                    margin:0;
                    color:#1E293B;
                    font-weight:700;
                ">
                    📘 {name}
                </h2>

                <div style="
                    margin-top:6px;
                    color:#64748B;
                    font-size:15px;
                ">
                    <span style="
                        background:#EEF2FF;
                        color:#5865F2;
                        padding:4px 10px;
                        border-radius:8px;
                        font-weight:600;
                        margin-right:8px;
                    ">
                        {code}
                    </span>

                    <span style="
                        background:#F3F4F6;
                        padding:4px 10px;
                        border-radius:8px;
                        font-weight:600;
                    ">
                        Section {section}
                    </span>
                </div>
            </div>

            <div style="
                background:{color};
                color:white;
                padding:10px 18px;
                border-radius:14px;
                font-weight:700;
                font-size:18px;
            ">
                {emoji} {percentage}%
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "📅 Total Classes",
                total,
            )

        with c2:
            st.metric(
                "✅ Attended",
                attended,
            )

        progress = percentage / 100

        st.progress(progress)

        st.caption(f"Attendance Progress • {percentage}%")

        st.divider()

        if footer_callback:
            footer_callback()