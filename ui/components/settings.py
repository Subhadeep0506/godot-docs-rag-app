import chainlit as cl
from chainlit.input_widget import Select, Slider


async def settings_setup():
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
