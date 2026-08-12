import os
import argparse
import json
import sys

from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM_PROMPT
from call_function import available_functions, call_function


def main():
    load_dotenv() # load environment variables from .env
    api_key = os.environ.get("OPENROUTER_API_KEY") # read API key
    if api_key is None:
        raise RuntimeError("API key not found.") # error message if API key not found

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")

    # Verbose optional command-line argument:
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    # Now we can access `args.user_prompt`:

    # Create an OpenAI client:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        #base_url="http://192.168.0.64:1234/v1",
        #api_key="lmstudio",
    )

    #print("Hello from ai-coding-agent!")
    model: str = "openrouter/free" # specific LLM being used
    #model = "qwythos-9b-v2"
    messages: list = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20): # call the model, handle responses, etc. in 20 turns
        chat = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=available_functions, # function written for the agent
            #temperature=0,
        )

        if chat.usage is not None:
            if args.verbose is True:
                print(
                    f"User prompt: {messages[0]["content"]}\n"
                    f"Prompt tokens: {chat.usage.prompt_tokens}\n"
                    f"Response tokens: {chat.usage.completion_tokens}\n"
                )

            message = chat.choices[0].message
            messages.append(message)

            if message.tool_calls:
                for tool_call in message.tool_calls:
                    function_args = json.loads(tool_call.function.arguments or "{}")
                    result_message = call_function(tool_call, function_args)
                    print(f"Calling function: {tool_call.function.name}({function_args})")
                    if result_message["content"] is None:
                        raise Exception("Error: there is no content in the resulting message.")
                    if args.verbose:
                        print(f"-> {result_message['content']}")

                    messages.append(result_message)
            else:
                print(
                    "Response:\n"
                    f"{message.content}"
                )

                break
    else:
        print(f"Error: took too many iterations. Exiting with error code 1")
        sys.exit(1)


if __name__ == "__main__":
    main()
