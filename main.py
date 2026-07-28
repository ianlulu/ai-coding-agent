import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() # load environment variables from .env
api_key = os.environ.get("OPENROUTER_API_KEY") # read API key
if api_key is None:
	raise RuntimeError("API key not found.") # error message if not found

# create an OpenAI client:
client = OpenAI(
     base_url="https://openrouter.ai/api/v1",
     api_key=api_key,
)

def main():
    # print("Hello from ai-coding-agent!")
    model: str = "openrouter/free" # specific LLM being used
    messages: list[dict] = [
         {
              "role": "user",
              "content": "Hello World!",
         }
    ]

    chat = client.chat.completions.create(model=model, messages=messages)
    print(chat.choices[0].message.content)


if __name__ == "__main__":
    main()
