import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_google_genai import GoogleGenerativeAIEmbeddings

QDRANT_COLLECTION_NAME = "document_vectors"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

def initialize_vector_store(splits):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    try:
        client.get_collection(QDRANT_COLLECTION_NAME)
    except:
        size = len(embeddings.embed_query("test"))
        client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )

    points = []
    for idx, chunk in enumerate(splits):
        vector = embeddings.embed_query(chunk)
        points.append(PointStruct(id=idx, vector=vector, payload={"text": chunk}))

    if points:
        client.upsert(QDRANT_COLLECTION_NAME, points=points)
    return client, embeddings
