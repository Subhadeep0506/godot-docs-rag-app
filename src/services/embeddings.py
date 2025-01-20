import os

import torch
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_cohere import CohereEmbeddings
from langchain_core.embeddings import Embeddings


def get_embeddings_model(type: str = "cohere", model: str = None) -> Embeddings:
    if type == "sentence-transformer":
        if model is not None:
            return SentenceTransformerEmbeddings(
                model=model,
                model_kwargs={
                    "device": torch.device(
                        "cuda" if torch.cuda.is_available() else "cpu"
                    )
                },
            )
        else:
            raise ValueError("Model is required for SentenceTransformerEmbeddings")
    elif type == "cohere":
        return CohereEmbeddings(
            model="embed-english-v3.0", cohere_api_key=os.environ["COHERE_API_KEY"]
        )
