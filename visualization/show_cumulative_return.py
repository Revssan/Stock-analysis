import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sqlalchemy import create_engine

# -------- SQL Server Connection --------
SERVER = "REVS"
DATABASE = "Stock"

connection_string = (
    f"mssql+pyodbc://{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)
engine = create_engine(connection_string)

# -------- Load Data --------


@st.cache_data
def load_data(query: str):
    df = pd.read_sql(query, engine)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by=["Ticker", "date"])
    return df

# -------- Cumulative Return Function --------


def show_cumulative_return():
    query = """
    SELECT date, Ticker, [close], month
    FROM dbo.stock_price_daily
    WHERE date >= '2024-01-01 00:00:00.000'
    ORDER BY Ticker, date
    """
    df = load_data(query)

    # Daily returns
    df["daily_return"] = df.groupby("Ticker")["close"].pct_change()

    # Cumulative returns
    df["cumulative_return"] = (
        (1 + df["daily_return"]).groupby(df["Ticker"]).cumprod() - 1
    )

    # Top 5 stocks
    final_returns = (
        df.groupby("Ticker")["cumulative_return"].last()
        .reset_index()
        .sort_values(by="cumulative_return", ascending=False)
    )
    top_5_stocks = final_returns.head(5)["Ticker"].tolist()
    top_5_df = df[df["Ticker"].isin(top_5_stocks)]

    # Layout
    with st.container():
        fig, ax = plt.subplots(figsize=(6, 4))
        for stock in top_5_stocks:
            stock_data = top_5_df[top_5_df["Ticker"] == stock]
            ax.plot(stock_data["date"],
                    stock_data["cumulative_return"], label=stock)

        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%y'))
        plt.xticks(rotation=45)

        ax.set_title(
            "Cumulative Return – Top 5 Stocks (Year to Date)", fontsize=12)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Cumulative Return", fontsize=10)
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)
