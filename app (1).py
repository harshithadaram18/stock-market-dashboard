import streamlit as st
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Real-Time Stock Dashboard", layout="wide")
st.title("📈 Real-Time Stock Market Dashboard")

symbol = st.selectbox("Select Stock", ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"])
period = st.selectbox("Select Period", ["5d", "1mo", "3mo", "6mo", "1y"])

@st.cache_data(ttl=60)
def get_stock_data(ticker, selected_period):
    return yf.download(
        ticker,
        period=selected_period,
        interval="1d",
        auto_adjust=False,
        progress=False
    )

try:
    data = get_stock_data(symbol, period)

    if data.empty:
        st.error("No stock data available. Please try again.")
    else:
        if data.columns.nlevels > 1:
            data.columns = data.columns.get_level_values(0)

        latest = data.iloc[-1]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Latest Close", f"${float(latest['Close']):.2f}")
        col2.metric("Day High", f"${float(latest['High']):.2f}")
        col3.metric("Day Low", f"${float(latest['Low']):.2f}")
        col4.metric("Volume", f"{int(latest['Volume']):,}")

        fig = px.line(
            data,
            x=data.index,
            y="Close",
            title=f"{symbol} Stock Price History",
            labels={"x": "Date", "Close": "Price (USD)"}
        )
        st.plotly_chart(fig, width="stretch")

        st.subheader("Historical Stock Data")
        st.dataframe(data, width="stretch")
        st.caption(
            f"Latest available trading date: {data.index[-1].date()}. "
            "Prices may be delayed and are not a live trading feed."
        )

except Exception as e:
    st.error(f"Unable to load stock data: {e}")
