import os
import glob
import subprocess

import requests

API_URL = 'https://ollama.com/api/chat'
MODEL = 'gpt-oss:20b'
HEADERS = {'Authorization': 'Bearer ' + os.environ['OLLAMA_API_KEY']}

def list_files(path):
    try:
        return '\n'.join(os.listdir(path))
    except Exception as e:
        return f"Error: {e}"

list_files_tool = {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "Use this when the user wants to list files from a specified folder.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path of the folder to list the files from."}
            },
            "required": ["path"]
        }
    }
}

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"

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

# run_python_tool = {
#     "type": "function",
#     "function": {
#         "name": "run_python_file",
#         "description": "Use this when the user wants to run a python file",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "path": {"type": "string", "description": "The path of the python file to run"},
#             },
#             "required": ["path"]
#         }
#     }
# }

def agent(messages):
    tools = [list_files_tool, read_file_tool, write_file_tool]

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
    "content": f"""
     Use the files in the Final_Project_Documents folder to determine whether a given beneficiary qualifies for a U.S. L-1 nonimmigrant visa and, if so, which L-1 category the applicant qualifies under. 
     Draft a support letter for a U.S. L-1 nonimmigrant visa petition based on the following parameters: 
     - Use the template_L1_sl.txt file contents for the support letter format.
     - Only use the specific visa category the applicant qualifies for based on the files and incorporate an explanation for the Beneficiary qualification based on the USCIS regulations relevant to the specified visa type.
     - Save the drafted support letter as 'Boudreau_Matthew_L-1_Support_Letter.txt' in the Final_Project_Documents folder. 
     - Never overwrite the contents of the original files."
     - Include description of the Petitioner and ultimate parent company business operations.
     - Include description of the job duties listed in the files for both roles in paragraph form.
     - Include description of how each position meets each of the USCIS requirements for the visa category the Beneficiary qualifies for.
     - Include list of any positions reporting to the Beneficiary in both the U.S. Position and Qualifying Foreign Position in the relevant sections.
     - Include references to each file utilized in making a determination for content as numbered exhibits based on the order of use.
     - Include the filing address for the L-1 petition based on the location of the U.S. Petitioner office location in the field indicated in the template.
     """
     }
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
            files = glob.glob(f"{path}/*")
            output = files
            print(files)

        if function_name == "read_file":
            path = function_arguments["path"]
            with open(path, "r", encoding="cp1252") as f:
                file_content = f.read()
            output = file_content

        if function_name == "write_file":
            path = function_arguments["path"]
            content = function_arguments["content"]
            #code directing where "content" is meant to be written.
            with open(path, "w") as f:
                f.write(content)

            output = f"File written to {path} with content: {content}"

        # if function_name == "run_python_file":
        #     path = function_arguments["path"]
        #     # Run the command and capture output
        #     result = subprocess.run(['python', path], capture_output=True, text=True, check=True)
        #     # Access the captured stdout
        #     output = f"output of python {path}: {result}"

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

last_message = messages[-1]
import pprint
printer = pprint.pprint

printer(messages)
