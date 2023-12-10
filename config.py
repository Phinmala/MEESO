import os
import openai

def get_openai_client():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("No OpenAI API key found in environment variables")
    return openai.OpenAI(api_key=api_key)

