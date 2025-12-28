import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


def Volatility_Analysis():
    # -------- SQL Server Connection --------
    SERVER = "REVS"
    DATABASE = "Stock"

    connection_string = (
        f"mssql+pyodbc://{SERVER}/{DATABASE}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )
    engine = create_engine(connection_string)

    # -------- Load Data --------
    query = """
    SELECT date, Ticker, [close]
    FROM dbo.stock_price_daily
    WHERE date >= '2023-01-01 00:00:00.000' AND date < '2024-01-01 00:00:00.000'
    ORDER BY date
    """
    df = pd.read_sql(query, engine)

    # -------- Data Preparation --------
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by=["Ticker", "date"])

    # -------- Daily Returns --------
    df["daily_return"] = df.groupby("Ticker")["close"].pct_change()

    # -------- Volatility Calculation --------
    volatility_df = (
        df.groupby("Ticker")["daily_return"]
        .std()
        .reset_index()
        .rename(columns={"daily_return": "volatility"})
    )

    # -------- Top 10 Volatile Stocks --------
    top_10 = volatility_df.sort_values(
        by="volatility", ascending=False).head(10)

    # -------- Layout with container --------
    with st.container():

        # -------- Bar Chart --------
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(top_10["Ticker"], top_10["volatility"], color="skyblue")
        ax.set_title("Top 10 Most Volatile Stocks (Past Year)")
        ax.set_xlabel("Stocks")
        ax.set_ylabel("Volatility")
        plt.xticks(rotation=45)

        st.pyplot(fig)
