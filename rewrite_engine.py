import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

async def run_agents(text: str) -> dict:
    """
    Runs Writer → Editor → Reviewer in sequence, but internally optimized for speed.
    No streaming — just returns the final polished chapter as before.
    """
    # Writer stage
    writer_prompt = (
        "Rewrite the following chapter to be more engaging, vivid, and atmospheric.\n"
        "— Output only the rewritten story, nothing else.\n"
        "— Do not include explanations or change logs.\n"
        "— Preserve all characters, settings, and core plot events exactly.\n\n"
        f"{text}"
    )
    writer_result = model.generate_content(writer_prompt).text.strip()

    # Editor stage
    editor_prompt = (
        "Edit the rewritten chapter below for clarity, grammar, flow, and consistency.\n"
        "— Output only the edited story, nothing else.\n"
        "— Do not include explanations or change logs.\n"
        "— Preserve the style and plot from the writer’s version.\n\n"
        f"{writer_result}"
    )
    editor_result = model.generate_content(editor_prompt).text.strip()

    # Reviewer stage
    reviewer_prompt = (
        "Review and polish the edited chapter for final publication quality.\n"
        "— Output only the polished story, nothing else.\n"
        "— Do not include comments, suggestions, or change logs.\n"
        "— Retain the tone, character voices, and plot intact.\n\n"
        f"{editor_result}"
    )
    reviewer_result = model.generate_content(reviewer_prompt).text.strip()

    return {
        "written": writer_result,
        "edited": editor_result,
        "reviewed": reviewer_result
    }
