import os
import requests
from dotenv import load_dotenv

# LOAD ENV HERE
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Add it to a .env file as: GEMINI_API_KEY=your_api_key_here"
    )

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)

def generate_text(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": str(prompt)}
                ]
            }
        ]
    }

    response = requests.post(
        f"{GEMINI_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload,
        timeout=30
    )

    try:
        response.raise_for_status()
        response_data = response.json()
        
        # Extract the text from the response
        if 'candidates' in response_data and response_data['candidates']:
            # Get the first candidate's content
            candidate = response_data['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                # Join all text parts
                return ' '.join(part.get('text', '') for part in candidate['content']['parts'] if 'text' in part)
        return "No content generated"
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"Gemini API error: {e}"
        if response.status_code == 400:
            try:
                error_data = response.json()
                error_msg += f" - {error_data}"
            except:
                pass
        raise RuntimeError(error_msg)
    except Exception as e:
        raise RuntimeError(f"Error in generate_text: {str(e)}")
