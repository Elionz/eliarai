import os, argparse, sys
from dotenv import load_dotenv
from google.genai import types
from google import genai
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("API is missing!!")

client = genai.Client(api_key=api_key)



def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()


    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    if args.verbose is True:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]),
        )

        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)


        if response.usage_metadata is None:
            raise RuntimeError("API missing...")
    
        if args.verbose is True:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if response.function_calls:
            function_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)

                if not function_call_result.parts:
                    raise Exception("Empty")
            
                if function_call_result.parts[0].function_response is None:
                    raise Exception("No details found")

                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("No data found")
            
                function_results.append(function_call_result.parts[0])
            
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=function_results))
            
        else:
            print(response.text)
            break
    else:
        print("Maximum iterations reached without finishing")
        sys.exit(1)



if __name__ == "__main__":
    main()