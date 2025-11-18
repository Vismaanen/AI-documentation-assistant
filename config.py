"""
Configuration file for API / source files and AI prompts.
"""

# provide credentials and configuration details
# API key and endpoint stored by default in environment variables
# provide variable names below
API_ENDPOINT_VAR = 'CHATAI_ENDPOINT'
API_KEY_VAR = 'CHATAI_KEY'


# provide GPT model below
# this is utilized with tokens calculation for performance assessment
GPT_MODEL = "gpt-4o"


# subject script / project directory
PROJECT_DIR = ""
# for a project: determine script / file extensions to be included for analysis
INCLUDED_EXTENSIONS = ['*.py', '*.ps1', '*.sql']
# if there are some files to be omitted: provide in this list
EXCLUDED_FILES = ['config.py']


# AI prompts section
# fine-tune this prompts for later use as needed
# ----------------------------------------------------------------------------------------------------------------------
AI_README_PROMPT = """
Generate complete README.md file code for attached script.  
README.md code must have exactly the same style and structure as an example below, using markdown, icons and badges:

# 📃 <SCRIPT NAME>

## 💫 Updates
YYYY-MM-DD - initial version of the script

## ⚙️ Main functionalities
Describe what script actually does, for example:
- which internal / external resources / APIs it scans,
- processes what kind of data,
- what report files / images it generates,
- if keeps / maintains cache or database(s),
- way of starting a script (task scheduler / cron etc.).

## 🧩 Architecture diagram
Create, describe and present an architecture diagram in Mermaid.

## ➕ Dependencies
List all required libraries, including those that may require installation. Provide a way to install those 
libraries (`pip install ...`). Attach additional details related to security or any other dependencies: 
(for example tokens, API permissions).  

## 🌐 External resources
Describe external resources which script connects (API, databases, SMTP etc.) alongside with network requirements.

## 🏃‍♂️‍➡️ Running script
Present example script usage including arguments and different work modes (if applicable).

## 📝 Configuration options
Describe in detail all configuration files and their attributes (examples below, if applicable):
- output directories,
- API endpoints,
- status maps / logic values,
- monitored customers / report recipients,
- databases,
- data retention settings,
- SMTP / email settings.

### Directories
List all directories script is using with their description and purpose.

### API endpoints
List and describe all API endpoints script is using.

### Identified service statuses
Describe in detail all status maps script is using if there is any.

### Monitored customers
Provide an example of customer / device / report recipients configurations.

### Database
Describe in detail database details and data retention mechanisms.

### SMTP and email messages
Describe SMTP server parameters and templates of outgoing messages (if applicable).

## 📃 Report output
Append a short but functional description of generated reports / charts / logs.

## 📜 License
Project available under license **Apache 2.0**.  
Link to full license text and LICENSE file in repository.

---

Additionally:
- all code samples put in Markdown blocks (````python````),
- Use icons and headers i exact style as provided,
- Generate professional, complete, ready for repository README.md file code for download,
- make sure that README.md file content can be understood by programmers, engineers and IT administrators.

Polish and tidy up all text content and descriptions within file. Always return results as a markdown file format in 
English language.

Script provided for review: 
"""

AI_ANALYSIS_PROMPT = """
You are an expert Python security reviewer. 
Your primary goal is to provide a concise and actionable analysis of the provided Python script(s). 
Analyze the code step-by-step and structure your response in Markdown using the exact headings below. 
For each section, use bullet points to present your findings clearly and succinctly. Provide output in English.

### RESPONSE FORMAT

### 1. Code Review (Security Vulnerabilities)
*   Identify potential security vulnerabilities (e.g., Injection, hardcoded secrets, insecure library usage). Reference CWE where applicable.
*   For each finding, briefly describe the issue and suggest a mitigation.
*   If no significant vulnerabilities are found, state "No significant security vulnerabilities were identified."
*   Example: `- CWE-798 (Use of Hard-coded Credentials): API key is hardcoded on line 15. Mitigation: Store secrets in environment variables or a dedicated secrets management service.`

### 2. Code Validation (Best Practices & Standards)
*   List any major deviations from Python best practices (e.g., PEP 8), security guidelines, or general coding standards.
*   Focus on issues like lack of error handling, missing type hints for critical functions, or overly complex logic that could hide bugs.
*   If the script is generally compliant, state "The script adheres to common best practices and standards."
*   Example: `- Lack of specific exception handling in the `process_data` function could lead to unexpected crashes. Mitigation: Catch specific exceptions instead of a bare `except:`.`

### 3. Affected Systems
*   List all external systems, services, or resources the script interacts with.
*   Categorize each interaction (e.g., Database, File System, External API, OS Command).
*   Example: `- External API: Connects to `api.example.com` for data retrieval.`
*   Example: `- File System: Reads configuration from `/data/config.ini` and writes logs to `/var/log/app.log`.`
*   Example: `- OS Command: Executes the `rsync` command.`

### 4. Affected Data
*   **Data Processed:** Briefly describe the type of data being handled (e.g., User PII, financial records, technical logs, configuration data).
*   **Encryption in Transit:** State if data is encrypted during transfer (e.g., via HTTPS/TLS). (Yes/No/Not Applicable).
*   **Encryption at Rest:** State if data is encrypted when stored. (Yes/No/Not Applicable).
*   **Data Sovereignty:** Note any potential issues related to data locality or cross-border data transfer. If none, state "No specific data sovereignty concerns identified."

### 5. Risks & Mitigations
*   Summarize the most critical risks identified from the points above in a simple list.
*   For each risk, provide a concise description and a clear, actionable mitigation strategy.
*   Example: `- Risk: Credential Leakage. Mitigation: Remove hardcoded credentials from the source code and utilize a secrets manager like HashiCorp Vault or AWS Secrets Manager.`
*   Example: `- Risk: Unreliable data processing. Mitigation: Implement robust error handling and logging to ensure script stability and traceability.

### INPUT
Python script provided for review: 
"""