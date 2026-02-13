
import os
from google import genai

# Create Gemini client

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_ai_feedback(problem, reasoning):
    prompt = f"""
You are an AI math tutor.

Problem:
{problem}

Student reasoning:
{reasoning}

Your job:
1) Identify where the student's thinking went wrong
2) Explain the mistake
3) Give a hint (not the full answer)
4) Give scores out of 10:
   - Logic
   - Clarity
   - Understanding
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def get_solution(problem):
    prompt = f"""
Solve this step-by-step like a teacher:

Problem:
{problem}

Give:
- Clear steps
- Final answer
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:

        return f"Error: {str(e)}"

