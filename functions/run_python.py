import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_target.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_target):
        return f'Error: File "{file_path}" not found.'

    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    commands = ["python", abs_target, *args]
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
