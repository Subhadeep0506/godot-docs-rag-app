from src.services.embeddings_factory import EmbeddingsFactory

embedding = EmbeddingsFactory().get_embeddings(
    embeddings_service="sentence-"
)