from llm.cohere_client import co


def generate_sql(question, context):

    prompt = f"""
You are a SQLite expert.

Generate ONLY valid SQLite SQL.

Rules:
- Return only SQL.
- Do not explain.
- Do not use markdown.
- Do not use ```sql blocks.
- Use only provided metadata.

Metadata:
{context}

Question:
{question}
"""

    response = co.chat(
        model="command-a-03-2025",
        message=prompt
    )

    sql = response.text

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    print("\\nGenerated SQL:")
    print(sql)

    return sql