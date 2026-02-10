import plotly.graph_objects as go

def var_gauge(var_value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=abs(var_value),
        title={"text": "1-Day VaR"},
        gauge={"axis": {"range": [0, abs(var_value)*2]}}
    ))
    return fig

import numpy as np

def pnl_distribution(port_returns, var_value):
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=port_returns,
        nbinsx=50,
        name="PnL Distribution"
    ))

    fig.add_vline(
        x=var_value,
        line_dash="dash",
        annotation_text="VaR",
        annotation_position="top left"
    )

    fig.update_layout(
        title="Portfolio Return Distribution",
        xaxis_title="Daily Returns",
        yaxis_title="Frequency"
    )

    return fig
