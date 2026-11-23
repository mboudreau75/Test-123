import os
import requests

API_URL = 'https://ollama.com/api/chat'
MODEL = 'gpt-oss:20b'
HEADERS = {'Authorization': 'Bearer ' + os.environ['OLLAMA_API_KEY']}

# def list_files(path):
#     try:
#         return '\n'.join(os.listdir(path))
#     except Exception as e:
#         return f"Error: {e}"

list_files_tool = {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "Use this when the user wants to list files in the current working directory by default, or in a named directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path of the directory on which to list the files."}
            },
            "required": ["path"]
        }
    }
}

# def read_file(path):
#     try:
#         with open(path) as f:
#             return f.read()
#     except Exception as e:
#         return f"Error: {e}"

read_file_tool = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Use this when the user wants read a file.",
        "parameters": {
            "type": 'object',
            'properties': {
                'path': {'type': 'string', 'description': 'The path of the file to read.'}
            },
            'required': ['path']
        }
    }
}

write_file_tool = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Use this when the user wants write a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path with filename and extension of the file to write. Only use .txt files."},
                "content": {"type": "string", "description": "the contents of the file."}
            },
            "required": ["path", "contents"]
        }
    }
}

edit_file_tool = {
    'type': 'function',
    'function': {
        'name': 'edit_file',
        'description': 'Use this to replace text in a file. Replaces old_content with new_content. old_content must appear exactly once in the file. Saves edited document as new_filename under the same directory. old_str must appear at least once in the file. If the file at path does not exist, it will be created with new_content as its contents (pass an empty string for old_content). Never overwrite the original file.',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {'type': 'string', 'description': 'The path of the file to edit.'},
                'old_content': {'type': 'string', 'description': 'The original content of the file.'},
                'new_content': {'type': 'string', 'description': 'The content of the file to replace the old_content.'}
            },
            'required': ['path', 'old_content', 'new_content']
        }
    }
}

save_file_tool = {
    'type': 'function',
    'function': {
        'name': 'edit_file',
        'description': 'Use this to save file.  Never overwrite the original file.',
        'parameters': {
            'type': 'object',
            'properties': {
                "path": {"type": "string", "description": "The path of the file to be saved."},
                "original_filename": {"type": "string", "description": "Filename of the original document being edited"},
                "new_filename": {"type": "string", "description": "Filename for the new edited document"},
                "save_directory": {"type": "string", "description": "Directory where the new document will be saved."}
            },
            'required': ['path', 'old_content', 'new_content', 'new_filename', 'save_directory']
        }
    }
}

qualification_tool = {
    "type": "function",
    "function": {
        "name": "qualification",
        "description": "Use this when searching for USCIS regulations to determine whether the applicant qualifies for L-1 visa status and, if so, which category of L-1 status the applicant qualifies under.",
        "parameters": {
            "type": "objects",
            "properties": {
                "path": {"type": "string", "description": "the path of the files containing L-1 regulations to review"},
                "determination": {"type": "string", "description": "the decision of whether the applicant qualifies for L-1 visa status"}
            },
            "required": ['path', 'determination']
        }
    }
}

def agent(messages):
    tools = [list_files_tool, read_file_tool, write_file_tool, edit_file_tool, qualification_tool]

    payload = {
        "model": "gpt-oss:20b",
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
    message = data["message"]
    return message

tool_called = True
messages = [
    {"role": "user", 
    #  This is the prompt asking the AI to do something with the tools available.
     "content": "Use the uploaded files to draft a support letter for a U.S. L-1 nonimmigrant visa petition for the specific visa category referenced within. Search for and incorporate the USCIS regulations relevant to the specified visa type. Save the final letter to the same directory as 'Boudreau_Matthew_L-1_Support_Letter'. Never overwrite the contents of the original files."}
]
while tool_called:
    message = agent(messages)
    print(message)
    tool_called = "tool_calls" in message

    if tool_called:
        print("tool called!")
        tool_calls = message["tool_calls"]
        tool_call = tool_calls[0]

        function_name = tool_call["function"]["name"]
        function_arguments = tool_call["function"]["arguments"]

        if function_name == "list_files":
            path = "."
            if "path" in function_arguments:
                path = function_arguments["path"]
            print(f"arguments for list_files: {path}")
            files = "\n".join(os.listdir(path))
            output = files

        if function_name == "read_file":
            path = function_arguments["path"]
            with open(path, "r") as file:
                file_content = file.read()
            output = file_content

        if function_name == "write_file":
            path = function_arguments["path"]
            content = function_arguments["content"]
            #code directing where "content" is meant to be written.
            with open(path, "w") as file:
                file.write(content)

            output = f"File written to {path} with content: {content}"

        if function_name == "edit_file":
            path = function_arguments ["path"]
            old_content = function_arguments ["old_content"]
            new_content = function_arguments ["new_content"]
            
            if not os.path.exists(path):
                with open(path, "w") as file:
                    file.write(new_filename)
            with open(path, "r") as file:
                file.read()
            with open(path, "w") as file:
                file.write(content.replace(old_content, new_content))

        if function_name == "save_file_tool":
            path = function_arguments ["path"]

            new_filename = function_arguments["new_filename"]
            save_directory = function_arguments["save_directory"]
        
        if function_name == "determination_tool":
            path = function_arguments ["path"]
            determination = function_arguments ["determination"]
            with open(path, "r") as file:
                file_content = file.read()


        tool_message = {
            "role": "tool",
            "content": f"The output of tool {function_name} is: {output}"
        }
        messages.append(tool_message)
    else:
        ai_message = {
            "role":  message["role"],
            "content": message["content"]
        }
        messages.append(ai_message)

# last_message = messages[-1]
# import pprint
# printer = pprint.pprint

print(messages)
