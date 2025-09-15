import time
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
        self.messages = []

    def generate_content(self, prompt):
        max_iters = self.max_iterations
        self.messages.append(
            types.Content(role="user", parts=[types.Part(text=prompt)])
        )

        for _ in range(0, max_iters):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=self.messages,
                    config=types.GenerateContentConfig(
                        tools=[self.function_tools.get_available_functions()],
                        system_instruction=system_prompt,
                    ),
                )
                if self.verbose:
                    print(f"User prompt: {prompt}")
                    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                    print(
                        "Response tokens:",
                        response.usage_metadata.candidates_token_count,
                    )

                if response.candidates:
                    # .candidates: This attribute holds a list of potential responses from the model.
                    # Usually, there's only one response in this list, but the API supports providing
                    # multiple alternatives.
                    candidate = response.candidates[0]
                    if self.verbose:
                        print(candidate.content)
                    if candidate.content is None:
                        continue
                    self.messages.append(candidate.content)

                if response.function_calls:
                    for function_call_part in response.function_calls:
                        result = self.function_tools.call_function(function_call_part)
                        # print(result)
                        self.messages.append(result)
                else:
                    if response.candidates:
                        text_response = "".join(
                            part.text
                            for part in response.candidates[0].content.parts
                            if part.text is not None
                        )
                        print(text_response)
                    break
            except Exception as e:
                print(f"Error: {e}")
                print("Retrying in 10 seconds...")
                time.sleep(10)
