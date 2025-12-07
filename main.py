import json
import os
from typing import Any 
from dotenv import load_dotenv
from google import genai
from google.genai import types as genai_types

# from google.genai import types
from datetime import datetime

_ = load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")
client = genai.Client(api_key=api_key)

def main():
    # Get settings from config
    config= load_config()
    model_id= config["model_id"]
    prompt = config["default_prompt"]

    response = prompt_request(model_id, prompt)

    useage = response.usage_metadata
    if useage is None:
        raise RuntimeError("Metadata returned None, there is no token count this time.")

    prompt_tokens = useage.prompt_token_count or 0
    response_tokens = useage.candidates_token_count or 0

    # print(response)
    print("User propmt:", prompt)
    print("Prompt tokens: ", prompt_tokens)
    print("Response tokens: ", response_tokens)
    print("Response:")
    print(response.text)

def load_config(config_path: str="config.json") -> dict[str, Any]:
    with open(config_path, "r") as f:
        return json.load(f)

def get_current_timestamp()-> str:
    return datetime.now().isoformat() + "Z"

def prompt_request(model: str, prompt: str) -> genai_types.GenerateContentResponse:
    prompt_response: genai_types.GenerateContentResponse= client.models.generate_content(model=model, contents=prompt)
    return prompt_response

def token_max(AI_model: str) -> tuple[int | None, int | None]:
    model_info: genai_types.Model = client.models.get(model=AI_model)
    prompt_max: int | None = model_info.input_token_limit
    response_max: int | None = model_info.output_token_limit

    print("Context window:", prompt_max, "tokens")
    print("Max output window:", response_max, "tokens")

    return (prompt_max, response_max)

def token_count(model: str, prompt: str):
    prompt_response = client.models.count_tokens(
        model=model,
        contents=prompt,
    )
    return prompt_response

if __name__ == "__main__":
    main()
