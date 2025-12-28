import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


def sector():
    # -------------------------
    # SQL Server Connection
    # -------------------------
    SERVER = "REVS"
    DATABASE = "Stock"

    connection_string = (
        f"mssql+pyodbc://{SERVER}/{DATABASE}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )
    engine = create_engine(connection_string)

    # -------------------------
    # Read data from SQL Server
    # -------------------------
    price_query = """
    SELECT date, ticker, [close]
    FROM stock_price_daily
    """

    sector_query = """
    SELECT company, sector
    FROM sector_data
    """

    price_df = pd.read_sql(price_query, engine)
    sector_df = pd.read_sql(sector_query, engine)

    # -------------------------
    # Data Preparation
    # -------------------------
    price_df["date"] = pd.to_datetime(price_df["date"])
    price_df = price_df.sort_values(["ticker", "date"])

    yearly_return = (
        price_df.groupby("ticker")
        .apply(lambda x: (x.iloc[-1]["close"] - x.iloc[0]["close"]) / x.iloc[0]["close"] * 100)
        .reset_index(name="yearly_return")
    )

    sector_return = yearly_return.merge(
        sector_df,
        left_on="ticker",
        right_on="company",
        how="left"
    )

    sector_avg = (
        sector_return.groupby("sector")["yearly_return"]
        .mean()
        .reset_index()
    )

    # -------------------------
    # Container with Chart (No title)
    # -------------------------
    with st.container():
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(sector_avg["sector"], sector_avg["yearly_return"])
        ax.set_xlabel("Sector")
        ax.set_ylabel("Average Yearly Return (%)")
        plt.xticks(rotation=45)

        st.pyplot(fig)
