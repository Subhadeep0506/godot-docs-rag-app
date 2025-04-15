from typing import Optional
import chainlit as cl
from chainlit.oauth_providers import providers
from chainlit.action import Action
from chainlit.input_widget import Select, Switch, Slider
from typing import Dict, Optional
from components.auth import auth_callback, oauth_callback

from chainlit.data.sql_alchemy import SQLAlchemyDataLayer

@cl.data_layer
def get_data_layer():
    return SQLAlchemyDataLayer(conninfo="postgresql+asyncpg://user_sessions_owner:npg_yRrcv6xmpuH3@ep-curly-paper-a13vinbr-pooler.ap-southeast-1.aws.neon.tech/user_sessions")

@cl.on_chat_start
async def start_app():
    print("Session ID/Thread ID", cl.context.session.thread_id)
    settings = await cl.ChatSettings(
        [
            Select(
                id="model",
                label="Langauge Model",
                values=[
                    "gemini-2.5-pro-preview-03-25",
                    "gemini-2.0-flash",
                    "gemini-2.0-flash-lite",
                    "gemini-1.5-flash",
                    "gemini-1.5-pro",
                    "command-a-03-2025",
                    "command-r7b-12-2024",
                    "command-r-plus-04-2024",
                ],
                initial_index=1,
            ),
            Slider(
                id="temperature",
                label="Model - Temperature",
                initial=0.3,
                min=0,
                max=2,
                step=0.1,
            ),
        ]
    ).send()
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
    await cl.Message(content=f"You sent {counter} message(s)!").send()
