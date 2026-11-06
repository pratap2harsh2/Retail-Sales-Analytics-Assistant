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

print("STARTING SCRIPT")

co = cohere.Client(
    os.getenv("COHERE_API_KEY")
)

EXCEL_FILE = r"C:\Users\prata\OneDrive\Desktop\project folder\Retail Sales Analytics Assistant\data\Retail_Sales_Text2SQL_MVP.xlsx"

client = QdrantClient(
    path="./qdrant_db"
)

COLLECTION_NAME = "retail_metadata"

# Delete old collection if exists
try:
    client.delete_collection(COLLECTION_NAME)
    print("Old collection deleted")
except:
    print("No previous collection found")

# Create new collection
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=1024,
        distance=Distance.COSINE
    )
)

print("Collection Created")

metadata_df = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Metadata"
)

relationships_df = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Relationships"
)

print("Metadata Rows:", len(metadata_df))
print("Relationship Rows:", len(relationships_df))

points = []
point_id = 0

# Metadata
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
                "document": document,
                "type": "metadata"
            }
        )
    )

    point_id += 1

# Relationships
for _, row in relationships_df.iterrows():

    document = f"""
Relationship:
{row['source_table']}.{row['source_column']}
joins
{row['target_table']}.{row['target_column']}
type:
{row['relationship']}
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
                "document": document,
                "type": "relationship"
            }
        )
    )

    point_id += 1

client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print("Documents Uploaded:", len(points))
print("DONE")