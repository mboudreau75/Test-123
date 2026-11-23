import os

import requests

API_URL = "https://ollama.com/api/chat"
HEADERS = {"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}

def agent(messages):
    payload = {
        "model": "gpt-oss:120b",
        "messages": messages,
        "stream": False,
    }
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=300,
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]

question = """
Give a short summary of the emails.
"""

messages = [{"role": "user", "content": question}]
print(agent(messages))