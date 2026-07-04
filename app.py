import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Stock Price Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Price Dashboard")

st.sidebar.header("Settings")

ticker = st.sidebar.text_input(
    "Stock Symbol",
    value="AAPL"
).upper().strip()

period = st.sidebar.selectbox(
    "Time Period",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "max"
    ]
)

intervals = {
    "1mo": "1d",
    "3mo": "1d",
    "6mo": "1d",
    "1y": "1d",
    "2y": "1wk",
    "5y": "1wk",
    "10y": "1mo",
    "max": "1mo"
}

interval = intervals[period]

try:

    data = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
        threads=False
    )

    if data.empty:
        st.error("No data available.")
        st.stop()

    # Handle MultiIndex columns if returned
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.dropna()

    latest = float(data["Close"].iloc[-1])
    high = float(data["High"].max())
    low = float(data["Low"].min())

    c1, c2, c3 = st.columns(3)

    c1.metric("Latest Price", f"{latest:,.2f}")
    c2.metric("Highest", f"{high:,.2f}")
    c3.metric("Lowest", f"{low:,.2f}")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Close",
            line=dict(width=2)
        )
    )

    fig.update_layout(
        template="plotly_white",
        title=f"{ticker} Closing Price",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified",
        height=650
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Historical Data")

    st.dataframe(data, use_container_width=True)

    csv = data.to_csv().encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{ticker}_{period}.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error("Unable to fetch stock data.")
    st.exception(e)
