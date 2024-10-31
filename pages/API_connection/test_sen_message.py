from openai import OpenAI
from dotenv import load_dotenv
import config


load_dotenv()


client = OpenAI(api_key=config.api_key)

completion = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
    stream=True,
)

for chunk in completion:
    print(chunk.choices[0].delta)
