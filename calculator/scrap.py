import os

import requests

API_URL = "https://ollama.com/api/chat"
HEADERS = {"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}

tool_schema = {
    "type": "function",
    "function": {
        "name": "getsenator",
        "description": "Use this when listing the names of senior and junior U.S. senators for the state provided.",
        "parameters": {
            "type": "objects",
            "properties": {
                "senior": {"type": "string", "description": "the senior senator to list"},
                "junior": {"type": "string", "description": "the junior senator to list"}
            },
            "required": []
        }
    }
}

def agent(messages):

    tools = [
        tool_schema
    ]

    payload = {
        "model": "gpt-oss:120b",
        "messages": messages,
        "stream": False,
        "tools": tools
    }
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=300,
    )
    response.raise_for_status()
    data = response.json()
        
    import pprint
    printer = pprint.pprint
    printer(data)
    
    message = data["message"]

    if "tool_calls" in message:
        print("we got a tool call!")
    else:
        print("womp womp, no tool call ...")
    
    return data["message"]["content"]

messages = [{"role": "user", "content": "Please list the names of the current senators for the state of Massachusetts."}]
print(agent(messages))