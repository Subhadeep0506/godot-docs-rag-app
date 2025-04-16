import chainlit as cl
from chainlit.input_widget import Select, Slider


async def settings_setup():
    settings = await cl.ChatSettings(
        [
            Select(
                id="model",
                label="Langauge Model",
                items={
                    "Gemini 2.5 Pro": "gemini-2.5-pro-preview-03-25",
                    "Gemini 2.0 Flash": "gemini-2.0-flash",
                    "Gemini 2.0 Flash Lite": "gemini-2.0-flash-lite",
                    "Gemini 1.5 Flash": "gemini-1.5-flash",
                    "Gemini 1.5 Pro": "gemini-1.5-pro",
                    "Cohere Command A": "command-a-03-2025",
                    "Cohere Command R 7B": "command-r7b-12-2024",
                    "Cohere Command R+": "command-r-plus-04-2024",
                    "Mistral - Codestral": "codestral-latest",
                    "Mistral - Large": "mistral-large-latest",
                    "Mistral - Small": "mistral-small-latest",
                    "Ministral 3B": "ministral-3b-latest",
                    "Ministral 8B": "ministral-8b-latest",
                    "Deepseek R1 Distill Llama 70B - Groq": "deepseek-r1-distill-llama-70b",
                    "Gemma 2 9B IT - Groq": "gemma2-9b-it",
                    "Llama 3.1 8B Instant - Groq": "llama-3.1-8b-instant",
                    "Llama 3.3 70B Versatile - Groq": "llama-3.3-70b-versatile",
                    "Llama 3 70B - Groq": "llama3-70b-8192",
                    "Llama 3 8B - Groq": "llama3-8b-8192",
                    "Qwen QwQ 32B - Groq": "qwen-qwq-32b",
                },
                initial_value="mistral-large-latest",
            ),
            Slider(
                id="temperature",
                label="Model - Temperature",
                initial=0.3,
                min=0,
                max=2,
                step=0.1,
            ),
            Select(
                id="vectorstore_service",
                label="Vectorstore Service",
                items={
                    "AstraDB": "astradb",
                    "Milvus": "milvus",
                },
                initial_value="astradb",
            ),
            Select(
                id="memory_service",
                label="Memory Service",
                items={
                    "Upstash Redis": "upstash",
                    "AstraDB": "astradb",
                },
                initial_value="astradb",
            ),
            Select(
                id="category",
                label="Category",
                items={
                    "None": "None",
                    "About": "about",
                    "Classes": "classes",
                    "Getting Started": "getting_started",
                    "Tutorials": "tutorials",
                    "Conversations": "conversations",
                },
            ),
            Select(
                id="sub_category",
                label="Sub Category",
                tooltip="Sub Category is optional and is available only for Getting Started and Tutorials category ONLY. Select None for other categories.",
                items={
                    "None": "None",
                    "2D": "2d",
                    "3D": "3d",
                    "Animation": "anumation",
                    "Assets Pipeline": "assets_pipeline",
                    "Audio": "audio",
                    "Best Practices": "best_practices",
                    "Editor": "editor",
                    "Export": "export",
                    "Internationalization": "i18n",
                    "Math": "math",
                    "Migrating": "migrating",
                    "Navigation": "navigation",
                    "Networking": "networking",
                    "Performance": "performance",
                    "Physics": "physics",
                    "Platform": "platform",
                    "Plugins": "plugins",
                    "Rendering": "rendering",
                    "Scripting": "scripting",
                    "Shaders": "shaders",
                    "UI": "ui",
                    "XR": "xr",
                },
            ),
        ]
    ).send()
    return settings
