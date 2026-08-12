# functions/write_file.py

import os


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write content into a file at the given working directory, file path, and content",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
                "file_path": {
                    "type": "string",
                    "description": "The file path to where the content will be written",
                },
                "content": {
                    "type": "string",
                    "description": "The content to be written in a file",
                }
            },
            "required": ["file_path", "content",],
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs_path: str = os.path.abspath(working_directory) # get an absolute path (i.e. from root `/`) from a relative path (i.e. `~/dev`)
        target_file_path: str = os.path.normpath( # normalize a path (handles things like `..` (go back 1 directory))
            os.path.join(working_dir_abs_path, file_path) # join two paths together safely (handles slashes)
        )

        # Will be True or False:
        valid_target_file_path: bool = os.path.commonpath([working_dir_abs_path, target_file_path]) == working_dir_abs_path

        # LLM agent file permission guardrails:
        if not valid_target_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Check if file_path leads to a directory or not:
        if os.path.isdir(file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Make sure that all parent directories of the `file_path` exist:
        os.makedirs( # create a directory, along with any necessary parent directories (note the optional `exist_ok` argument)
            os.path.dirname(target_file_path), exist_ok=True # get the parent directory of a given path
        )
        # Open the file:
        with open(target_file_path, "w") as f: # open a file for reading or writing - "w" for write mode
            f.write(content) # write a string to a text file

        # Success message:
        return f'Succesfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing file "{file_path}": {e}'
