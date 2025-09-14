import os
import subprocess

from google.genai import types


class FunctionTools:
    def __init__(self, working_directory, file_read_max_size, verbose=False):
        self.working_directory = working_directory
        self.file_read_max_size = file_read_max_size
        self.verbose = verbose

    def get_file_content(self, file_path: str) -> str:
        abs_working_dir = os.path.abspath(self.working_directory)
        abs_file_path = os.path.join(abs_working_dir, file_path)

        if not os.path.isfile(abs_file_path):
            return f"Error: The file is not found or not a file: {file_path}"

        try:
            with open(abs_file_path, "r") as f:
                content = f.read(self.file_read_max_size)
                if os.path.getsize(abs_file_path) > self.file_read_max_size:
                    content += f"[...File {file_path} is truncated at {self.file_read_max_size} characters]"
                return content
        except Exception as e:
            return f"Error: There is an error reading the file {file_path}: {e}"

    def write_file(self, file_path: str, content: str) -> str:
        abs_working_dir = os.path.abspath(self.working_directory)
        abs_file_path = os.path.join(abs_working_dir, file_path)
        abs_file_dir = os.path.dirname(abs_file_path)

        if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
            return f"Error: The file is a directory: {file_path}"

        if not os.path.exists(abs_file_dir):
            try:
                os.makedirs(abs_file_dir)
            except Exception as e:
                return (
                    f"Error: There is an error creating the directory {file_path}: {e}"
                )

        try:
            with open(abs_file_path, "w") as f:
                f.write(content)
            return f'Successfully wrote file "{file_path}". ({len(content)} characters written))'
        except Exception as e:
            return f"Error: There is an error writing the file {file_path}: {e}"

    def get_directory_info(self, directory: str = ".") -> str:
        abs_working_dir = os.path.abspath(self.working_directory)
        abs_dir_path = os.path.join(abs_working_dir, directory)

        if not os.path.isdir(abs_dir_path):
            return f"Error: The directory is not found or not a directory: {directory}"

        try:
            files_info = []
            for filename in os.listdir(abs_dir_path):
                file_path = os.path.join(abs_dir_path, filename)
                is_dir = os.path.isdir(file_path)
                file_size = os.path.getsize(file_path) if not is_dir else 0
                files_info.append(
                    f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
                )
            return "\n".join(files_info)
        except Exception as e:
            return f"Error: There is an error reading the directory {directory}: {e}"

    def run_python_file(self, file_path: str, args: list = None) -> str:
        abs_working_dir = os.path.abspath(self.working_directory)
        abs_file_path = os.path.join(abs_working_dir, file_path)

        if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
            return f"Error: The file is a directory: {file_path}"

        if not os.path.isfile(abs_file_path):
            return f"Error: The file is not found: {file_path}"
        if not file_path.endswith(".py"):
            return f"Error: The file is not a Python file: {file_path}"

        try:
            commands = ["python", abs_file_path]
            if args:
                commands.extend(args)
            result = subprocess.run(
                commands,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=abs_working_dir,
            )
            output = []
            if result.stdout:
                output.append(f"stdout: {result.stdout}")
            if result.stderr:
                output.append(f"stderr: {result.stderr}")

            if result.returncode != 0:
                output.append(f"Process exited with return code {result.returncode}")

            return "\n".join(output) if output else "No output from the Python file."
        except Exception as e:
            return f"Error: There is an error running the Python file {file_path}: {e}"

    def get_available_functions(self):
        return types.Tool(
            function_declarations=self.function_declarations(),
        )

    def function_declarations(self) -> list:
        return [
            types.FunctionDeclaration(
                name="get_file_content",
                description=f"Reads and returns the first {self.file_read_max_size} characters of the content from a specified file within the working directory.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "file_path": types.Schema(
                            type=types.Type.STRING,
                            description="The path to the file whose content should be read, relative to the working directory.",
                        ),
                    },
                    required=["file_path"],
                ),
            ),
            types.FunctionDeclaration(
                name="write_file",
                description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "file_path": types.Schema(
                            type=types.Type.STRING,
                            description="Path to the file to write, relative to the working directory.",
                        ),
                        "content": types.Schema(
                            type=types.Type.STRING,
                            description="Content to write to the file",
                        ),
                    },
                    required=["file_path", "content"],
                ),
            ),
            types.FunctionDeclaration(
                name="get_directory_info",
                description=(
                    "Lists files in the specified directory along with their sizes, constrained to the working directory."
                ),
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "directory": types.Schema(
                            type=types.Type.STRING,
                            description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                        ),
                    },
                ),
            ),
            types.FunctionDeclaration(
                name="run_python_file",
                description="Executes a Python file within the working directory and returns the output from the interpreter.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "file_path": types.Schema(
                            type=types.Type.STRING,
                            description="Path to the Python file to execute, relative to the working directory.",
                        ),
                        "args": types.Schema(
                            type=types.Type.ARRAY,
                            items=types.Schema(
                                type=types.Type.STRING,
                                description="Optional arguments to pass to the Python file.",
                            ),
                            description="Optional arguments to pass to the Python file.",
                        ),
                    },
                    required=["file_path"],
                ),
            ),
        ]

    def call_function(self, function_call_part):
        if self.verbose:
            print(
                f" - Calling function: {function_call_part.name}({function_call_part.args})"
            )
        else:
            print(f" - Calling function: {function_call_part.name}")
        function_map = {
            "get_directory_info": self.get_directory_info,
            "get_file_content": self.get_file_content,
            "run_python_file": self.run_python_file,
            "write_file": self.write_file,
        }
        function_name = function_call_part.name
        if function_name not in function_map:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
        args = dict(function_call_part.args)
        if self.verbose:
            print(f"Function args: {args}")
        function_result = function_map[function_name](**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
