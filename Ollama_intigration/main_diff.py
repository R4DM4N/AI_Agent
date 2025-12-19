import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from datetime import datetime
from pydantic import BaseModel

def get_current_timestamp():
    return datetime.utcnow().isoformat() + "Z"
    
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

print(response.text)
#print(response)
def chat_with_gemini(user_input):
        if usage_metadata is not None:
            usage_metadata = {
            "usage_token_count": 0, # Initialize
            "timestamp": get_current_timestamp(),
        }
    


                         
def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
