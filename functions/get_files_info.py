# functions/get_files_info.py

import os


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs_path: str = os.path.abspath(working_directory) # absolute path of the working directory
        target_dir: str = os.path.normpath(os.path.join(working_dir_abs_path, directory))

        if os.path.isdir(target_dir) is False:
            #raise Exception(f'Error: "{directory}" is not a directory')
            return f'Error: "{target_dir}" is not a directory'
        
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

        # List contents of valid target directory:
        list_dir: list = os.listdir(target_dir)
        content: list[str] = []
        """
        if target_dir == ".":
            content = "Result for current directory:"
        else:
            content = f"Result for '{target_dir}' directory:"
        """
        item_name: str = ""
        item_file_size: int = 0
        item_is_dir: bool = False
        item_info: str = ""
        item_path: str = ""
        files_info: str = ""

        for item in list_dir:
            item_name = item
            item_path = os.path.join(target_dir, item_name)
            item_file_size = os.path.getsize(item_path)
            item_is_dir = os.path.isdir(item_path)
            item_info = f"- {item_name}: file_size={item_file_size} bytes, is_dir={item_is_dir}"

            content.append(item_info)
            files_info = "\n".join(content)

        #return f'Success: "{directory}" is within the working directory'
        return files_info
    except Exception as e:
        return f"Error listing files {e}"
