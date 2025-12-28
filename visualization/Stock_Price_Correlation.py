import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine


def Stock_Price_Correlation():

    # -------------------------
    # SQL Server Connection
    # -------------------------
    SERVER = "REVS"
    DATABASE = "Stock"

    engine = create_engine(
        f"mssql+pyodbc://{SERVER}/{DATABASE}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )

    # -------------------------
    # Load data
    # -------------------------
    query = """
    SELECT date, ticker, [close]
    FROM stock_price_daily
    ORDER BY date
    """
    df = pd.read_sql(query, engine)

    df["date"] = pd.to_datetime(df["date"])

    # -------------------------
    # Pivot & Monthly Returns
    # -------------------------
    price_pivot = df.pivot(index="date", columns="ticker", values="close")
    monthly_prices = price_pivot.resample("M").last()
    monthly_returns = monthly_prices.pct_change()

    # -------------------------
    # Sidebar filter
    # -------------------------
    st.sidebar.subheader("Filter Stocks")

    selected_tickers = st.sidebar.multiselect(
        "Select Stocks",
        monthly_returns.columns,
        default=monthly_returns.columns[:15]
    )

    if len(selected_tickers) < 2:
        st.warning("Select at least two stocks.")
        st.stop()

    filtered_returns = monthly_returns[selected_tickers]

    # -------------------------
    # Correlation Matrix (NxN)
    # -------------------------
    corr_matrix = filtered_returns.corr()

    # -------------------------
    # Square Heatmap
    # -------------------------
    n = len(corr_matrix)

    fig, ax = plt.subplots(figsize=(n * 0.6, n * 0.6))

    im = ax.imshow(corr_matrix, cmap="RdYlGn", vmin=-1, vmax=1)

    # Force square cells
    ax.set_aspect("equal")

    # Axis ticks
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))

    ax.set_xticklabels(corr_matrix.columns, rotation=90, fontsize=8)
    ax.set_yticklabels(corr_matrix.columns, fontsize=8)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Correlation")

    ax.set_title("Monthly Stock Price Correlation", fontsize=12)

    plt.tight_layout()
    st.pyplot(fig)
