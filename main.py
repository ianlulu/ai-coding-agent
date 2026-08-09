import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv() # load environment variables from .env
api_key = os.environ.get("OPENROUTER_API_KEY") # read API key
if api_key is None:
	raise RuntimeError("API key not found.") # error message if not found

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")

# verbose optional command-line argument
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()
# Now we can access `args.user_prompt`

# create an OpenAI client:
client = OpenAI(
     #base_url="https://openrouter.ai/api/v1",
     #api_key=api_key,
     base_url="http://192.168.0.64:1234/v1",
     api_key="lmstudio",
)

def main():
    #print("Hello from ai-coding-agent!")
    #model: str = "openrouter/free" # specific LLM being used
    model = "qwythos-9b-v2"
    messages: list[dict] = [
         {
              "role": "user",
              "content": args.user_prompt,
         },
    ]

    chat = client.chat.completions.create(model=model, messages=messages)

    if chat.usage is not None:
        if args.verbose is True:
             print(
                  f"User prompt: {messages[0]["content"]}\n"
                  f"Prompt tokens: {chat.usage.prompt_tokens}\n"
                  f"Response tokens: {chat.usage.completion_tokens}"
               )
             
        print(
             "Response:\n"
             f"{chat.choices[0].message.content}"
          )

          
    else:
         raise RuntimeError("Failed API request. No usage property found.")


if __name__ == "__main__":
    main()
