from fastapi import FastAPI

from services.llm.retrieve_context import get_context
from services.llm.generate_sql import generate_sql
from services.llm.generate_answer import generate_answer

from src.services.sql_validator import validate_sql
from src.services.sql_executor import execute_sql

app = FastAPI()


@app.post("/ask")
def ask(question: str):

    context = get_context(question)

    sql = generate_sql(
        question,
        context
    )

    validate_sql(sql)

    result_df = execute_sql(sql)

    answer = generate_answer(
        question,
        result_df
    )

    return {
        "question": question,
        "sql": sql,
        "answer": answer,
        "rows": len(result_df),
        "data": result_df.to_dict(
            orient="records"
        )
    }