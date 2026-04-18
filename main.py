import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError('API key not found')

# argparse use
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str,help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
prompt = parser.parse_args().user_prompt

messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=messages
)

if response.usage_metadata is None:
    raise RuntimeError('Usage Meta Data not found')

print(parser.parse_args().verbose)

if parser.parse_args().verbose is True:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
print("Response:")   
print(response.text)

def main():
    print("Hello from firstaiagent!")


if __name__ == "__main__":
    main()
