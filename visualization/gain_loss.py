import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# -----------------------------
# Function to calculate top gainers and losers
# -----------------------------


def gain_loss():
    # -----------------------------
    # SQL Server Connection
    # -----------------------------
    SERVER = "REVS"
    DATABASE = "Stock"

    engine = create_engine(
        f"mssql+pyodbc://{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
    )

    # -----------------------------
    # Load data from SQL Server
    # -----------------------------
    query = """
    SELECT date, ticker, [close], [open]
    FROM stock_price_daily
    """
    df = pd.read_sql(query, engine)

    # Fix column names
    df.columns = [col.lower() for col in df.columns]
    df['month'] = df['date'].dt.to_period('M')

    # -----------------------------
    # Calculate Monthly Returns
    # -----------------------------
    monthly_returns = df.groupby(['month', 'ticker']).apply(
        lambda x: (x['close'].iloc[-1] - x['close'].iloc[0]) /
        x['close'].iloc[0] * 100
    ).reset_index(name='monthly_return')

    # -----------------------------
    # Get Top 5 Gainers and Losers
    # -----------------------------
    def get_top5_gainers_losers(df):
        top_gainers = df.groupby('month').apply(
            lambda x: x.nlargest(5, 'monthly_return')).reset_index(drop=True)
        top_losers = df.groupby('month').apply(
            lambda x: x.nsmallest(5, 'monthly_return')).reset_index(drop=True)
        return top_gainers, top_losers

    top_gainers, top_losers = get_top5_gainers_losers(monthly_returns)

    # -----------------------------
    # Streamlit Dashboard
    # -----------------------------
    st.set_page_config(layout="wide")

    # Sidebar: Month filter
    all_months = monthly_returns['month'].astype(str).unique()
    selected_month = st.sidebar.selectbox("Select Month", all_months)

    month_gainers = top_gainers[top_gainers['month'].astype(
        str) == selected_month]
    month_losers = top_losers[top_losers['month'].astype(
        str) == selected_month]

    # Display side-by-side charts
    col1, col2 = st.columns(2)

    with col1:
        fig_gainers = px.bar(
            month_gainers,
            x='ticker',
            y='monthly_return',
            color='monthly_return',
            color_continuous_scale='Greens',
            title=f'Top 5 Gainers - {selected_month}'
        )
        st.plotly_chart(fig_gainers, use_container_width=True)

    with col2:
        fig_losers = px.bar(
            month_losers,
            x='ticker',
            y='monthly_return',
            color='monthly_return',
            color_continuous_scale='Reds',
            title=f'Top 5 Losers - {selected_month}'
        )
        st.plotly_chart(fig_losers, use_container_width=True)
