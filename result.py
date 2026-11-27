import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ==================================================
# COLORS
# ==================================================

NAVY = "#101F3C"
DARK_BLUE = "#172D50"
LAVENDER = "#A78BFA"
PURPLE = "#7770D8"
WHITE = "#FFFFFF"
LIGHT_BG = "#F7F8FD"


# ==================================================
# PAGE DESIGN
# ==================================================

def apply_result_style():

    st.markdown("""
    <style>

    .result-header {
        background: linear-gradient(120deg, #0B1738, #172D50);
        padding: 28px;
        border-radius: 15px;
        margin-bottom: 25px;
    }

    .result-header h1 {
        color: #FFFFFF !important;
        font-size: 34px;
        margin-bottom: 8px;
    }

    .result-header p {
        color: #E5E7EB !important;
        font-size: 16px;
    }

    .section-heading {
        color: #101F3C;
        font-size: 23px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .metric-card {
        background: #FFFFFF;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 7px rgba(0,0,0,0.04);
    }

    .metric-label {
        color: #64748B;
        font-size: 14px;
    }

    .metric-value {
        color: #101F3C;
        font-size: 25px;
        font-weight: 700;
        margin-top: 7px;
    }

    .result-footer {
        text-align: center;
        color: #64748B;
        padding: 20px;
        margin-top: 35px;
        border-top: 1px solid #E5E7EB;
    }

    </style>
    """, unsafe_allow_html=True)


# ==================================================
# METRIC CARD
# ==================================================

def show_metric(title, value):

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# CHART DESIGN
# ==================================================

def style_graph(fig, title):

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(color=NAVY, size=20)
        ),
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(color=NAVY, size=13),
        xaxis=dict(
            title_font=dict(color=NAVY),
            tickfont=dict(color=NAVY),
            gridcolor="#E5E7EB"
        ),
        yaxis=dict(
            title_font=dict(color=NAVY),
            tickfont=dict(color=NAVY),
            gridcolor="#E5E7EB"
        ),
        legend=dict(
            font=dict(color=NAVY)
        ),
        margin=dict(l=25, r=25, t=60, b=25)
    )

    return fig


# ==================================================
# RESULT PAGE
# ==================================================

