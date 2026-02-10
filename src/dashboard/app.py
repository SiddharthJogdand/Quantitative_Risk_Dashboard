import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.data.loader import load_market_data, load_portfolio
from src.engine.var_engine import VaREngine
from src.dashboard.plots import var_gauge, pnl_distribution


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(layout="wide")
st.title("📊 Quantitative Risk Dashboard")
st.markdown("#### Institutional Portfolio Risk Monitoring System")


# -------------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------------
st.sidebar.header("⚙ Risk Parameters")

confidence = st.sidebar.slider(
    "Confidence Level",
    min_value=0.80,
    max_value=0.999,
    value=0.95,
    step=0.005
)

method = st.sidebar.selectbox(
    "VaR Method",
    ["Historical", "Monte Carlo", "Parametric"]
)

window = st.sidebar.slider(
    "Rolling Window (Days)",
    min_value=100,
    max_value=500,
    value=252
)


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
portfolio = load_portfolio()
prices, returns = load_market_data(portfolio.instrument_id.tolist())
engine = VaREngine(portfolio, returns)


# -------------------------------------------------
# COMPUTE METRICS
# -------------------------------------------------
if method == "Historical":
    var, es = engine.historical_var(confidence)
elif method == "Monte Carlo":
    var, es = engine.monte_carlo_var(confidence)
else:
    var, es = engine.parametric_var(confidence)

port_returns = engine._portfolio_returns()
component_contrib = engine.component_var()
cumulative = engine.cumulative_returns()
drawdown = engine.drawdown()


# -------------------------------------------------
# TABS
# -------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Risk Overview",
    "📈 Backtesting",
    "📉 Portfolio Analytics"
])


# =====================================================
# TAB 1 — RISK OVERVIEW
# =====================================================
with tab1:

    col1, col2, col3 = st.columns(3)

    col1.metric("VaR", f"{var:.2%}")
    col2.metric("Expected Shortfall", f"{es:.2%}")
    col3.metric("Confidence", f"{confidence:.3f}")

    st.plotly_chart(var_gauge(var), width="stretch")

    colA, colB = st.columns(2)

    with colA:
        st.plotly_chart(
            pnl_distribution(port_returns, var),
            width="stretch"
        )

    with colB:
        fig_contrib = px.bar(
            component_contrib,
            title="Asset Risk Contribution",
            labels={"value": "Contribution", "index": "Asset"}
        )
        fig_contrib.update_layout(showlegend=False)
        st.plotly_chart(fig_contrib, width="stretch")


# =====================================================
# TAB 2 — BACKTESTING
# =====================================================
with tab2:

    rolling_var, breaches, breach_count = engine.backtest_var(
        confidence=confidence,
        window=window
    )

    st.metric("VaR Breaches", int(breach_count))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=rolling_var.index,
        y=rolling_var,
        name="Rolling VaR"
    ))

    fig.add_trace(go.Scatter(
        x=port_returns.index,
        y=port_returns,
        name="Actual Returns",
        opacity=0.5
    ))

    fig.update_layout(
        title=f"Rolling VaR vs Actual Returns ({window}-Day Window)",
        xaxis_title="Date",
        yaxis_title="Returns"
    )

    st.plotly_chart(fig, width="stretch")


# =====================================================
# TAB 3 — PORTFOLIO ANALYTICS
# =====================================================
with tab3:

    col1, col2 = st.columns(2)

    with col1:
        fig_cum = px.line(
            cumulative,
            title="Cumulative Portfolio Returns"
        )
        st.plotly_chart(fig_cum, width="stretch")

    with col2:
        fig_dd = px.line(
            drawdown,
            title="Portfolio Drawdown"
        )
        st.plotly_chart(fig_dd, width="stretch")

    st.subheader("Correlation Heatmap")

    corr_matrix = returns.corr()

    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Asset Correlation Matrix"
    )

    st.plotly_chart(fig_corr, width="stretch")
