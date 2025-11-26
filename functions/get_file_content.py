import os
import config
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read"{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file, "r") as f:
            file_content_string = f.read()
            if len(file_content_string) > config.MAX_CHARS:
                return file_content_string[
                    :10001
                ], f'[...File "{file_path}" truncated at 10000 characters]'
            else:
                return file_content_string
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of the file specified up to 10000 characters and appends a message if the content is longer than 10000 characters after truncating it.",  
        parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to get the file content from  from, relative to the working directory. If not provided, it looks for the file in the working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get the content from."
            )
        },
    ),
)
