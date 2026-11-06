FORBIDDEN = [
    "DROP",
    "DELETE",
    "UPDATE",
    "ALTER",
    "INSERT",
    "TRUNCATE"
]

def validate_sql(sql):

    query = sql.upper()

    for keyword in FORBIDDEN:

        if keyword in query:

            raise Exception(
                f"Blocked SQL: {keyword}"
            )

    return True