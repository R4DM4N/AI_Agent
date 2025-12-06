import os
from dotenv import load_dotenv
from google import genai

# from google.genai import types
from datetime import datetime

MODEL_ID = "gemini-2.5-flash"  # @param ["gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-2.5-pro","gemini-3-pro-preview"] {"allow-input":true, isTemplate: true}

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")
client = genai.Client(api_key=api_key)

prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."


def main():
    # Token Max
    t_max = token_max(MODEL_ID)
    print(t_max)
    # Count tokens

    response = prompt_request(MODEL_ID, prompt)
    response_tokens = 0
    prompt_tokens = 0
    metadata = response.usage_metadata.candidates_token_count
    if metadata is not None:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
    else:
        print("Metadata returned None, there is no token count this time.")

    # print(response)
    print("User propmt:", prompt)
    print("Prompt tokens: ", prompt_tokens)
    print("Response tokens: ", response_tokens)
    print("Response:")
    print(response.text)


def get_current_timestamp():
    return datetime.now().isoformat() + "Z"


def chat_with_gemini(user_input):
    if user_input.usage_metadata is not None:
        usage_metadata = {
            "usage_token_count": 0,  # Initialize
            "timestamp": get_current_timestamp(),
        }
    return usage_metadata


def token_max(AI_model):
    model_info = client.models.get(model=AI_model)  # """model"""
    prompt_max = model_info.input_token_limit
    response_max = model_info.output_token_limit

    print("Context window:", prompt_max, "tokens")
    print("Max output window:", response_max, "tokens")

    return (prompt_max, response_max)


def token_count(model, prompt):
    prompt_response = client.models.count_tokens(
        model=model,
        contents=prompt,
    )
    return prompt_response


def prompt_request(model, prompt):
    response = client.models.generate_content(model=model, contents=prompt)
    return response


if __name__ == "__main__":
    main()
