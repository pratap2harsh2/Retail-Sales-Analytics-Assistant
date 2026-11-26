import pandas as pd

REPORT_PATH = "evaluation/reports/report.csv"


def summarize(report_path):
    df = pd.read_csv(report_path)

    total = len(df)

    passed = len(
        df[df["status"] == "PASS"]
    )

    failed = total - passed

    accuracy = round(
        (passed / total) * 100,
        2
    )

    print("=" * 40)
    print("Evaluation Summary")
    print("=" * 40)

    print(f"Total Questions : {total}")
    print(f"Passed          : {passed}")
    print(f"Failed          : {failed}")
    print(f"Execution Rate  : {accuracy}%")
    

if __name__ == "__main__":
    summarize(REPORT_PATH)