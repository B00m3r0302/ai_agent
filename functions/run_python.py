import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_target.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_target):
        return f'Error: File "{file_path}" not found.'

    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    if isinstance(args, str):
        args = [args]

    commands = ["python", abs_target, *args]
    
    if args:
        commands.extend(args)

    result = subprocess.run(
        commands, capture_output=True, cwd=abs_working_dir, timeout=30
    )
    try:
        output = f"STDOUT: {result.stdout.decode('utf-8')} | STDERR: {result.stderr.decode('utf-8')}"
        if result.stdout.decode("utf-8") == "" and result.stderr.decode("utf-8") == "":
            output = "No output produced"
        if result.returncode != 0:
            output += f" Process exited with code {result.returncode}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file along with any additional args that are passed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to run the file from from, relative to the working directory. If not provided, runs the file in the working directory itself.",
            ),
            "file_path": types.Schema(
                description="The path of the file to execute."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional args to include."
            )
        },
    ),
)
