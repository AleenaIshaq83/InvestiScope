import streamlit as st
import home
import analysis
import risk
import result


# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="InvestiScope",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ================= PROFESSIONAL THEME =================

st.markdown("""
<style>

/* MAIN BACKGROUND */

.stApp {
    background-color: #F7F8FD !important;
    color: #101C3A !important;
}

/* SIDEBAR BACKGROUND */

[data-testid="stSidebar"] {
    background-color: #0B1738 !important;
}

/* SIDEBAR CONTENT */

[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    height: 100vh;
}

[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding-bottom: 100px !important;
}

/* SIDEBAR GENERAL TEXT */

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* RADIO GROUP SPACING */

[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 12px !important;
}

/* ALL RADIO OPTIONS */

[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: transparent !important;
    border-radius: 9px !important;
    padding: 9px 12px !important;
    transition: background-color 0.2s ease;
}

/* RADIO TEXT - FORCE WHITE */

[data-testid="stSidebar"] div[role="radiogroup"] label p,
[data-testid="stSidebar"] div[role="radiogroup"] label span,
[data-testid="stSidebar"] div[role="radiogroup"] label div {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* SELECTED RADIO OPTION */

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background-color: #7770D8 !important;
    border: 1px solid #A78BFA !important;
    border-radius: 9px !important;
}

/* SELECTED RADIO TEXT */

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p,
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) span,
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) div {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 800 !important;
}

/* RADIO CIRCLE */

[data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
    color: #FFFFFF !important;
}

/* SIDEBAR FOOTER */

[data-testid="stSidebar"] .sidebar-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 21rem;
    box-sizing: border-box;
    text-align: center;
    background-color: #0B1738;
    padding: 12px 8px;
    border-top: 1px solid #394866;
    z-index: 9999;
}

.sidebar-footer p {
    margin: 5px 0;
}

/* GENERAL HEADINGS */

h1, h2, h3, h4 {
    color: #101C3A !important;
    font-weight: 750 !important;
}

/* BUTTONS */

.stButton > button {
    background-color: #7770D8 !important;
    color: #FFFFFF !important;
    border: none;
    border-radius: 9px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #5E56BE !important;
    color: #FFFFFF !important;
}

/* INPUT LABELS */

.stNumberInput label,
.stTextInput label,
.stSelectbox label,
.stSlider label {
    color: #101C3A !important;
    font-weight: 600 !important;
}

/* METRIC CARDS */

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E4E5F2;
    border-radius: 13px;
    padding: 15px;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: #101C3A !important;
}

/* DATAFRAMES */

[data-testid="stDataFrame"] {
    background: #FFFFFF;
    border-radius: 10px;
}

/* DIVIDER */

hr {
    border-color: #DADCF0;
}

/* HIDE DEFAULT FOOTER */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ================= SIDEBAR =================

with st.sidebar:

    # BRAND LOGO

    st.markdown(
        "<div style='text-align:center; font-size:48px;'>📊</div>",
        unsafe_allow_html=True
    )

    # BRAND NAME

    st.markdown(
        "<h1 style='color:#FFFFFF !important; "
        "font-size:27px !important; font-weight:800 !important; "
        "text-align:center; margin:5px 0;'>"
        "InvestiScope</h1>",
        unsafe_allow_html=True
    )

    # TAGLINE

    st.markdown(
        "<p style='color:#DAD8FF !important; "
        "font-size:12px; text-align:center;'>"
        "Invest Smart. Grow Faster.</p>",
        unsafe_allow_html=True
    )

    st.divider()

    # NAVIGATION MENU

    page = st.radio(
        "MAIN MENU",
        [
            "Home Dashboard",
            "Financial Analysis",
            "Risk Assessment",
            "Investment Results"
        ],
        label_visibility="visible",
        key="main_navigation"
    )

    # SIDEBAR FOOTER

    st.markdown("""
    <div class="sidebar-footer">
        <p style="color:#DAD8FF !important; font-size:12px;">
            Your Financial Intelligence Partner
        </p>
        <p style="color:#FFFFFF !important; font-size:12px;
                  font-weight:600;">
            InvestiScope © 2026
        </p>
    </div>
    """, unsafe_allow_html=True)


# ================= PAGE NAVIGATION =================

if page == "Home Dashboard":

    home.show_home()

elif page == "Financial Analysis":

    analysis.show_analysis()

elif page == "Risk Assessment":

    risk.show_risk()

elif page == "Investment Results":

    result.show_result()