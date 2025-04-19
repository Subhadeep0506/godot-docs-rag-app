from dotenv import load_dotenv
import os

_ = load_dotenv()

from src.core.infisical import InfisicalManagedCredentials

secrets_client = InfisicalManagedCredentials()
import chainlit as cl
from chainlit.types import ThreadDict
from typing import Optional, Dict
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit.data.storage_clients.base import BaseStorageClient

from ui.utils import generate_response, generate_reddit_response
from ui.components.settings import settings_setup
from ui.components.chat_starters import chat_starters
from ui.components.auth import auth_callback, oauth_callback


@cl.data_layer
def get_data_layer():
    return SQLAlchemyDataLayer(
        conninfo=os.environ.get("SUPABASE_POSTGRESQL_URI"),
        storage_provider=BaseStorageClient,
    )


@cl.set_starters
async def set_starters():
    return chat_starters()


@cl.on_chat_start
async def start_app():
    settings = await settings_setup()
    await settings_update(settings)


@cl.on_chat_resume
async def chat_resume(thread: ThreadDict):
    _ = await settings_setup()
    chainlit_thread_id = thread.get("id")
    chainlit_thread_settings = thread.get("metadata")["chat_settings"]
    cl.user_session.set("current_thread_id", chainlit_thread_id)
    await settings_update(chainlit_thread_settings)


@cl.on_settings_update
async def settings_update(settings: Dict[str, str]):
    cl.user_session.set("model_name", settings["model"])
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
    cl.user_session.set("temperature", settings.get("temperature", 0.7))
    cl.user_session.set("top_k", settings.get("top_k", 10))
    cl.user_session.set("current_thread_id", cl.context.session.thread_id)
    cl.user_session.set("reddit_username", settings.get("reddit_username", None))
    cl.user_session.set("relevance", settings.get("relevance", None))


@cl.on_message
async def on_message(message: cl.Message):
    try:
        response = None
        async with cl.Step(name="generate_response", type="llm") as step:
            response = await generate_response(
                query=message.content,
                session_id=cl.user_session.get("current_thread_id"),
                model_name=cl.user_session.get("model_name"),
                memory_service=cl.user_session.get("memory_service", None),
                category=cl.user_session.get("category", None),
                sub_category=cl.user_session.get("sub_category", None),
                temperature=cl.user_session.get("temperature"),
                top_k=cl.user_session.get("top_k"),
            )
            await step.update()
            await step.remove()
        await cl.Message(content=response["output"]).send()
        if (
            "sorry" in response["output"].lower()
            or "appologize" in response["output"].lower()
        ):
            res = await cl.AskActionMessage(
                content="Do you want to regenerate the response using Reddit tool?",
                actions=[
                    cl.Action(
                        name="continue",
                        payload={"value": "continue"},
                        label="Continue",
                        icon="step-forward"
                    ),
                    cl.Action(
                        name="cancel", payload={"value": "cancel"}, label="Cancel", icon="ban"
                    ),
                ],
            ).send()
            if res and res.get("payload").get("value") == "continue":
                if cl.user_session.get("reddit_username") is None:
                    await cl.Message(
                        content="⚠️ Reddit username is not set. Please set it in the settings. ⚠️",
                    ).send()
                else:
                    async with cl.Step(
                        name="generate_reddit_response", type="llm"
                    ) as inner_step:
                        response = await generate_reddit_response(
                            query=message.content,
                            reddit_username=cl.user_session.get("reddit_username"),
                            relevance=cl.user_session.get("relevance"),
                            session_id=cl.user_session.get("current_thread_id"),
                            model_name=cl.user_session.get("model_name"),
                            memory_service=cl.user_session.get("memory_service", None),
                            temperature=cl.user_session.get("temperature"),
                            top_k=cl.user_session.get("top_k"),
                        )
                        await inner_step.update()
                        await inner_step.remove()
                    await cl.Message(
                        content=response["output"],
                    ).send()
            step.input = message.content
            step.output = response["output"]
            step.metadata = response["intermediate_steps"]
    except Exception as e:
        await cl.ErrorMessage(
            f"An error occurred while processing your request: {str(e)}"
        ).send()
