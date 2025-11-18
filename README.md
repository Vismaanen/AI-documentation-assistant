# 📃 AI documentation assistant

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## 💫 Updates
2024-05-21 - initial version of the script

## ⚙️ Main functionalities
This script leverages a corporate Generative AI instance to assist developers with code refactoring and documentation. It's an interactive tool designed to automate the creation of project README files and perform detailed code analysis on a file-by-file basis.

- **Scans local project directories** for source code files based on configurable extensions (e.g., `*.py`).
- **Processes source code** by combining it with user-defined prompts.
- **Connects to a corporate AI API** endpoint to submit the code and prompts for processing.
- **Generates `README.md`** for the entire project, providing a comprehensive overview, setup instructions, and architecture.
- **Generates individual Markdown analysis files** for each source code file, containing suggestions for refactoring, optimization, and documentation improvements.
- **Maintains detailed log files** for each run in a local `logs` subdirectory.
- **Does not maintain a cache or database**; each run is a fresh session.
- The script is **started manually from the command line** and prompts the user for the desired mode of operation.

## ➕ Dependencies
The script requires several Python libraries. It also depends on environment variables for secure access to the AI service.

| Library      | Purpose                               | Installation Command           |
|--------------|---------------------------------------|--------------------------------|
| **requests** | For making HTTP requests to the AI API. | `pip install requests`         |
| **tiktoken** | For calculating token count before API call. | `pip install tiktoken` |

You can install all required libraries using the following command:
````bash
pip install requests tiktoken
````

### Security Dependencies
The script requires access to a proprietary AI API. Authentication is handled via an API key. For security reasons, the API key and endpoint URL must be configured as **environment variables**. The names of these variables are defined in the `config.py` file.

-   **API Key**: Set an environment variable (e.g., `MY_AI_API_KEY`) with your key.
-   **API Endpoint**: Set an environment variable (e.g., `MY_AI_ENDPOINT`) with the full URL.

## 🌐 External resources
The script connects to one primary external resource:

-   **Corporate AI API**:
    -   **Purpose**: To process source code and generate documentation/analysis.
    -   **Protocol**: HTTPS
    -   **Network Port**: 443 (standard for HTTPS)
    -   **Endpoint URL**: The URL is not hardcoded. It is retrieved from an environment variable, the name of which is specified in the `config.py` file (see `API_ENDPOINT_VAR`).

Ensure that the machine running the script has outbound internet access to the AI provider's domain on port 443.

## 🏃‍♂️‍➡️ Running script
To run the script, execute it from your terminal using Python. The script will then prompt you to choose a mode of operation.

**Example Usage:**

1.  Navigate to the script's directory.
2.  Run the script:
    ````bash
    python ai_code_assistant.py
    ````
3.  The script will display the available modes and ask for your input:
    ````
    2024-05-21 10:30:00 - INFO - select task to perform
    2024-05-21 10:30:00 - INFO - readme - ask for a README.md for a project
    2024-05-21 10:30:00 - INFO - analyze - ask for a code analysis of project files
    2024-05-21 10:30:00 - INFO - all - perform all requests
    Chosen task [readme / analyze / all]:
    ````
4.  Enter `readme`, `analyze`, or `all` and press Enter to proceed. The script will handle the rest.

## 📝 Configuration options
All configuration is centralized in the `config.py` file. Below is a detailed description of each attribute.

````python
# config.py

# --- Project Files ---
# Directory containing the source code to be analyzed.
PROJECT_DIR = r"C:\path\to\your\project"
# File extensions to include in the analysis (uses rglob pattern).
INCLUDED_EXTENSIONS = ["*.py", "*.js"]
# Specific files to exclude from processing.
EXCLUDED_FILES = ["__init__.py", "config.py"]

# --- AI Prompts & Model ---
# The prompt used for generating the main README.md file.
# The script will append all collected source code to this prompt.
AI_README_PROMPT = "Generate a complete README.md file for the attached project..."
# The prompt used for analyzing individual code files.
# The script will append the code of a single file to this prompt.
AI_ANALYSIS_PROMPT = "Perform a detailed code analysis and suggest refactoring improvements for the following script:"
# The name of the AI model, used by tiktoken to accurately count tokens.
GPT_MODEL = "gemini-1.5-pro-latest" # Example model

# --- API & Security ---
# The NAME of the environment variable storing the API key.
API_KEY_VAR = "MY_AI_API_KEY"
# The NAME of the environment variable storing the API endpoint URL.
API_ENDPOINT_VAR = "MY_AI_ENDPOINT"

````

### Directories
-   **`PROJECT_DIR`**: (Configurable) The root directory of the project you want to analyze. The script scans this directory recursively.
-   **`logs/`**: (Auto-created) Located in the same directory as the script. Stores timestamped log files for each execution.
-   **`AI analysis/`**: (Auto-created) Located inside `PROJECT_DIR`. Stores the individual markdown analysis files generated in `analyze` mode.

### API endpoints
The script does not contain a hardcoded API endpoint.
-   **`API_ENDPOINT_VAR`**: This variable in `config.py` specifies the **name** of the environment variable that holds the API endpoint URL. The script reads this name, then fetches the URL from the system's environment variables.

### Identified service statuses
This script does not use internal status maps. It directly reports the HTTP status codes (200 for success, others for failure) received from the external API.

### Monitored customers
This script is not designed to monitor customers or devices.

### Database
This script is stateless and does not use any database for caching or data retention.

### SMTP and email messages
This script does not have functionalities for sending emails and does not require SMTP configuration.

## 📃 Report output
The script generates human-readable reports in Markdown format, as well as detailed log files.

-   **`README.md`**: (Optional) A single, comprehensive file created in the `PROJECT_DIR`. It is generated based on the `AI_README_PROMPT` and the content of all included project files.
-   **`AI analysis/<filename>.md`**: (Optional) In `analyze` mode, one Markdown file is created for each source code file. Each report contains the AI-generated analysis, refactoring suggestions, or documentation improvements for that specific file.
-   **`logs/<timestamp>_api_checker.log`**: A log file containing detailed, timestamped information about the script's execution, including modes, files found, API requests, token counts, and success or failure messages. This is useful for debugging.

## 📜 License

Project is available under terms of **[Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)**.  
Full license text can be found in file: [LICENSE](./LICENSE).

---

© 2025 **Vismaanen** — simple coding for simple life