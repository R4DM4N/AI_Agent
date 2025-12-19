import json
import os
import argparse
from typing import Any 
from dotenv import load_dotenv
from google import genai
from google.genai import types as genai_types
from google.genai import errors as genai_errors

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
    #prompt_reserve = config["default_prompt"]
    print("Model_id: ", model_id)
    #print("default_prompt", prompt_reserve)
    # Get prompt from arguments 
    prompt =  parser_fn()
    
    response = prompt_request(model_id, prompt)
    if response is None or response.usage_metadata is None:
        raise RuntimeError("Metadata returned None, there is no token count this time.")
    prompt_tokens = response.usage_metadata.prompt_token_count or 0
    response_tokens = response.usage_metadata.candidates_token_count or 0

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

def parser_fn(description="Chatbot")-> str:
    parser = argparse.ArgumentParser(
        description=description
    )
    parser.add_argument(
        "prompt", 
        type=str, 
        help="User prompt"
    )
    args = parser.parse_args()
    prompt = args.prompt
    """
    with (open(args.prompt, 'w') if args.prompt is not None
        else contextlib.nullcontext(sys.stdout)) as log:
        log.write('%s' % sum(args.integers))
    """   
    return prompt

def prompt_request(model: str, prompt: str) -> genai_types.GenerateContentResponse| None:
    try:
        prompt_response: genai_types.GenerateContentResponse= client.models.generate_content(
            model=model, 
            contents=prompt
        )
        return prompt_response
    except genai_errors.ClientError as e:
        print(f"DEBUG: Type of exception caught: {type(e)}")
        print(f"DEBUG: Exception details (full error object): {e}")
        # Extract status code using a regular expression from the error string
        match = re.search(r'(\d{3})\s[A-Z_]+', str(e))
        error_code_from_string = int(match.group(1)) if match else None

        if error_code_from_string == 429:
            print("Quota exceeded! Please try again tomorrow")
            # You might want to re-raise the error or handle it differently
            # depending on what you want your program to do.
            return None 
        else:
            # For other ClientErrors, you can still print the full error object
            # or try to access a more general error message if the library provides one.
            print(f"An API error occurred: {e}") # Print the full error object for other ClientErrors
            return None        

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
