import os
import yaml
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import String, Float, BigInteger, DateTime

# =============================
# CONFIGURATION
# =============================

YAML_FOLDER = r"E:\Fileconversion\data\2024-11"        # Month folder
TABLE_NAME = "stock_price_daily"

SERVER = "REVS"
DATABASE = "Stock"

# =============================
# STEP 1: READ YAML FILES
# =============================

all_records = []

for file_name in os.listdir(YAML_FOLDER):
    if file_name.endswith((".yaml", ".yml")):

        file_path = os.path.join(YAML_FOLDER, file_name)

        with open(file_path, "r") as file:
            data = yaml.safe_load(file)

        if not data:
            continue

        # YAML is already a list of records
        for record in data:
            all_records.append(record)

# =============================
# STEP 2: CREATE DATAFRAME
# =============================

df = pd.DataFrame(all_records)

# =============================
# STEP 3: DATA TYPE CLEANING
# =============================

df["Ticker"] = df["Ticker"].astype(str)

df["open"] = df["open"].astype(float)
df["high"] = df["high"].astype(float)
df["low"] = df["low"].astype(float)
df["close"] = df["close"].astype(float)

df["volume"] = df["volume"].astype("int64")

df["date"] = pd.to_datetime(df["date"])
df["month"] = df["month"].astype(str)

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# =============================
# STEP 4: CONNECT TO SQL SERVER
# =============================

connection_string = (
    f"mssql+pyodbc://{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(connection_string)

# =============================
# STEP 5: LOAD TO SQL SERVER
# =============================

dtype_mapping = {
    "Ticker": String(20),
    "open": Float(),
    "high": Float(),
    "low": Float(),
    "close": Float(),
    "volume": BigInteger(),
    "date": DateTime(),
    "month": String(7)
}

df.to_sql(
    name=TABLE_NAME,
    con=engine,
    if_exists="append",
    index=False,
    chunksize=1000,
    dtype=dtype_mapping
)

print("✅ Stock data successfully loaded into SQL Server")
