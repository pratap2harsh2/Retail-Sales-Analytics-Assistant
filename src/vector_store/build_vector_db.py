import os
import pandas as pd
import cohere

from dotenv import load_dotenv
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from vector_store.qdrant_manager import get_qdrant_client


def build_vector_store():

    print("Building Vector Store...")

    load_dotenv()

    try:
        import streamlit as st
        api_key = st.secrets["COHERE_API_KEY"]
    except Exception:
        api_key = os.getenv("COHERE_API_KEY")

    co = cohere.Client(api_key)

    client = get_qdrant_client()

    COLLECTION_NAME = "retail_metadata"

    collections = client.get_collections()

    collection_names = [
        c.name
        for c in collections.collections
    ]

    # Collection already exists
    if COLLECTION_NAME in collection_names:
        print("Collection already exists.")
        return

    EXCEL_FILE = "data/Retail_Sales_Text2SQL_MVP.xlsx"

    print("Excel exists:", os.path.exists(EXCEL_FILE))

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE
        )
    )

    print("Collection created.")

    metadata_df = pd.read_excel(
        EXCEL_FILE,
        sheet_name="Metadata"
    )

    relationships_df = pd.read_excel(
        EXCEL_FILE,
        sheet_name="Relationships"
    )

    points = []
    point_id = 0

    # Metadata embeddings
    for _, row in metadata_df.iterrows():

        document = f"""
Table: {row['table_name']}
Column: {row['column_name']}
Description: {row['description']}
Keywords: {row['keywords']}
"""

        response = co.embed(
            texts=[document],
            model="embed-english-v3.0",
            input_type="search_document"
        )

        embedding = response.embeddings[0]

        points.append(
            PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "document": document
                }
            )
        )

        point_id += 1

    # Relationship embeddings
    for _, row in relationships_df.iterrows():

        document = f"""
Relationship:
{row['source_table']}.{row['source_column']}
joins
{row['target_table']}.{row['target_column']}
"""

        response = co.embed(
            texts=[document],
            model="embed-english-v3.0",
            input_type="search_document"
        )

        embedding = response.embeddings[0]

        points.append(
            PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "document": document
                }
            )
        )

        point_id += 1

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Inserted {len(points)} vectors")

    collections = client.get_collections()

    print(
        "Collections:",
        [c.name for c in collections.collections]
    )

    print("Vector Store Created Successfully")


if __name__ == "__main__":
    build_vector_store()