import streamlit as st
import plotly.graph_objects as go


def show_home():

    # ================= DASHBOARD CSS =================
    st.markdown("""
    <style>
    .welcome-box {
        background: linear-gradient(110deg, #0B1738, #192B5C);
        padding: 25px;
        border-radius: 17px;
        margin-bottom: 22px;
    }

    .welcome-box h1 {
        color: white !important;
        font-size: 32px;
        margin-bottom: 5px;
    }

    .welcome-box p {
        color: #DCD9FF !important;
        font-size: 15px;
    }

    .kpi-card {
        background: white;
        border: 1px solid #E4E5F2;
        border-bottom: 4px solid #A99FEA;
        padding: 18px;
        border-radius: 14px;
        min-height: 125px;
        box-shadow: 0 3px 12px rgba(16,28,58,0.06);
    }

    .kpi-label {
        color: #536078 !important;
        font-size: 14px;
        font-weight: 600;
    }

    .kpi-value {
        color: #101C3A !important;
        font-size: 25px;
        font-weight: 800;
        margin-top: 10px;
    }

    .kpi-change {
        color: #16866E !important;
        font-size: 12px;
        margin-top: 7px;
        font-weight: 600;
    }

    .section-title {
        background: #0B1738;
        color: white !important;
        padding: 12px 16px;
        border-radius: 10px 10px 0 0;
        font-size: 17px;
        font-weight: 700;
        margin-top: 15px;
    }

    .white-panel {
        background: white;
        border: 1px solid #E5E5F0;
        border-radius: 0 0 12px 12px;
        padding: 15px;
    }

    .insight {
        background: #F0EEFF;
        border-left: 4px solid #8C82DF;
        padding: 12px;
        margin: 9px 0;
        border-radius: 8px;
        color: #101C3A !important;
        font-size: 13px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ================= COMMON GRAPH STYLE =================
    common_axis = dict(
        color="#101C3A",
        tickfont=dict(color="#101C3A", size=11),
        title_font=dict(color="#101C3A", size=12),
        showline=True,
        linecolor="#D5D8E5",
        zerolinecolor="#D5D8E5"
    )

    # ================= HEADER =================
    st.markdown("""
    <div class="welcome-box">
        <h1>Welcome to InvestiScope</h1>
        <p>Investment Intelligence & Risk Analytics System</p>
    </div>
    """, unsafe_allow_html=True)

    # ================= KPI CARDS =================
    st.markdown("### Financial Overview")

    c1, c2, c3, c4 = st.columns(4)

    kpis = [
        ("💰 TOTAL INVESTMENT", "Rs. 500,000", "Sample portfolio"),
        ("📈 EXPECTED RETURN", "Rs. 125,000", "Sample projection"),
        ("％ ROI", "25.00%", "Illustrative return"),
        ("🛡️ RISK LEVEL", "Moderate", "Sample assessment")
    ]

    for col, (label, value, change) in zip(
        [c1, c2, c3, c4], kpis
    ):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-change">{change}</div>
            </div>
            """, unsafe_allow_html=True)

    # ================= CHART DATA =================
    months = ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]

    investment = [60000, 78000, 93000, 110000, 120000, 125000]
    returns = [20000, 28000, 38000, 43000, 49000, 48000]

    # ================= GROWTH CHART =================
    left, right = st.columns([1.6, 1])

    with left:

        st.markdown(
            '<div class="section-title">📈 Investment Growth Overview</div>',
            unsafe_allow_html=True
        )

        fig1 = go.Figure()

        fig1.add_trace(go.Scatter(
            x=months,
            y=investment,
            name="Investment",
            mode="lines+markers",
            line=dict(color="#102653", width=4),
            marker=dict(size=8, color="#102653"),
            fill="tozeroy",
            fillcolor="rgba(16,38,83,0.08)"
        ))

        fig1.add_trace(go.Scatter(
            x=months,
            y=returns,
            name="Returns",
            mode="lines+markers",
            line=dict(color="#8175D8", width=4),
            marker=dict(size=8, color="#8175D8")
        ))

        fig1.update_layout(
            height=340,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(
                family="Arial",
                color="#101C3A",
                size=12
            ),
            margin=dict(l=15, r=15, t=30, b=15),
            legend=dict(
                orientation="h",
                y=1.12,
                font=dict(color="#101C3A", size=11)
            ),
            xaxis=dict(
                **common_axis,
                title="Month",
                showgrid=False
            ),
            yaxis=dict(
                **common_axis,
                title="Amount (PKR)",
                gridcolor="#E9EAF2"
            )
        )

        st.plotly_chart(fig1, use_container_width=True)

    # ================= DONUT CHART =================
    with right:

        st.markdown(
            '<div class="section-title">📊 Investment Distribution</div>',
            unsafe_allow_html=True
        )

        fig2 = go.Figure(go.Pie(
            labels=["Business", "Equipment", "Marketing", "Other"],
            values=[65, 20, 10, 5],
            hole=0.62,
            marker=dict(
                colors=["#102653", "#8578D8", "#B9AFE9", "#E5E1FA"]
            ),
            textinfo="percent",
            textfont=dict(
                color="#FFFFFF",
                size=13
            ),
            insidetextorientation="auto"
        ))

        fig2.update_layout(
            height=340,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(
                family="Arial",
                color="#101C3A",
                size=12
            ),
            showlegend=True,
            legend=dict(
                font=dict(color="#101C3A", size=11)
            ),
            margin=dict(l=10, r=10, t=25, b=10)
        )

        st.plotly_chart(fig2, use_container_width=True)

    # ================= LOWER SECTION =================
    a, b, c = st.columns([1.35, 1, 1.2])

    # ================= MONTHLY RETURNS =================
    with a:

        st.markdown(
            '<div class="section-title">📅 Monthly Returns</div>',
            unsafe_allow_html=True
        )

        fig3 = go.Figure(go.Bar(
            x=months,
            y=returns,
            marker=dict(
                color="#8175D8",
                line=dict(color="#6256B8", width=1)
            ),
            text=returns,
            textposition="outside",
            texttemplate="%{y:,.0f}",
            textfont=dict(
                color="#101C3A",
                size=11
            )
        ))

        fig3.update_layout(
            height=290,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(
                family="Arial",
                color="#101C3A",
                size=12
            ),
            margin=dict(l=10, r=10, t=35, b=10),
            xaxis=dict(
                **common_axis,
                showgrid=False
            ),
            yaxis=dict(
                **common_axis,
                title="Returns (PKR)",
                gridcolor="#ECECF3"
            )
        )

        st.plotly_chart(fig3, use_container_width=True)

    # ================= KEY METRICS =================
    with b:

        st.markdown(
            '<div class="section-title">🧮 Key Financial Metrics</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="white-panel">
            <p style="color:#101C3A;">↗ Net Profit
            <b style="float:right;color:#16866E;">Rs. 125,000</b></p>
            <hr>
            <p style="color:#101C3A;">％ Profit Margin
            <b style="float:right;color:#101C3A;">25.00%</b></p>
            <hr>
            <p style="color:#101C3A;">◷ Payback Period
            <b style="float:right;color:#101C3A;">2.8 Years</b></p>
            <hr>
            <p style="color:#101C3A;">★ NPV
            <b style="float:right;color:#101C3A;">Rs. 95,000</b></p>
        </div>
        """, unsafe_allow_html=True)

    # ================= QUICK INSIGHTS =================
    with c:

        st.markdown(
            '<div class="section-title">💡 Quick Insights</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="white-panel">
            <div class="insight">✓ Investment is showing positive sample returns.</div>
            <div class="insight">✓ Risk level is currently shown as moderate.</div>
            <div class="insight">✓ Review cash flows before making decisions.</div>
        </div>
        """, unsafe_allow_html=True)

    # ================= FOOTER =================
    st.markdown("---")

    st.caption(
        "InvestiScope © 2026 | Investment Intelligence & Risk Analytics System"
    )

    st.caption(
        "Dashboard figures are illustrative sample values, not live predictions."
    )