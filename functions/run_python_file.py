import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional arguments to run the file with",
            ),
        },    
        required=["file_path"],     
    ),
)

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    
    try:
        absolute = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(absolute, file_path))

        if os.path.commonpath([absolute, absolute_file_path]) != absolute:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", absolute_file_path]

        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=absolute,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = []

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")

        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if not result.stdout and not result.stderr:
            output.append("No output produced")
            
        return "\n".join(output)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"