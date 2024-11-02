import os

from langchain_cohere import CohereEmbeddings
from langchain_core.embeddings import Embeddings


def get_embeddings_model() -> Embeddings:
    return CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=os.environ["COHERE_API_KEY"])