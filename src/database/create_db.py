
import pandas as pd
from sqlalchemy import create_engine

DB_PATH = "sqlite:///database/retail.db"

engine = create_engine(DB_PATH)

EXCEL_PATH = "data/Retail_Sales_Text2SQL_MVP.xlsx"

data_sheets = [
    "Stores",
    "Products",
    "Customers",
    "Orders"
]

for sheet in data_sheets:

    df = pd.read_excel(
        EXCEL_PATH,
        sheet_name=sheet
    )

    df.to_sql(
        sheet.lower(),
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {sheet}")