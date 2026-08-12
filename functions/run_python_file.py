# functions/run_python_file.py

import os
import subprocess
from subprocess import CompletedProcess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run or execute a Python file given a working directory, file path, and arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
                "file_path": {
                    "type": "string",
                    "description": "The file path to where the Python file to be executed lives",
                },
                "args": {
                    "type": "array",
                    "description": "Optional arguments to be passed to the function. The type is an array whose items are strings"
                },
            },
            "required": "file_path",
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs_path: str = os.path.abspath(working_directory) # get an absolute path (i.e. from root `/`) from a relative path (i.e. `~/dev`)
        target_file_path: str = os.path.normpath( # normalize a path (handles things like `..` (go back 1 directory))
            os.path.join(working_dir_abs_path, file_path) # join two paths together safely (handles slashes) - this is the absolute path to the passed file_path argument
        )
        
        # Will be True or False:
        valid_target_file_path: bool = os.path.commonpath([working_dir_abs_path, target_file_path]) == working_dir_abs_path
        
        # LLM agent file permission guardrails:
        if not valid_target_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if file_path leads to a regular file or not:
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Check if file is a Python file or not:
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Command list to run:
        command: list[str] = ["python", target_file_path]

        # Add any args (arguments) provided to the command list:
        if args is not None:
            command.extend(args)

        # Run the command by spinning up a subprocess:
        run: CompletedProcess = subprocess.run(
            command, # pass the command list that was instantiated earlier
            capture_output=True, # set capture output (i.e. stdout & stderr) to True
            cwd=working_dir_abs_path, # set current working directory to the proper absolute path
            timeout=30, # set timeout to 30 seconds to prevent infinite execution
            text=True # decode the output to strings, rather than bytes
        )

        # Exit with this string:
        output_string: str = ""

        # If the process exited with a non-zero `returncode`:
        if run.returncode != 0:
            output_string += f"Process exited with code {run.returncode}\n"

        # If stdout & stderr contained no output:
        if not run.stdout and not run.stderr:
            output_string += "No output produced\n"
        elif run.stdout and not run.stderr: # If only stdout contains output:
            output_string += f"STDOUT: {run.stdout}\n"
        elif not run.stdout and run.stderr: # If only stderr contains output:
            output_string += f"STDERR: {run.stderr}\n"
        else: # Otherwise, include any stdout or stderr text:
            output_string += f"STDOUT: {run.stdout}\n"
            output_string += f"STDERR: {run.stderr}\n"

        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
