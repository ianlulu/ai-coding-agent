# functions/get_files_info.py

import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    if os.path.isdir(directory) is False:
        #raise Exception(f'Error: "{directory}" is not a directory')
        return f'Error: "{directory}" is not a directory'

    working_dir_abs_path: str = os.path.abspath(working_directory) # absolute path of the working directory
    target_dir: str = os.path.normpath(os.path.join(working_dir_abs_path, directory))

    # Will be True or False:
    valid_target_dir: bool = os.path.commonpath([working_dir_abs_path, target_dir]) == working_dir_abs_path # common path should be the same as the absolute working directory path

    # LLM agent file permission guardrails
    if valid_target_dir is False:
        # raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory') # we never want the agent to be able to perform any work outside the working directory we give it
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    """
    Without this restriction, the LLM might run amok anywhere on the machine,
    reading sensitive files or overwriting important data.
    This is a very important step that will be baked into every function the LLM can call.
    """

    return f'Success: "{directory}" is within the working directory'
