# Gemini Agent CLI

This project is a Python-based interactive command-line interface (CLI) that allows you to chat with a Google Gemini model. The agent is equipped with a set of tools to interact with the local filesystem, including reading, writing, listing files, and executing Python scripts.

## Features

- **Interactive Chat**: Engages in a continuous conversation, accepting prompts from the user in a loop.
- **Gemini Powered**: Utilizes Google's Gemini models for powerful conversational AI and function calling.
- **Filesystem Tools**: Comes with built-in tools for:
  - Listing directory contents.
  - Reading from files.
  - Writing to files.
  - Executing Python scripts.
- **Configuration**: Easily configured using a `.env` file for your API key and model choice.

## Requirements

- Python 3.13+
- A Google Gemini API Key. You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd gemini-agent
    ```

2.  **Install dependencies:**
    ```bash
    pip install google-genai python-dotenv
    ```

3.  **Create an environment file:**
    Create a file named `.env` in the root of the project and add your configuration:
    ```env
    # Your Google Gemini API Key
    GEMINI_API_KEY="YOUR_API_KEY_HERE"

    # The model you want to use (e.g., gemini-1.5-flash)
    GEMINI_AI_MODEL="gemini-1.5-flash"
    ```

## Usage

Run the agent from your terminal. You must specify a working directory, which is the folder the agent is allowed to operate in.

```bash
python genagent.py -w /path/to/your/workspace
```

This will start the interactive session, and you can start typing your prompts.

### Command-Line Arguments

- `-w`, `--working_dir` ( **Required**): The absolute or relative path to the directory where the agent can read, write, and execute files.
- `-v`, `--verbose`: Enables verbose output, showing more details about the agent's function calls and API interactions.
- `[prompt]`: You can provide an optional initial prompt directly from the command line.

### Example

```bash
# Start the agent with a working directory and an initial prompt
python genagent.py -w ./my-project "List all the files in the current directory."

# Start the agent in interactive mode only
python genagent.py -w /Users/me/Documents/Code/test-project
```

### Exiting

To stop the agent, press `Ctrl+C`.
