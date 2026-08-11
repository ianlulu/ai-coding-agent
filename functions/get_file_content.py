# functions/get_file_content.py

import os
from config import MAX_CHARS


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Get or read the contents of a file returned as a string given a working directory and a file path",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to get files from, relative to the working directory (default is the working directory itself)",
                },
                "file_path": {
                    "type": "string",
                    "description": "The file path to where file to be read lives",
                },
            },
            "required": "file_path",
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs_path: str = os.path.abspath(working_directory) # absolute path of the working directory i.e. starting with root `/` compared to a relative path
        target_file_path: str = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        # Will be True or False:
        valid_target_file_path: bool = os.path.commonpath([working_dir_abs_path, target_file_path]) == working_dir_abs_path # common path should be the same as the absolute working directory path

        # LLM agent file permission guardrails
        if valid_target_file_path is False: 
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory' # we never want the agent to be able to perform any work outside the working directory we give it

        # Check if file_path leads to a file or not
        if os.path.isfile(target_file_path) is False:
            #raise Exception(f'Error: "{directory}" is not a directory')
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            file_content_string_length_check = f.read(1)

            if file_content_string_length_check:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
