import streamlit as st
from visualization.show_cumulative_return import show_cumulative_return
from visualization.Volatility_Analysis import Volatility_Analysis
from visualization.sector import sector
from visualization.Stock_Price_Correlation import Stock_Price_Correlation
from visualization.gain_loss import gain_loss

st.set_page_config(page_title="Stock Analysis", layout="wide")
st.markdown("<h1 style='text-align: center;'>📊Data-Driven Stock Analysis</h1>",
            unsafe_allow_html=True)

st.markdown("""
<style>
.block-container {
    padding-top: 2.5rem;
}

.chart-card {
    background-color: #0e1117;
    border-radius: 12px;
    padding: 16px;
    height: 100%;
}

.chart-title {
    text-align: center;
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>📉 Stock Volatility Analysis</div>",
                unsafe_allow_html=True)
    Volatility_Analysis()
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>📈 Cumulative Return Analysis (Top 5 Stocks)</div>",
                unsafe_allow_html=True)
    show_cumulative_return()
    st.markdown("</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>🏭 Average Yearly Return by Sector</div>",
                unsafe_allow_html=True)
    sector()
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>🔗 Stock Price Correlation Heatmap</div>",
                unsafe_allow_html=True)
    Stock_Price_Correlation()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='chart-card' style='display:flex; justify-content:center;'>",
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class='chart-title'
         style='text-align:center; font-size:26px; font-weight:600;'>
         📈 Top 5 Stock Gainers and Losers by Month
    </div>
    """,
    unsafe_allow_html=True
)

gain_loss()

st.markdown("</div>", unsafe_allow_html=True)
