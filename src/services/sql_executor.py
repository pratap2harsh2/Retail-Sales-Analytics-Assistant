import pandas as pd

from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///database/retail.db"
)
def execute_sql(sql):

    return pd.read_sql(
        sql,
        engine
    )