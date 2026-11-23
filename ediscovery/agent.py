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

    file_path_two = "ediscovery/03_email_Corvane_recruiter_2024-02-02.txt"
    
    with open(file_path_two, "r") as file:
        file_contents_two = file.read()

    file_message_two = {
        "role": "system",
        "content": f"Here are the contents of a file called {file_path_two}:\n{file_contents_two}"
    }

    messages.insert(2, file_message_two)

    file_path_three = "ediscovery/06_email_Tidewater_Marina_offsite_2024-05-10.txt"
        
    with open(file_path_three, "r") as file:
        file_contents_three = file.read()
    
    file_message_three = {
         "role": "system",
        "content": f"Here are the contents of a file called {file_path_three}:\n{file_contents_three}"
    }
    
    messages.insert(3, file_message_three)

    file_path_four = "ediscovery/08_email_Lindqvist_to_counsel_2024-04-02.txt"
        
    with open(file_path_four, "r") as file:
        file_contents_four = file.read()
    
    file_message_four = {
         "role": "system",
        "content": f"Here are the contents of a file called {file_path_four}:\n{file_contents_four}"
    }
    
    messages.insert(4, file_message_four)

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