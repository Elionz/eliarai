import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory: str, directory: str = ".") -> str:
    absolute = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute, directory))

    if os.path.commonpath([absolute, target_dir]) != absolute:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir):  
        return f'Error: "{directory}" is not a directory'
    
    #return f'Success: "{directory}" is within the working directory'¨

    try:
        items = os.listdir(target_dir)
        lines = []

        for item in items:
            full_path = os.path.join(target_dir, item)

            file_size = os.path.getsize(full_path)
            is_directory = os.path.isdir(full_path)

            line = f"- {item}: file_size={file_size} bytes, is_dir={is_directory}"

            lines.append(line)

            #print(f"{item} is a directory: {is_directory}")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"