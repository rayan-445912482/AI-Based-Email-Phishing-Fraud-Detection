import streamlit as st

from src.config import APP_SUBTITLE, APP_TITLE, APP_VERSION, ASSETS_DIR


def _load_css():
    css_path = ASSETS_DIR / "style.css"
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

_load_css()

with st.sidebar:
    logo_path = ASSETS_DIR / "logo.svg"
    if logo_path.exists():
        st.markdown(
            f'<div style="text-align:center;padding:1rem 0;">'
            f'{logo_path.read_text(encoding="utf-8")}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div style="text-align:center;margin-bottom:1.5rem;">
            <h2 style="margin:0;color:#0f172a;font-size:1.1rem;">{APP_TITLE}</h2>
            <p style="margin:0;color:#64748b;font-size:0.75rem;">{APP_SUBTITLE}</p>
            <p style="margin:0;color:#94a3b8;font-size:0.7rem;">v{APP_VERSION}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🔍 Analyzer",
            "📊 Dashboard",
            "⚖️ Comparison",
            "🐞 Error Analysis",
            "👥 Members & Tasks",
            "⚙️ Settings",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:0.75rem;color:#94a3b8;line-height:1.5;">
            <strong>⚠️ Security Notice</strong><br>
            Do not enter passwords, confidential messages,
            or sensitive personal information.
        </div>
        """,
        unsafe_allow_html=True,
    )


if page == "🏠 Home":
    from views.home import render
    render()
elif page == "🔍 Analyzer":
    from views.analyzer import render
    render()
elif page == "📊 Dashboard":
    from views.dashboard import render
    render()
elif page == "⚖️ Comparison":
    from views.comparison import render
    render()
elif page == "🐞 Error Analysis":
    from views.errors import render
    render()
elif page == "👥 Members & Tasks":
    from views.members import render
    render()
elif page == "⚙️ Settings":
    from views.settings import render
    render()
