from llm.cohere_client import co
def generate_answer(
    question,
    results
):

    prompt = f"""
Question:

{question}

Query Result:

{results.to_string()}

Rules:

Use only query results.

If answer not found,
say:

'I could not find the answer in the available data.'
"""

    response = co.chat(
        model="command-a-03-2025",
        message=prompt
    )

    return response.text