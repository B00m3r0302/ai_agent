import os


def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_target.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_target):
        return f'Error: File "{file_path}" not found.'

    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a python file.'
