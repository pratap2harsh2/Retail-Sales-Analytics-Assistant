import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="Retail Analytics Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Analytics Assistant")
st.caption(
    "Ask questions about your retail sales data"
)

question = st.text_input(
    "Ask a Question",
    placeholder="Which region generated the highest revenue?"
)

if st.button("Generate Answer"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            with st.spinner(
                "Generating SQL and analyzing data..."
            ):

                response = requests.post(
                    API_URL,
                    params={"question": question}
                )

                result = response.json()

            col1, col2 = st.columns([2, 1])

            with col1:

                st.subheader("📝 Answer")

                st.success(
                    result.get(
                        "answer",
                        "No answer generated"
                    )
                )

            with col2:

                st.subheader("📊 Statistics")

                st.metric(
                    "Rows Returned",
                    result.get(
                        "rows",
                        0
                    )
                )

            st.divider()

            st.subheader("🛠 Generated SQL")

            st.code(
                result.get(
                    "sql",
                    ""
                ),
                language="sql"
            )

            st.divider()

            if "data" in result:

                st.subheader(
                    "📋 Query Result"
                )

                st.dataframe(
                    result["data"],
                    use_container_width=True
                )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )