import sys
from pathlib import Path
import traceback

import streamlit as st
from qdrant_client import QdrantClient

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from vector_store.build_vector_db import build_vector_store

from llm.retrieve_context import get_context
from llm.generate_sql import generate_sql
from llm.generate_answer import generate_answer

from services.sql_validator import validate_sql
from services.sql_executor import execute_sql


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Retail Analytics Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Analytics Assistant")


# ---------------------------------------------------
# QDRANT INITIALIZATION
# ---------------------------------------------------

COLLECTION_NAME = "retail_metadata"

try:

    client = QdrantClient(
        path="./qdrant_db"
    )

    collections = client.get_collections()

    collection_names = [
        c.name
        for c in collections.collections
    ]

    st.sidebar.write(
        "Collections:",
        collection_names
    )

    if COLLECTION_NAME not in collection_names:

        st.info(
            "Collection not found. Building Vector Store..."
        )

        build_vector_store()

        st.success(
            "Vector Store Created Successfully!"
        )

except Exception as e:

    st.error(
        f"Vector DB initialization failed: {e}"
    )

    st.code(
        traceback.format_exc()
    )


# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------

question = st.text_input(
    "Ask a Question",
    placeholder="Which region generated the highest revenue?"
)


# ---------------------------------------------------
# QUERY EXECUTION
# ---------------------------------------------------

if st.button("Generate Answer"):

    if question.strip():

        try:

            with st.spinner(
                "Analyzing data..."
            ):

                context = get_context(
                    question
                )

                sql = generate_sql(
                    question,
                    context
                )

                validate_sql(sql)

                result_df = execute_sql(
                    sql
                )

                answer = generate_answer(
                    question,
                    result_df
                )

            st.subheader(
                "📝 Answer"
            )

            st.success(
                answer
            )

            st.subheader(
                "🛠 Generated SQL"
            )

            st.code(
                sql,
                language="sql"
            )

            st.subheader(
                "📋 Query Result"
            )

            st.dataframe(
                result_df,
                use_container_width=True
            )

            st.metric(
                "Rows Returned",
                len(result_df)
            )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )

            st.code(
                traceback.format_exc()
            )