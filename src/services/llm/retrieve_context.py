from dotenv import load_dotenv

from llm.cohere_client import co
from vector_store.qdrant_manager import get_qdrant_client

load_dotenv()

COLLECTION_NAME = "retail_metadata"


def get_context(question):

    client = get_qdrant_client()

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