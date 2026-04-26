import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Run the python file provided in the specific directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path of the Python file to execute"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that has to be written in the file"
            )
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path

        # is a directory then cannot write
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        if valid_target_dir is False :
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        parent_dir = os.path.dirname(target_dir)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        with open(target_dir, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
