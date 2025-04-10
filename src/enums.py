from enum import Enum


class EmbeddingsService(Enum):
    COHERE = "cohere"
    SENTENCE_TRANSFORMERS = "sentence-transformers"


class LLMService(Enum):
    COHERE = "cohere"
    GEMINI = "gemini"
    GROQ = "groq"


class VectorStoreService(Enum):
    MILVUS = "milvus"
    ASTRADB = "astradb"
