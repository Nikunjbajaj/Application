import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(
    page_title="Stock Price Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Price Dashboard")

ticker = st.text_input(
    "Enter Stock Symbol",
    value="AAPL",
    help="Examples: AAPL, MSFT, TSLA, RELIANCE.NS, TCS.NS"
).upper()

period = st.selectbox(
    "Select Time Period",
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

interval_map = {
    "1mo": "1d",
    "3mo": "1d",
    "6mo": "1d",
    "1y": "1d",
    "2y": "1wk",
    "5y": "1wk",
    "10y": "1mo",
    "max": "1mo"
}

if st.button("Fetch Data"):

    with st.spinner("Downloading data..."):

        data = yf.download(
            ticker,
            period=period,
            interval=interval_map[period],
            auto_adjust=True,
            progress=False
        )

    if data.empty:
        st.error("No data found.")
    else:

        latest = float(data["Close"].iloc[-1])
        highest = float(data["High"].max())
        lowest = float(data["Low"].min())

        c1, c2, c3 = st.columns(3)

        c1.metric("Latest Price", f"{latest:.2f}")
        c2.metric("Highest", f"{highest:.2f}")
        c3.metric("Lowest", f"{lowest:.2f}")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                mode="lines",
                name="Close Price",
                line=dict(width=3)
            )
        )

        fig.update_layout(
            title=f"{ticker} Stock Price",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_white",
            height=650,
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Historical Data")
        st.dataframe(data)

        csv = data.to_csv().encode()

        st.download_button(
            "Download CSV",
            csv,
            f"{ticker}_{period}.csv",
            "text/csv"
        )
