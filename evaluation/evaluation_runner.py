import json
from pathlib import Path
import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(PROJECT_ROOT))
from src.services.llm.retrieve_context import get_context
from src.services.llm.generate_sql import generate_sql
from src.services.sql_validator import validate_sql
from src.services.sql_executor import execute_sql

DATASET_PATH = Path(
    "evaluation/datasets/questions_v1.json"
)

REPORT_PATH = Path(
    "evaluation/reports/report.csv"
)


def run_evaluation():

    with open(DATASET_PATH, "r") as f:
        questions = json.load(f)

    results = []

    for item in questions:

        question = item["question"]

        print(f"\nRunning: {question}")

        try:
            context = get_context(question)

            sql = generate_sql(
                question,
                context
            )

            validate_sql(sql)

            result_df = execute_sql(sql)

            results.append({
                "id": item["id"],
                "category": item["category"],
                "question": question,
                "status": "PASS",
                "rows_returned": len(result_df),
                "generated_sql": sql
            })

        except Exception as e:

            results.append({
                "id": item["id"],
                "category": item["category"],
                "question": question,
                "status": "FAIL",
                "rows_returned": 0,
                "generated_sql": "",
                "error": str(e)
            })

    return results


if __name__ == "__main__":

    results = run_evaluation()

    report_df = pd.DataFrame(results)

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report_df.to_csv(
        REPORT_PATH,
        index=False
    )

    print("\nReport saved.")