import os
import argparse
from dotenv import load_dotenv

from gemini_client import GeminiClient

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_AI_MODEL = os.getenv("GEMINI_AI_MODEL")
FILE_READ_MAX_SIZE = int(os.getenv("FILE_READ_MAX_SIZE", "1000"))


print(f"GEMINI_API_KEY: {GEMINI_API_KEY}")
print(f"GEMINI_AI_MODEL: {GEMINI_AI_MODEL}")


def main():
    parser = argparse.ArgumentParser(description="Gemini Agent CLI")
    parser.add_argument("-w", "--working_dir", help="Working directory for the agent")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    parser.add_argument("prompt", nargs="*", help="The initial prompt for the agent")
    args = parser.parse_args()

    working_dir = args.working_dir
    verbose = args.verbose
    initial_prompt = " ".join(args.prompt)

    if not working_dir:
        print("Please specify working directory with -w or --working_dir")
        exit(1)

    if verbose:
        print(f"Working directory: {working_dir}")

    gen_client = GeminiClient(
        api_key=GEMINI_API_KEY,
        model_name=GEMINI_AI_MODEL,
        working_directory=working_dir,
        file_read_max_size=FILE_READ_MAX_SIZE,
        verbose=verbose,
    )

    # If an initial prompt is provided, run it
    if initial_prompt:
        if verbose:
            print(f"Initial prompt: {initial_prompt}")
        gen_client.generate_content(initial_prompt)

    # Enter interactive loop
    try:
        while True:
            prompt = input("\nPrompt: ")
            if not prompt.strip():
                continue
            gen_client.generate_content(prompt)
    except KeyboardInterrupt:
        print("\nExiting.")


if __name__ == "__main__":
    main()
