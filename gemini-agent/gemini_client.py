from google import genai
from google.genai import types

from prompts import system_prompt
from function_tools import FunctionTools


class GeminiClient:
    max_iterations = 20

    def __init__(
        self, api_key, model_name, working_directory, file_read_max_size, verbose=False
    ):
        self.client = genai.Client(api_key=api_key)
        self.model = model_name
        self.verbose = verbose
        self.function_tools = FunctionTools(working_directory, file_read_max_size)

    def generate_content(self, prompt):
        max_iters = self.max_iterations
        messages = [
            types.Content(role="user", parts=[types.Part(text=prompt)]),
        ]
        for _ in range(0, max_iters):
            response = self.client.models.generate_content(
                model=self.model,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[self.function_tools.get_available_functions()],
                    system_instruction=system_prompt,
                ),
            )
            if self.verbose:
                print(f"User prompt: {prompt}")
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print(
                    "Response tokens:", response.usage_metadata.candidates_token_count
                )

            if response.candidates:
                for candidate in response.candidates:
                    if self.verbose:
                        print(candidate.content)
                    if candidate.content is None:
                        continue
                    messages.append(candidate.content)

            if response.function_calls:
                for function_call_part in response.function_calls:
                    result = self.function_tools.call_function(function_call_part)
                    # print(result)
                    messages.append(result)
            else:
                print(response.text)
                break
