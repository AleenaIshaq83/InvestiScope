import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ==================================================
# 1. COLOR THEME
# ==================================================

NAVY = "#101F3C"
DARK_BLUE = "#172D50"
LAVENDER = "#A78BFA"
PURPLE = "#7C3AED"
WHITE = "#FFFFFF"


# ==================================================
# 2. PAGE STYLING
# ==================================================

def apply_page_style():

    st.markdown("""
    <style>

    .analysis-header {
        background: linear-gradient(120deg, #101F3C, #172D50);
        padding: 25px;
        border-radius: 14px;
        margin-bottom: 22px;
    }

    .analysis-header h1 {
        color: #FFFFFF !important;
        font-size: 30px;
        margin: 0;
    }

    .analysis-header p {
        color: #E5E1FF !important;
        margin-top: 8px;
    }

    .section-heading {
        color: #101F3C !important;
        font-size: 21px;
        font-weight: 750;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E5F0;
        border-bottom: 4px solid #A78BFA;
        border-radius: 13px;
        padding: 17px;
        min-height: 115px;
    }

    .metric-label {
        color: #34415D !important;
        font-size: 14px;
        font-weight: 600;
    }

    .metric-value {
        color: #101F3C !important;
        font-size: 23px;
        font-weight: 800;
        margin-top: 10px;
    }

    .download-heading {
        background: #FFFFFF;
        color: #101F3C !important;
        font-size: 20px;
        font-weight: 750;
        padding: 12px 0;
    }

    .stDownloadButton button {
        background-color: #101F3C !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
    }

    .stDownloadButton button p {
        color: #FFFFFF !important;
    }

    </style>
    """, unsafe_allow_html=True)


# ==================================================
# 3. FINANCIAL CALCULATIONS
# ==================================================

def calculate_npv(investment, cash_flows, rate):

    return sum(
        cf / ((1 + rate) ** year)
        for year, cf in enumerate(cash_flows, start=1)
    ) - investment


def calculate_roi(investment, cash_flows):

    if investment <= 0:
        return 0

    total_profit = sum(cash_flows) - investment

    return (total_profit / investment) * 100


def calculate_payback(investment, cash_flows):

    cumulative = 0

    for year, cf in enumerate(cash_flows, start=1):

        previous = cumulative
        cumulative += cf

        if cumulative >= investment:

            if cf <= 0:
                return float(year)

            return (year - 1) + (
                (investment - previous) / cf
            )

    return None


def calculate_irr(investment, cash_flows):

    flows = [-investment] + cash_flows

    def npv_at(rate):

        return sum(
            cf / ((1 + rate) ** year)
            for year, cf in enumerate(flows)
        )

    low = -0.99
    high = 10.0

    if npv_at(low) * npv_at(high) > 0:
        return None

    for _ in range(200):

        mid = (low + high) / 2
        value = npv_at(mid)

        if abs(value) < 0.000001:
            return mid

        if npv_at(low) * value < 0:
            high = mid
        else:
            low = mid

    return (low + high) / 2


# ==================================================
# 4. GRAPH STYLING
# ==================================================

def style_graph(fig, title):

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(color=NAVY, size=18)
        ),
        height=350,
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(color=NAVY),
        margin=dict(l=25, r=25, t=55, b=35),
        xaxis=dict(
            tickfont=dict(color=NAVY),
            gridcolor="#E8E9F1"
        ),
        yaxis=dict(
            tickfont=dict(color=NAVY),
            gridcolor="#E8E9F1"
        )
    )

    return fig


# ==================================================
# 5. MAIN FINANCIAL ANALYSIS PAGE
# ==================================================

