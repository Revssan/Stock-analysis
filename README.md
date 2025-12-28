# 📊 Stock Data Extraction, Analysis & Visualization

## 📁 Project Overview

This project focuses on **extracting stock market data from YAML files**, transforming it into **CSV format**, and performing **comprehensive data analysis and visualization** using Python.

The data is organized **month-wise**, with **date-wise entries inside each month**, and contains information for **multiple stock symbols**. After processing, the system generates **50 CSV files**, one for each stock symbol or data category.

---

## 🗂️ Data Extraction & Transformation

### 🔹 Input Format

* Data Source: **YAML files**
* Structure:

  * Month-level folders
  * Date-wise stock data within each month

### 🔹 Transformation Objective

* Parse YAML data
* Normalize and consolidate records
* Export **symbol-wise CSV files**

### 🔹 Output

* ✅ 50 CSV files
* Each CSV represents **one stock symbol** with historical data across the year

---

## 🧮 Data Analysis & Metrics

All analysis is performed using **Python (Pandas, NumPy, Matplotlib, Seaborn)**.

### 📌 Key Market Metrics

#### 1️⃣ Top 10 Green Stocks

* Sorted by **yearly return (highest)**

#### 2️⃣ Top 10 Loss Stocks

* Sorted by **yearly return (lowest)**

#### 3️⃣ Market Summary

* Number of **Green vs Red stocks**
* **Average Price** across all stocks
* **Average Volume** across all stocks

---

## 📈 Visual Analytics

### 1️⃣ Volatility Analysis

**Objective:**

* Measure and visualize stock price volatility over the year

**Why It Matters:**

* Higher volatility → Higher risk
* Lower volatility → More stable stock

**Methodology:**

* Daily Return:

  ```text
  (Close Price - Previous Close Price) / Previous Close Price
  ```
* Volatility = **Standard Deviation of Daily Returns**

**Visualization:**

* 📊 Bar chart of **Top 10 Most Volatile Stocks**

  * X-axis: Stock Symbol
  * Y-axis: Volatility (Std Dev)

---

### 2️⃣ Cumulative Return Over Time

**Objective:**

* Track stock growth from start to end of the year

**Why It Matters:**

* Shows long-term performance trends

**Methodology:**

* Compute cumulative return using running daily returns

**Visualization:**

* 📈 Line chart for **Top 5 Performing Stocks**

  * X-axis: Date
  * Y-axis: Cumulative Return

---

### 3️⃣ Sector-wise Performance Analysis

**Objective:**

* Analyze stock performance grouped by industry sectors

**Data Source:**

* External **Sector Mapping CSV**

**Methodology:**

* Map stocks to sectors
* Calculate **average yearly return per sector**

**Visualization:**

* 📊 Bar chart: **Average Yearly Return by Sector**

---

### 4️⃣ Stock Price Correlation Analysis

**Objective:**

* Identify relationships between stock price movements

**Why It Matters:**

* Helps in diversification and risk management

**Methodology:**

* Use `pandas.DataFrame.corr()` on closing prices

**Visualization:**

* 🌡️ Correlation Heatmap

  * Darker colors indicate stronger correlations

---

### 5️⃣ Monthly Top 5 Gainers & Losers

**Objective:**

* Identify short-term monthly trends

**Why It Matters:**

* Helps detect momentum and reversals

**Methodology:**

* Group data by **month**
* Calculate **monthly percentage returns**
* Identify:

  * Top 5 Gainers
  * Top 5 Losers

**Visualization:**

* 📊 Dashboard with **12 Monthly Bar Charts**

  * Each chart shows Top 5 Gainers & Losers for that month

---

## 🛠️ Tech Stack

* **Python**
* **Pandas & NumPy** – Data processing
* **Matplotlib & Seaborn** – Visualization
* **PyYAML** – YAML parsing

---

## 🚀 Outcomes

* YAML data ingestion into SQL Server (manual execution)
* Yearly stock performance insights
* Risk & volatility assessment
* Sector-based and correlation analysis
* Monthly gainers & losers dashboard