def show_result():

    apply_result_style()

    st.markdown("""
    <div class="result-header">
        <h1>Investment Results & Evaluation</h1>
        <p>Complete financial performance and investment risk overview</p>
    </div>
    """, unsafe_allow_html=True)

    # Get data from other pages
    financial_data = st.session_state.get("financial_data")
    risk_data = st.session_state.get("risk_data")

    # ==================================================
    # FINANCIAL RESULTS
    # ==================================================

    st.markdown(
        '<div class="section-heading">Financial Analysis Results</div>',
        unsafe_allow_html=True
    )

    if not financial_data:

        st.info(
            "Please complete Financial Analysis first "
            "to view your financial results."
        )

    else:

        currency = financial_data.get("currency", "PKR")
        investment = financial_data.get("investment", 0)
        discount_rate = financial_data.get("discount_rate", 0)
        duration = financial_data.get("duration", 0)
        cash_flows = financial_data.get("cash_flows", [])

        npv = financial_data.get("npv", 0)
        total_inflow = financial_data.get("total_inflow", 0)
        total_profit = financial_data.get("total_profit", 0)
        roi = financial_data.get("roi", 0)
        irr = financial_data.get("irr", 0)
        payback = financial_data.get("payback", 0)

        # Financial KPI cards
        col1, col2, col3 = st.columns(3)

        with col1:
            show_metric("Initial Investment",
                        f"{currency} {investment:,.2f}")

        with col2:
            show_metric("Net Present Value",
                        f"{currency} {npv:,.2f}")

        with col3:
            show_metric("Return on Investment",
                        f"{roi:.2f}%")

        col4, col5, col6 = st.columns(3)

        with col4:
            show_metric("Internal Rate of Return",
                        f"{irr:.2f}%")

        with col5:
            show_metric("Total Cash Inflow",
                        f"{currency} {total_inflow:,.2f}")

        with col6:
            show_metric("Payback Period",
                        f"{payback:.2f} Years")

        st.markdown(
            '<div class="section-heading">Cash Flow Summary</div>',
            unsafe_allow_html=True
        )

        if cash_flows:

            cash_flow_table = pd.DataFrame({
                "Year": list(range(1, len(cash_flows) + 1)),
                "Annual Cash Inflow": cash_flows
            })

            cash_flow_table["Cumulative Cash Inflow"] = (
                cash_flow_table["Annual Cash Inflow"].cumsum()
            )

            st.dataframe(
                cash_flow_table,
                use_container_width=True,
                hide_index=True
            )

            # Annual cash flow chart
            fig1 = go.Figure()

            fig1.add_trace(go.Bar(
                x=cash_flow_table["Year"],
                y=cash_flow_table["Annual Cash Inflow"],
                name="Annual Cash Inflow",
                marker_color=LAVENDER
            ))

            fig1.update_layout(
                xaxis_title="Year",
                yaxis_title=f"Cash Inflow ({currency})"
            )

            st.plotly_chart(
                style_graph(fig1, "Annual Cash Flow"),
                use_container_width=True
            )

            # Cumulative cash flow chart
            cumulative = [-investment]

            running_total = -investment

            for amount in cash_flows:
                running_total += amount
                cumulative.append(running_total)

            years = list(range(0, len(cash_flows) + 1))

            fig2 = go.Figure()

            fig2.add_trace(go.Scatter(
                x=years,
                y=cumulative,
                mode="lines+markers",
                name="Cumulative Cash Position",
                line=dict(color=PURPLE, width=3)
            ))

            fig2.add_hline(
                y=0,
                line_dash="dash",
                line_color="#64748B"
            )

            fig2.update_layout(
                xaxis_title="Year",
                yaxis_title=f"Cash Position ({currency})"
            )

            st.plotly_chart(
                style_graph(fig2, "Cumulative Cash Position"),
                use_container_width=True
            )

        # Investment decision
        st.markdown(
            '<div class="section-heading">Investment Evaluation</div>',
            unsafe_allow_html=True
        )

        if npv > 0:
            st.success(
                "Positive NPV: The investment is financially attractive "
                "based on the entered cash flows and discount rate."
            )

        elif npv < 0:
            st.warning(
                "Negative NPV: The investment may not meet the required "
                "return at the selected discount rate."
            )

        else:
            st.info(
                "NPV is zero: The investment is expected to break even "
                "in present-value terms."
            )

        st.write(f"**Total Profit:** {currency} {total_profit:,.2f}")
        st.write(f"**Discount Rate:** {discount_rate:.2f}%")
        st.write(f"**Project Duration:** {duration} Years")

    # ==================================================
    # RISK ASSESSMENT RESULTS
    # ==================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-heading">Risk Assessment Results</div>',
        unsafe_allow_html=True
    )

    if not risk_data:

        st.info(
            "Please complete Risk Assessment first "
            "to view your risk results."
        )

    else:

        risk_score = risk_data.get("risk_score", 0)
        risk_level = risk_data.get("risk_level", "Not Available")
        risk_factors = risk_data.get("risk_factors", {})

        col1, col2 = st.columns(2)

        with col1:
            show_metric(
                "Overall Risk Score",
                f"{risk_score:.1f}/100"
            )

        with col2:
            show_metric(
                "Risk Classification",
                risk_level
            )

        # Risk gauge
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={
                "text": "Overall Investment Risk",
                "font": {"color": NAVY}
            },
            number={"font": {"color": NAVY}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickfont": {"color": NAVY}
                },
                "bar": {"color": PURPLE},
                "steps": [
                    {
                        "range": [0, 35],
                        "color": "#D1FAE5"
                    },
                    {
                        "range": [35, 65],
                        "color": "#FEF3C7"
                    },
                    {
                        "range": [65, 100],
                        "color": "#FEE2E2"
                    }
                ]
            }
        ))

        fig3.update_layout(
            paper_bgcolor=WHITE,
            font=dict(color=NAVY),
            height=350
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        # Risk factor table and chart
        if isinstance(risk_factors, dict) and risk_factors:

            risk_table = pd.DataFrame({
                "Risk Factor": list(risk_factors.keys()),
                "Risk Score": list(risk_factors.values())
            })

            st.markdown(
                '<div class="section-heading">Risk Factors Breakdown</div>',
                unsafe_allow_html=True
            )

            st.dataframe(
                risk_table,
                use_container_width=True,
                hide_index=True
            )

            fig4 = go.Figure()

            fig4.add_trace(go.Bar(
                x=risk_table["Risk Factor"],
                y=risk_table["Risk Score"],
                marker_color=LAVENDER,
                name="Risk Score"
            ))

            fig4.update_layout(
                xaxis_title="Risk Factors",
                yaxis_title="Risk Score"
            )

            st.plotly_chart(
                style_graph(fig4, "Individual Risk Factors"),
                use_container_width=True
            )

        elif isinstance(risk_factors, list) and risk_factors:

            st.markdown(
                '<div class="section-heading">Risk Factors Breakdown</div>',
                unsafe_allow_html=True
            )

            risk_table = pd.DataFrame(risk_factors)

            st.dataframe(
                risk_table,
                use_container_width=True,
                hide_index=True
            )

    # ==================================================
    # FINAL SUMMARY
    # ==================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-heading">Overall Project Summary</div>',
        unsafe_allow_html=True
    )

    if financial_data and risk_data:

        st.success(
            "Financial Analysis and Risk Assessment data "
            "are both available. Your investment evaluation "
            "includes financial performance and risk information."
        )

    elif financial_data:

        st.info(
            "Financial results are available. Complete Risk "
            "Assessment to see the combined investment evaluation."
        )

    elif risk_data:

        st.info(
            "Risk results are available. Complete Financial "
            "Analysis to see the combined investment evaluation."
        )

    else:

        st.info(
            "Complete Financial Analysis and Risk Assessment "
            "to generate your overall investment results."
        )

    # ==================================================
    # FOOTER
    # ==================================================

    st.markdown("""
    <div class="result-footer">
        InvestiScope | Business Investment Feasibility Analyzer
        <br>
        Financial Analysis • Risk Assessment • Investment Evaluation
    </div>
    """, unsafe_allow_html=True)