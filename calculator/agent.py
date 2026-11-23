import os

import requests

API_URL = "https://ollama.com/api/chat"
HEADERS = {"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}

tool_schema = {
    "type": "function",
    "function": {
        "name": "add2",
        "description": "Use this when adding two numbers together.",
        "parameters": {
            "type": "objects",
            "properties": {
                "arg1": {"type": "string", "description": "the first number to add"},
                "arg2": {"type": "string", "description": "the second number to add"}
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

messages = [{"role": "user", "content": "Hello program"}]
print(agent(messages))