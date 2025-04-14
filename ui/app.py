# from langchain.agents import AgentExecutor, AgentType, initialize_agent
# from langchain.agents.structured_chat.prompt import SUFFIX
# from langchain.chat_models import ChatOpenAI
# from langchain.memory import ConversationBufferMemory

# import chainlit as cl
# from chainlit.action import Action
# from chainlit.input_widget import Select, Switch, Slider


# @cl.action_callback("Create variation")
# async def create_variant(action: Action):
#     agent_input = f"Create a variation of {action.payload.get('image')}"
#     await cl.Message(
#         content=f"Creating a variation of `{action.payload.get('image')}`."
#     ).send()
#     await main(cl.Message(content=agent_input))


# @cl.author_rename
# def rename(orig_author):
#     mapping = {
#         "LLMChain": "Assistant",
#     }
#     return mapping.get(orig_author, orig_author)


# @cl.cache
# def get_memory():
#     return ConversationBufferMemory(memory_key="chat_history")


# @cl.on_settings_update
# async def setup_agent(settings):
#     print("Setup agent with following settings: ", settings)

#     llm = ChatOpenAI(
#         temperature=settings["Temperature"],
#         streaming=settings["Streaming"],
#         model=settings["Model"],
#     )
#     memory = get_memory()
#     _SUFFIX = "Chat history:\n{chat_history}\n\n" + SUFFIX

#     agent = initialize_agent(
#         llm=llm,
#         tools=[generate_image_tool, edit_image_tool],
#         agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#         memory=memory,
#         agent_kwargs={
#             "suffix": _SUFFIX,
#             "input_variables": ["input", "agent_scratchpad", "chat_history"],
#         },
#     )
#     cl.user_session.set("agent", agent)


# @cl.on_message
# async def main(message: cl.Message):
#     agent = cl.user_session.get("agent")  # type: AgentExecutor
#     cl.user_session.set("generated_image", None)

#     # No async implementation in the Stability AI client, fallback to sync
#     res = await cl.make_async(agent.run)(
#         input=message.content, callbacks=[cl.LangchainCallbackHandler()]
#     )

#     elements = []
#     actions = []

#     generated_image_name = cl.user_session.get("generated_image")
#     generated_image = cl.user_session.get(generated_image_name)
#     if generated_image:
#         elements = [
#             cl.Image(
#                 content=generated_image,
#                 name=generated_image_name,
#                 display="inline",
#             )
#         ]
#         actions = [
#             cl.Action(name="Create variation", payload={"image": generated_image_name})
#         ]

#     await cl.Message(content=res, elements=elements, actions=actions).send()

from typing import Optional
import chainlit as cl
from components.auth import auth_callback

@cl.on_message
async def on_message(message: cl.Message):
    global counter
    counter += 1

    await cl.Message(content=f"You sent {counter} message(s)!").send()
