
import os
from google import genai

# Create Gemini client

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_ai_feedback(problem, reasoning):
  
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


