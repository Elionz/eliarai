import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Read file contents",
            ),
        },
    required=["file_path"],
    ),
)

def get_file_content(working_directory: str, file_path: str) -> str:

    base = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(base, file_path))

    #print(base)
    #print(target)
    #print(os.path.commonpath([base, target]))

    try:
        common = os.path.commonpath([base, target])
        if common != base:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    

        with open(target, "r") as f:
            MAX_CHARS = 10000
            content = f.read(MAX_CHARS)
            extra = f.read(1)
            if extra:
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    
    except Exception as e:
        return f"Error: {e}"