from dotenv import load_dotenv
import os

_ = load_dotenv()

from src.core.infisical import InfisicalManagedCredentials

secrets_client = InfisicalManagedCredentials()
import chainlit as cl

from src.core.query import Query
from src.services.embeddings_factory import EmbeddingsFactory
from src.services.vector_store_factory import VectorStoreFactory
from src.services.llm_factory import LLMFactory

from typing import Optional, Dict
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer

from ui.components.settings import settings_setup
from ui.components.chat_starters import chat_starters
from ui.components.auth import auth_callback, oauth_callback


@cl.cache
def load_embeddings():
    embeddings = EmbeddingsFactory().get_embeddings(
        "sentence-transformers", "intfloat/multilingual-e5-large-instruct"
    )
    return embeddings


embeddings = load_embeddings()


@cl.data_layer
def get_data_layer():
    return SQLAlchemyDataLayer(conninfo=os.environ.get("SUPABASE_POSTGRESQL_URI"))


@cl.set_starters
async def set_starters():
    return chat_starters()


@cl.on_chat_start
async def start_app():
    settings = await settings_setup()
    await settings_update(settings)


@cl.on_chat_resume
async def chat_resume(thread):
    chainlit_thread_id = thread.get("id")
    cl.user_session.set("current_thread_id", chainlit_thread_id)
    # TODO: Implement logic to resume the chat with the last message


@cl.on_settings_update
async def settings_update(settings: Dict[str, str]):
    vector_store = VectorStoreFactory().get_vectorstore(
        vectorstore_service=settings["vectorstore_service"],
        embeddings=embeddings,
    )

    llm = LLMFactory().get_chat_model(
        model_name=settings["model"],
    )
    query = Query(vectorstore=vector_store)
    cl.user_session.set("llm_service", llm)
    cl.user_session.set("memory_service", settings["memory_service"])
    cl.user_session.set(
        "category",
        (
            None
            if settings["category"] == "None" or settings["category"] is None
            else settings["category"]
        ),
    )
    cl.user_session.set(
        "sub_category",
        (
            None
            if settings["sub_category"] == "None" or settings["sub_category"] is None
            else settings["sub_category"]
        ),
    )
    cl.user_session.set("query_chain", query)
    cl.user_session.set("current_thread_id", cl.context.session.thread_id)


@cl.on_message
async def on_message(message: cl.Message):
    query_chain = cl.user_session.get("query_chain")
    response = query_chain.generate_response(
        query=message.content,
        category=cl.user_session.get("category", None),
        sub_category=cl.user_session.get("sub_category", None),
        source=None,
        top_k=10,
        session_id=cl.user_session.get("current_thread_id", None),
        memory_service=cl.user_session.get("memory_service", None),
        llm=cl.user_session.get("llm_service"),
    )["output"]
    await cl.Message(content=response).send()
