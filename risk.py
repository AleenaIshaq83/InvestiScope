import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def show_risk():

    # =====================================
    # NAVY, WHITE AND LIGHT LAVENDER THEME
    # =====================================

    st.markdown("""
    <style>

    .risk-header {
        background-color: #0B1738;
        padding: 25px;
        border-radius: 14px;
        margin-bottom: 22px;
    }

    .risk-header h1 {
        color: #FFFFFF !important;
        margin: 0;
        font-size: 30px;
    }

    .risk-header p {
        color: #E5E1FF !important;
        margin-top: 8px;
    }

    .risk-card {
        background-color: #FFFFFF;
        padding: 18px;
        border-radius: 13px;
        border: 1px solid #E2E5F0;
        border-bottom: 4px solid #A99FEA;
        min-height: 110px;
    }

    .risk-label {
        color: #34415D !important;
        font-size: 14px;
        font-weight: 600;
    }

    .risk-value {
        color: #101C3A !important;
        font-size: 25px;
        font-weight: 800;
        margin-top: 10px;
    }

    .risk-section {
        background-color: #0B1738;
        color: #FFFFFF !important;
        padding: 13px 16px;
        border-radius: 10px 10px 0 0;
        font-size: 16px;
        font-weight: 700;
    }

    .risk-insight {
        background-color: #0B1738;
        color: #FFFFFF !important;
        padding: 20px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
        line-height: 1.6;
        margin-top: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

    # =====================================
    # PAGE HEADER
    # =====================================

    st.markdown("""
    <div class="risk-header">
        <h1>Risk Assessment</h1>
        <p>Investment Risk Evaluation & Performance Monitoring</p>
    </div>
    """, unsafe_allow_html=True)

    # =====================================
    # RISK INPUTS
    # =====================================

    st.markdown("## Enter Investment Risk Factors")

    c1, c2 = st.columns(2)

    with c1:

        market_risk = st.slider(
            "Market Risk",
            0, 100, 45
        )

        financial_risk = st.slider(
            "Financial Risk",
            0, 100, 35
        )

        business_risk = st.slider(
            "Business Risk",
            0, 100, 40
        )

    with c2:

        liquidity_risk = st.slider(
            "Liquidity Risk",
            0, 100, 30
        )

        operational_risk = st.slider(
            "Operational Risk",
            0, 100, 35
        )

        economic_risk = st.slider(
            "Economic Risk",
            0, 100, 45
        )

    # =====================================
    # RISK CALCULATION
    # =====================================

    factors = {
        "Market Risk": market_risk,
        "Financial Risk": financial_risk,
        "Business Risk": business_risk,
        "Liquidity Risk": liquidity_risk,
        "Operational Risk": operational_risk,
        "Economic Risk": economic_risk
    }

    score = sum(factors.values()) / len(factors)

    if score < 35:

        level = "Low Risk"
        risk_color = "#16866E"

    elif score < 65:

        level = "Moderate Risk"
        risk_color = "#A17A18"

    else:

        level = "High Risk"
        risk_color = "#C04455"

    # =====================================
    # SAVE RISK DATA FOR RESULTS PAGE
    # =====================================

    st.session_state["risk_data"] = {
        "risk_score": score,
        "risk_level": level,
        "risk_factors": factors
    }

    # =====================================
    # KPI CARDS
    # =====================================

    st.markdown("## Risk Overview")

    a, b, c = st.columns(3)

    with a:

        st.markdown(f"""
        <div class="risk-card">
            <div class="risk-label">Overall Risk Score</div>
            <div class="risk-value">{score:.1f}/100</div>
        </div>
        """, unsafe_allow_html=True)

    with b:

        st.markdown(f"""
        <div class="risk-card">
            <div class="risk-label">Risk Classification</div>
            <div class="risk-value" style="color:{risk_color} !important;">
                {level}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c:

        st.markdown("""
        <div class="risk-card">
            <div class="risk-label">Risk Factors</div>
            <div class="risk-value">6 Factors</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # =====================================
    # GAUGE AND BAR CHART
    # =====================================

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="risk-section">Overall Risk Gauge</div>',
            unsafe_allow_html=True
        )

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                number={
                    "font": {
                        "color": "#101C3A",
                        "size": 35
                    }
                },
                gauge={
                    "axis": {
                        "range": [0, 100],
                        "tickfont": {
                            "color": "#101C3A"
                        }
                    },
                    "bar": {
                        "color": "#101C3A"
                    },
                    "steps": [
                        {
                            "range": [0, 35],
                            "color": "#CDEDE3"
                        },
                        {
                            "range": [35, 65],
                            "color": "#F3E7C4"
                        },
                        {
                            "range": [65, 100],
                            "color": "#F4D6DC"
                        }
                    ]
                }
            )
        )

        gauge.update_layout(
            height=320,
            paper_bgcolor="#FFFFFF",
            font=dict(color="#101C3A"),
            margin=dict(l=20, r=20, t=35, b=15)
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

    with right:

        st.markdown(
            '<div class="risk-section">Risk Factor Analysis</div>',
            unsafe_allow_html=True
        )

        bar = go.Figure(
            go.Bar(
                x=list(factors.values()),
                y=list(factors.keys()),
                orientation="h",
                marker_color=[
                    "#101C3A",
                    "#8175D8",
                    "#A99FEA",
                    "#C7BFF0",
                    "#6C78A0",
                    "#B5A8E8"
                ],
                text=list(factors.values()),
                textposition="outside",
                textfont=dict(
                    color="#101C3A",
                    size=12
                )
            )
        )

        bar.update_layout(
            height=320,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(
                color="#101C3A",
                size=12
            ),
            xaxis=dict(
                title="Risk Score",
                range=[0, 115],
                tickfont=dict(color="#101C3A"),
                gridcolor="#E8E9F1"
            ),
            yaxis=dict(
                tickfont=dict(color="#101C3A")
            ),
            margin=dict(l=15, r=35, t=25, b=25)
        )

        st.plotly_chart(
            bar,
            use_container_width=True
        )

    # =====================================
    # RISK FACTORS TABLE
    # =====================================

    st.markdown("## Risk Factors Summary")

    df = pd.DataFrame({
        "Risk Factor": list(factors.keys()),
        "Risk Score": list(factors.values()),
        "Classification": [
            "Low" if value < 35
            else "Moderate" if value < 65
            else "High"
            for value in factors.values()
        ]
    })

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # =====================================
    # RISK INSIGHTS
    # =====================================

    st.markdown("## Risk Insights")

    if score < 35:

        message = (
            "The entered factors indicate a relatively low risk profile. "
            "Continue monitoring the investment conditions."
        )

    elif score < 65:

        message = (
            "The entered factors indicate a moderate risk profile. "
            "Monitor higher-scoring factors and review them regularly."
        )

    else:

        message = (
            "The entered factors indicate elevated risk. "
            "Carefully review the major risk sources before making decisions."
        )

    st.markdown(
        f'<div class="risk-insight">{message}</div>',
        unsafe_allow_html=True
    )

    # =====================================
    # FOOTER
    # =====================================

    st.caption(
        "InvestiScope | Educational risk-scoring model based on "
        "user-entered values. This is not a validated prediction "
        "of actual investment losses."
    )