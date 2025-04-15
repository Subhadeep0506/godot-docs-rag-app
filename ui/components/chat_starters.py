import chainlit as cl


def chat_starters():
    return [
        cl.Starter(
            label="How to use the new animation system",
            message="How to use the new animation system in Godot 4.0?",
            icon="/public/godot.svg",
        ),
        cl.Starter(
            label="How to create a spline path",
            message="Explain how to create a spline path in Godot 4.0 in detailed steps.",
            icon="/public/godot.svg",
        ),
        cl.Starter(
            label="How to add attack sound to attack animation",
            message="How to add attack sound to attack animation in Godot 4.0?",
            icon="/public/godot.svg",
        ),
        cl.Starter(
            label="Give me a simple code to make a moving platform",
            message="Give me a simple code to make a moving platform in Godot 4.0.",
            icon="/public/godot.svg",
        ),
    ]
