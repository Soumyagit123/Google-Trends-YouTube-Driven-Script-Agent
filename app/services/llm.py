from google import genai
import os
import json
import re

from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_script(prompt: str) -> dict:
    """
    Calls Gemini API and returns a parsed script dict.
    Return type: {"hook": str, "intro": str, "body": str, "outro": str}
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    raw_text = response.text

    return parse_script_output(raw_text)


def parse_script_output(raw_text: str) -> dict:
    """
    Converts Claude's raw text response into a structured hook/intro/body/outro dict.
    Uses three fallback layers to handle different Claude output formats.
    """

    # Layer 1: Try direct JSON parse after stripping markdown code fences
    try:
        clean = re.sub(r"```json|```", "", raw_text).strip()
        parsed = json.loads(clean)
        return {
            "hook": parsed.get("hook", ""),
            "intro": parsed.get("intro", ""),
            "body": parsed.get("body", ""),
            "outro": parsed.get("outro", "")
        }
    except (json.JSONDecodeError, AttributeError):
        pass

    # Layer 2: Extract sections by label using regex
    sections = {"hook": "", "intro": "", "body": "", "outro": ""}
    for key in sections:
        pattern = rf"{key}[:\s]+(.*?)(?=\n(?:hook|intro|body|outro)[:\s]|\Z)"
        match = re.search(pattern, raw_text, re.IGNORECASE | re.DOTALL)
        if match:
            sections[key] = match.group(1).strip()

    # Layer 3: Put entire response in body if all else fails
    if not any(sections.values()):
        sections["body"] = raw_text.strip()

    return sections
