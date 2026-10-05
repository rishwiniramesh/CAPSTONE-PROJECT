import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()

token = os.getenv("HF_TOKEN")

if not token:
    raise RuntimeError("HF_TOKEN was not found in .env")


client = InferenceClient(
    api_key=token,
)

response = client.chat.completions.create(
    model="Qwen/Qwen3-4B-Thinking-2507",
    messages=[
        {
            "role": "user",
            "content": "Say hello in one sentence.",
        }
    ],
)

print(response.choices[0].message.content)