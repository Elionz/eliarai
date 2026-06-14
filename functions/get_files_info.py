import os


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