def show_analysis():

    apply_page_style()

    # PAGE HEADER

    st.markdown("""
    <div class="analysis-header">
        <h1>Investment Analysis</h1>
        <p>
        Financial Feasibility, Investment Valuation
        & Performance Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    # INVESTMENT DETAILS

    st.markdown(
        '<div class="section-heading">Investment Details</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        currency = st.selectbox(
            "Select Currency",
            ["PKR", "USD", "GBP", "EUR", "AED", "SAR"]
        )

    with c2:

        investment = st.number_input(
            "Initial Investment",
            min_value=1,
            value=500000,
            step=10000
        )

    with c3:

        rate_percent = st.number_input(
            "Discount Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.5
        )

    duration = st.number_input(
        "Project Duration (Years)",
        min_value=1,
        max_value=30,
        value=5,
        step=1
    )

    rate = rate_percent / 100

    # ANNUAL CASH FLOWS

    st.markdown(
        '<div class="section-heading">Annual Cash Inflows</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Enter the expected cash inflow for each project year."
    )

    cash_flows = []

    left, right = st.columns(2)

    for year in range(1, int(duration) + 1):

        target_col = left if year % 2 == 1 else right

        with target_col:

            inflow = st.number_input(
                f"Year {year} Cash Inflow ({currency})",
                min_value=0,
                value=150000,
                step=10000,
                key=f"analysis_cashflow_{year}"
            )

            cash_flows.append(inflow)

    # CALCULATIONS

    npv = calculate_npv(
        investment,
        cash_flows,
        rate
    )

    total_inflow = sum(cash_flows)

    total_profit = total_inflow - investment

    roi = calculate_roi(
        investment,
        cash_flows
    )

    payback = calculate_payback(
        investment,
        cash_flows
    )

    irr = calculate_irr(
        investment,
        cash_flows
    )

    payback_text = (
        f"{payback:.2f} Years"
        if payback is not None
        else "Not Recovered"
    )

    irr_text = (
        f"{irr * 100:.2f}%"
        if irr is not None
        else "N/A"
    )

    # SAVE DATA FOR OTHER PAGES

    st.session_state["financial_data"] = {
        "currency": currency,
        "investment": investment,
        "discount_rate": rate_percent,
        "duration": int(duration),
        "cash_flows": cash_flows,
        "npv": npv,
        "total_inflow": total_inflow,
        "total_profit": total_profit,
        "roi": roi,
        "irr": irr,
        "payback": payback
    }

    # KPI CARDS

    st.markdown(
        '<div class="section-heading">Financial Performance</div>',
        unsafe_allow_html=True
    )

    symbol = currency

    cards = [
        ("Net Present Value", f"{symbol} {npv:,.2f}"),
        ("Total Cash Inflow", f"{symbol} {total_inflow:,.2f}"),
        ("Total Profit", f"{symbol} {total_profit:,.2f}"),
        ("Return on Investment", f"{roi:.2f}%"),
        ("Internal Rate of Return", irr_text),
        ("Payback Period", payback_text)
    ]

    columns = st.columns(3)

    for index, (label, value) in enumerate(cards):

        with columns[index % 3]:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    # CASH FLOW TABLE

    st.markdown(
        '<div class="section-heading">Cash Flow Statement</div>',
        unsafe_allow_html=True
    )

    rows = []

    for year, cf in enumerate(cash_flows, start=1):

        discount_factor = 1 / ((1 + rate) ** year)

        present_value = cf * discount_factor

        rows.append({
            "Year": year,
            f"Cash Flow ({currency})": cf,
            "Discount Factor": discount_factor,
            f"Present Value ({currency})": present_value
        })

    df = pd.DataFrame(rows)

    st.dataframe(
        df.style.format({
            f"Cash Flow ({currency})": "{:,.2f}",
            "Discount Factor": "{:.4f}",
            f"Present Value ({currency})": "{:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    # GRAPH DATA

    years_list = list(range(1, int(duration) + 1))

    cumulative_values = []
    running_total = -investment

    for cf in cash_flows:

        running_total += cf
        cumulative_values.append(running_total)

    # ANNUAL CASH FLOW GRAPH

    left, right = st.columns(2)

    with left:

        fig1 = go.Figure()

        fig1.add_trace(go.Bar(
            x=years_list,
            y=cash_flows,
            marker_color="#887BDD",
            text=cash_flows,
            textposition="outside",
            name="Annual Cash Flow"
        ))

        fig1 = style_graph(
            fig1,
            "Annual Cash Flow"
        )

        fig1.update_xaxes(title="Year")
        fig1.update_yaxes(title=currency)

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # CUMULATIVE CASH POSITION

    with right:

        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(
            x=years_list,
            y=cumulative_values,
            mode="lines+markers",
            line=dict(
                color="#887BDD",
                width=4
            ),
            marker=dict(size=9),
            name="Cumulative Position"
        ))

        fig2.add_hline(
            y=0,
            line_dash="dash",
            line_color=NAVY
        )

        fig2 = style_graph(
            fig2,
            "Cumulative Cash Position"
        )

        fig2.update_xaxes(title="Year")
        fig2.update_yaxes(title=currency)

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # INVESTMENT PERFORMANCE COMPARISON

    st.markdown(
        '<div class="section-heading">Investment Performance Comparison</div>',
        unsafe_allow_html=True
    )

    fig3 = go.Figure()

    fig3.add_trace(go.Bar(
        x=["Initial Investment", "Total Inflow", "Net Profit"],
        y=[investment, total_inflow, total_profit],
        marker_color=[
            "#101F3C",
            "#887BDD",
            "#A78BFA"
        ],
        text=[
            f"{investment:,.0f}",
            f"{total_inflow:,.0f}",
            f"{total_profit:,.0f}"
        ],
        textposition="outside"
    ))

    fig3 = style_graph(
        fig3,
        "Investment Performance"
    )

    fig3.update_yaxes(title=currency)

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # INVESTMENT DECISION

    st.markdown(
        '<div class="section-heading">Investment Decision</div>',
        unsafe_allow_html=True
    )

    if npv > 0:

        st.success(
            "Positive NPV: The project has positive estimated "
            "value at the selected discount rate."
        )

    elif npv < 0:

        st.warning(
            "Negative NPV: The project has negative estimated "
            "value at the selected discount rate."
        )

    else:

        st.info(
            "NPV is zero: Present value equals the initial investment."
        )

    # FINANCIAL SUMMARY

    summary = pd.DataFrame({
        "Financial Indicator": [
            "Initial Investment",
            "Total Cash Inflow",
            "Total Profit",
            "Net Present Value",
            "ROI",
            "IRR",
            "Payback Period"
        ],
        "Calculated Result": [
            f"{currency} {investment:,.2f}",
            f"{currency} {total_inflow:,.2f}",
            f"{currency} {total_profit:,.2f}",
            f"{currency} {npv:,.2f}",
            f"{roi:.2f}%",
            irr_text,
            payback_text
        ]
    })

    st.markdown(
        '<div class="section-heading">Financial Summary</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    # DOWNLOAD REPORT

    st.markdown(
        '<div class="download-heading">Download Financial Report</div>',
        unsafe_allow_html=True
    )

    csv_data = summary.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Financial Report (CSV)",
        data=csv_data,
        file_name="InvestiScope_Financial_Report.csv",
        mime="text/csv"
    )

    # FOOTER

    st.caption(
        "InvestiScope | Financial Investment Analysis System. "
        "Results are estimates based on entered assumptions "
        "and do not guarantee investment returns."
    )

# Do not call show_analysis() here.
# app.py should call analysis.show_analysis()