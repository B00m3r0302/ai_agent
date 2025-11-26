import os
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content 
from functions.run_python import run_python_file
from functions.write_file import write_file
from config import WORKING_DIRECTORY

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    function_name = function_call_part.name

    if not function_call_part.name in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name = function_name,
                    response = {"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIRECTORY
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_map[function_name](**args)},
            )
        ],
    )

