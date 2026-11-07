from dotenv import load_dotenv
from qdrant_client import QdrantClient
from llm.cohere_client import co

load_dotenv()

COLLECTION_NAME = "retail_metadata"


def get_context(question):

    client = QdrantClient(
        path="./qdrant_db"
    )

    response = co.embed(
        texts=[question],
        model="embed-english-v3.0",
        input_type="search_query"
    )

    query_vector = response.embeddings[0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=10
    )

    documents = []

    for point in results.points:
        documents.append(
            point.payload["document"]
        )

    return "\n\n".join(documents)