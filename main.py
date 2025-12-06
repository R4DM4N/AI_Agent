import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from datetime import datetime

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise Run timeError("api_key not found")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        usage_metadata=GeneratContentResponseUsageMetadata
    )

    #print(response)
    print(response.text)

def get_current_timestamp():
    return datetime.now().isoformat() + "Z"


def chat_with_gemini(user_input):
        if usage_metadata is not None:
            usage_metadata = {
            "usage_token_count": 0, # Initialize
            "timestamp": get_current_timestamp(),
        }
    
main()


if __name__ == "__main__":
    main()
