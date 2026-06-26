import os
import json
import google.generativeai as genai
import traceback
from dotenv import load_dotenv
import os

load_dotenv()

print("Loaded API Key:", os.getenv("GEMINI_API_KEY"))
# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")


# -----------------------------
# Ask Gemini (General)
# -----------------------------
def ask_gemini(prompt):

    response = model.generate_content(prompt)

    return response.text


# -----------------------------
# Evaluate Entire Interview
# -----------------------------
def evaluate_interview(questions, answers):

    prompt = f"""
You are an expert AI Technical Interviewer.

Evaluate every interview answer.

For EACH question return:

- score (0-10)
- feedback
- ideal_answer

Return ONLY valid JSON.

Example:

[
    {{
        "score":9,
        "feedback":"Excellent answer with clear explanation.",
        "ideal_answer":"Ideal answer here."
    }},
    {{
        "score":8,
        "feedback":"Good answer but add more details.",
        "ideal_answer":"Ideal answer here."
    }}
]

Questions:

{json.dumps(questions, indent=2)}

Answers:

{json.dumps(answers, indent=2)}

Do NOT return markdown.
Do NOT use ```json.
Return ONLY JSON array.
"""

    try:

        print("========== Sending Interview ==========")

        response = model.generate_content(prompt)

        text = response.text.strip()

        print(text)

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        result = json.loads(text)

        return result

    except Exception as e:

        print("Gemini Error:", e)

        return [
            {
                "score": 0,
                "feedback": str(e),
                "ideal_answer": ""
            }
            for _ in questions
        ]