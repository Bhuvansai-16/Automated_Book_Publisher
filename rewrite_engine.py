import os
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

async def agent_call(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()

async def run_agents(text: str) -> dict:
    writer_prompt = f"Rewrite the following chapter to be more engaging, vivid, and atmospheric.— Output only the rewritten story, nothing else.— Do not include explanations or change logs.— Preserve all characters, settings, and core plot events exactly.\n\n{text}"
    written = await agent_call(writer_prompt)

    editor_prompt = f"Edit the rewritten chapter below for clarity, grammar, flow, and consistency.— Output only the edited story, nothing else.— Do not include explanations or change logs.— Preserve the style and plot from the writer’s version.\n\n{written}"
    edited = await agent_call(editor_prompt)

    reviewer_prompt = f"Review and polish the edited chapter for final publication quality.— Output only the polished story, nothing else.— Do not include comments, suggestions, or change logs.— Retain the tone, character voices, and plot intact.\n\n{edited}"
    reviewed = await agent_call(reviewer_prompt)

    return {
        "written": written,
        "edited": edited,
        "reviewed": reviewed
    }
