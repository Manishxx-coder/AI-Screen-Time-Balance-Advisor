import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm():
    model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

    return ChatGoogleGenerativeAI(
        model=model
    )


def get_text(response):
    content = response.content

    # Gemini may return a list of content blocks
    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
            else:
                parts.append(str(item))

        return "".join(parts).strip()

    return str(content).strip()


def extract_day_data(text):

    llm = get_llm()

    prompt = f"""
Extract information from this sentence.

Return ONLY JSON in exactly this format:

{{
    "screen_time_hours": 0,
    "study_time_hours": 0,
    "sleep_hours": 0
}}

Rules:
- Convert minutes into decimal hours.
- If the user says 6 hours 30 minutes, return 6.5.
- If a value is not mentioned, return 0.
- Do not add markdown.
- Do not add explanations.

Sentence:
{text}
"""

    response = llm.invoke(prompt)

    content = get_text(response)

    # Remove accidental markdown code fences
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    data = json.loads(content)

    return {
        "screen_time_hours": float(data["screen_time_hours"]),
        "study_time_hours": float(data["study_time_hours"]),
        "sleep_hours": float(data["sleep_hours"])
    }


def generate_explanation(data, result):

    llm = get_llm()

    prompt = f"""
Give a short explanation of this daily balance.

Screen time: {data["screen_time_hours"]} hours
Study time: {data["study_time_hours"]} hours
Sleep: {data["sleep_hours"]} hours

Fuzzy balance score: {result["score"]}/100
Balance level: {result["level"]}

Give exactly two simple practical suggestions.
Do not give medical advice.
"""

    response = llm.invoke(prompt)

    return get_text(response)