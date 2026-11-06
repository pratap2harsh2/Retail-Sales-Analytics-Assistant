def build_vector_store():

    import os
    import pandas as pd
    import cohere

    from dotenv import load_dotenv
    from qdrant_client import QdrantClient
    from qdrant_client.models import (
        Distance,
        VectorParams,
        PointStruct
    )

    load_dotenv()

    try:
        import streamlit as st
        api_key = st.secrets["COHERE_API_KEY"]
    except:
        api_key = os.getenv("COHERE_API_KEY")

    co = cohere.Client(api_key)

    EXCEL_FILE = "data/Retail_Sales_Text2SQL_MVP.xlsx"

    client = QdrantClient(
        path="./qdrant_db"
    )

    COLLECTION_NAME = "retail_metadata"

    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE
        )
    )

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

    print("Vector Store Created")

    client.close()


if __name__ == "__main__":
    build_vector_store()