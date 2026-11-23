import os

import requests

API_URL = "https://ollama.com/api/chat"
HEADERS = {"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}

def agent(messages):    
    system_message = {
        "role": "system",
        "content": "You are a helpful legal AI assistant, only provide information that is provided to you in the message history."
    }

    messages.insert(0, system_message)

    file_path = "ediscovery/02_email_Okafor_to_personal_2024-03-14.txt"
    
    with open(file_path, "r") as file:
        file_contents = file.read()

    file_message = {
        "role": "system",
        "content": f"Here are the contents of a file called {file_path}:\n{file_contents}"
    }

    messages.insert(1, file_message)

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
Give a short summary of all emails uploaded.
"""

messages = [{"role": "user", "content": question}]
print(agent(messages))