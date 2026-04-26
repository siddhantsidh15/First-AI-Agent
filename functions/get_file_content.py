import os

from config import MAX_CHARS

from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file content upto a specific character limit. If the file is outside the permitted directory throw an error",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description= "Relative path of the file to read"
            )
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory, file_path=None):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path

        if valid_target_dir is False:
            raise RuntimeError(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.isfile(target_dir):
            raise RuntimeError(f'Error: File not found or is not a regular file: "{file_path}"')
        
        # read the file
        with open(target_dir, 'r') as f:
            content =  f.read(MAX_CHARS)
            # print(content)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                # print(content)
            return content
        
    except Exception as e:
        return f"Error: {e}"
    return