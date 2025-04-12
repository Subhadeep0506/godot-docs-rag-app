from dotenv import load_dotenv
import warnings

warnings.filterwarnings("ignore")
load_dotenv()

from src.core.infisical import InfisicalManagedCredentials

secrets_client = InfisicalManagedCredentials()

from src.core.ingestion import Ingestion
from langchain.document_loaders.reddit import RedditPostsLoader
from src.services.embeddings_factory import EmbeddingsFactory
from src.services.vector_store_factory import VectorStoreFactory
import praw

embeddings = EmbeddingsFactory().get_embeddings(
    "sentence-transformers", "intfloat/multilingual-e5-large-instruct"
)

vector_store = VectorStoreFactory().get_vectorstore(
    vectorstore_service="astradb",
    embeddings=embeddings,
)
ingestion = Ingestion(vectorstore=vector_store)
ingestion.ingest_docs(
    directory="dataset/rtdocs/docs.godotengine.org/en/latest/"
)

# ingestion.ingest_conversations("glaiveai/godot_4_docs") # ImJimmeh/godot-training
