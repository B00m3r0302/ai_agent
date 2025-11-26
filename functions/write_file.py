import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        if not os.path.exists(os.path.dirname(target_dir)):
            os.makedirs(os.path.dirname(target_dir))
            with open(target_dir, "w") as f:
                f.write(content)
        else:
            with open(target_dir, "w") as f:
                f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content to the specified file if it exists and if it does not exist creates the file and writes the content to it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to write to the file from, relative to the working directory. If not provided, writes to the file in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to write to the file"
            )
        },
        required=["file_path", "content"]
    ),
)
