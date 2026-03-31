import os
from openai import OpenAI, APIError, AuthenticationError
from system_prompt import SYSTEM_PROMPT

MODEL = "gpt-4o-mini"
TEMPERATURE = 0.7
MAX_TOKENS = 1024


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-api-key-here":
        raise ValueError(
            "Please set your OPENAI_API_KEY in the .env file. "
            "You can get one at https://platform.openai.com/api-keys"
        )
    return OpenAI(api_key=api_key)


def get_response(client: OpenAI, conversation_history: list[dict]) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        return response.choices[0].message.content
    except AuthenticationError:
        return "Invalid API key. Please check your OPENAI_API_KEY in the .env file."
    except APIError as e:
        return f"OpenAI API error: {e.message}"
    except Exception as e:
        return f"Something went wrong: {str(e)}"
