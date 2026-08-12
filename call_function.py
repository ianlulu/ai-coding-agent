#
# available functions for the agent

import json
import inspect

from collections.abc import Callable
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}({function_args})")

    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if function_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }

    #function_args["working_directory"] = "./calculator"

    func = function_map[function_name]
    sig = inspect.signature(func).parameters
    #new_dict: dict = {}
    filtered: dict = {k: v for k, v in function_args.items() if k in sig}

    filtered["working_directory"] = "./calculator"

    #result = function_map[function_name](**function_args)
    result = function_map[function_name](**filtered)

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }
