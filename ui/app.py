from typing import Optional, Dict
import chainlit as cl
from components.settings import settings_setup
from components.chat_starters import chat_starters
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from components.auth import auth_callback, oauth_callback


@cl.data_layer
def get_data_layer():
    return SQLAlchemyDataLayer(
        conninfo="postgresql+asyncpg://user_sessions_owner:npg_yRrcv6xmpuH3@ep-curly-paper-a13vinbr-pooler.ap-southeast-1.aws.neon.tech/user_sessions"
    )


@cl.set_starters
async def set_starters():
    return chat_starters()


@cl.on_chat_start
async def start_app():
    settings = await settings_setup()
    await settings_update(settings)


@cl.on_chat_resume
async def chat_resume(thread):
    print("Resumed thread ID", thread)


@cl.on_settings_update
async def settings_update(settings: Dict[str, str]):
    # Settings updated; reinitialize agent executor.
    pass


@cl.on_message
async def on_message(message: cl.Message):
    cl.user_session.set("counter", cl.user_session.get("counter", 0) + 1)
    await cl.Message(
        content=f"You sent {cl.user_session.get('counter', 0)} message(s)!"
    ).send()
