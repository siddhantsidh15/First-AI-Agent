import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.call_function import available_functions, call_function
from config import MODEL, MAX_ITERATIONS




def main():
    try:
        # argparse use
        parser = argparse.ArgumentParser(description="AI Code Assistant")
        parser.add_argument("user_prompt", type=str,help="User prompt")
        parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

        args = parser.parse_args()

        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")

        if api_key is None:
            raise RuntimeError('API key not found')
        
        client = genai.Client(api_key=api_key)
        messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

        if args.verbose:
            print(f"User prompt: {args:user_prompt}\n")

        for _ in range(MAX_ITERATIONS):
            try:
                final_response = generate_content(client, messages, args.verbose)
                if final_response:
                    print("Final Response:")
                    print(final_response)
                    return
            except Exception as e:
                print(f"Error in generate_content: {e}")

        print(f"Maximum iterations ( {MAX_ITERATIONS}) reached")
        sys.exit(1)
        
    except Exception as e:
        print(f"Error: {e}")

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
            model=MODEL,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )

    if response.usage_metadata is None:
        raise RuntimeError('Usage Meta Data not found')
    
    if verbose is True:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for item in response.candidates:
            if item.content: 
                messages.append(item.content)

    # only return statement in the entire function
    if not response.function_calls:
        return response.text
    
    # we are only performing operations on response we will get
    function_responses = []
    result = ""
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        if verbose is True:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])

    # see we are not returning anything here, we are only appending our messages
    messages.append(types.Content(role="user",
                                  parts=function_responses))

    
if __name__ == "__main__":
    main()
