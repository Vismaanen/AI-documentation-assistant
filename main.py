"""
Title:          AI code assistant
Description:    Utilize corporate AI instance to assist with code refactoring and documentation creation.
"""


import os
import sys
import logging
import pathlib
import tiktoken
import requests
import config as c
from typing import Any
from pathlib import Path
from datetime import datetime


def main() -> None:
    """
    Main executable.
    """
    print("""
━━━━━━━━━━┏┓━━━━━━━━┏━━━┓┏━━┓━━━━━━━━━━━━━━━┏┓━━━━━━━━━━━┏┓━
━━━━━━━━━━┃┃━━━━━━━━┃┏━┓┃┗┫┣┛━━━━━━━━━━━━━━┏┛┗┓━━━━━━━━━┏┛┗┓
┏━━┓┏━━┓┏━┛┃┏━━┓━━━━┃┃━┃┃━┃┃━┏━━┓┏┓┏━━┓┏━━┓┗┓┏┛┏━━┓━┏━┓━┗┓┏┛
┃┏━┛┃┏┓┃┃┏┓┃┃┏┓┃━━━━┃┗━┛┃━┃┃━┃━━┫┣┫┃━━┫┃━━┫━┃┃━┗━┓┃━┃┏┓┓━┃┃━
┃┗━┓┃┗┛┃┃┗┛┃┃┃━┫━━━━┃┏━┓┃┏┫┣┓┣━━┃┃┃┣━━┃┣━━┃━┃┗┓┃┗┛┗┓┃┃┃┃━┃┗┓
┗━━┛┗━━┛┗━━┛┗━━┛━━━━┗┛━┗┛┗━━┛┗━━┛┗┛┗━━┛┗━━┛━┗━┛┗━━━┛┗┛┗┛━┗━┛
      AI code refactoring and documentation assistant
        """)
    # create log object, exit script on failure
    log = check_for_log()
    log.info("new script instance running")
    # ask for a script mode
    mode = check_mode(log)
    # perform directory run to collect files
    subjects = collect_files(log)
    # perform API requests
    perform_analysis(log, mode, subjects)


def check_for_log() -> logging.Logger:
    """
    Create a log file in a script location subdirectory.
    Return logger object configured for a local file and a console output.
    Exit script execution in case of an exception.

    :return: log object
    :rtype: logging.getLogger()
    :raise exc: log file / directory creation exception, exiting script as a result
    """
    # log parameters
    log_name = f"{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_api_checker.log"
    try:
        # adjust target logs directory as needed - by default: subdirectory in a script location
        log_directory = Path(__file__).parent / 'logs'
        log_directory.mkdir(exist_ok=True)
        log_path = log_directory / log_name
        # create logger
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.INFO)
        # file handler setting
        if not logger.handlers:
            file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                                        datefmt='%Y-%m-%d %H:%M:%S'))
            logger.addHandler(file_handler)
        # console output handler setting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                                       datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(console_handler)
        return logger
    except Exception as exc:
        print(f"cannot create local log object: {str(exc)}; script will now exit")
        exit()


def check_mode(log: logging.Logger) -> str:
    """
    Ask for user input to choose script mode.

    :param log: log object
    :type log: logging.Logger
    :return: script mode string, optional
    :rtype: str or exit
    """
    log.info('select task to perform')
    log.info('readme - ask for a README.md for a project')
    log.info('analyze - ask for a code analysis of project files')
    log.info('all - perform all requests')
    # get user input
    mode = input(f"Chosen task [readme / analyze / all]: ")
    # verify input - if in range, return proper mode string
    if mode in ['readme', 'analyze', 'all']:
        log.info(f'proceeding with {mode}')
        return mode
    else:
        log.critical(f'Option [{mode}] not recognized, exiting...')
        exit()


def collect_files(log: logging.Logger) -> dict[str, str]:
    """
    Attempt to collect all eligible code files from PROJECT_DIR path in config file according to configured extensions.

    :param log: log object
    :type log: logging.Logger
    :return: dictionary of eligible files, optional
    :rtype: dict[str, str] or exit
    """
    # set up directory
    directory = c.PROJECT_DIR
    if directory:
        log.info(f"directory in config: {directory}")
        directory = Path(directory)
    else:
        log.warning(f"no valid project directory configured, check [PROJECT_DIR] variable value in config")
        exit()

    # loop folders to collect files matching configured extension
    # create a dictionary per script directory
    subjects = {}

    for extension in c.INCLUDED_EXTENSIONS:
        for f in directory.rglob(extension):
            if f.name in c.EXCLUDED_FILES:
                continue
            folder = str(f.parent)
            subjects.setdefault(folder, []).append(f.name)
    # if there are scripts collected - proceed with analysis
    if not subjects:
        log.warning(f"no files matching configured extensions found  script will now exit.")
        exit()
    return subjects


def perform_analysis(log: logging.Logger, mode: str, subjects: dict[str, str]) -> None:
    """
    Execute tasks depending on a chosen mode.

    :param log: log object
    :param str mode: app chosen mode string
    :param subjects: script / project files dictionary
    :type log: logging.Logger
    :type subjects: dict[str, str]
    """
    # distribute tasks depending on mode
    if mode == 'readme':
        tokens = manage_readme_creation(subjects, log)
    elif mode == 'analyze':
        tokens = manage_code_analysis(subjects, log)
    else:
        tokens = manage_readme_creation(subjects, log)
        tokens += manage_code_analysis(subjects, log)
    # summarize tokens usage for whole exchange
    log.info(f'-------------------')
    log.info(f'in total: {tokens} used for all requests')
    log.info(f'all actions finished')


def manage_readme_creation(subjects: dict[str, str], log: logging.Logger) -> int:
    """
    Manage tasks related to readme file creation.

    :param subjects: script / project files dictionary
    :param log: log object
    :type subjects: dict[str, str]
    :type log: logging.Logger
    :return: number of tokens used
    :rtype: int
    """
    parts = []
    # append prompt
    if c.AI_README_PROMPT:
        # add prompt content
        parts.append({"text": c.AI_README_PROMPT})
        # append script code parts
        parts = append_code_parts(parts, subjects, log)
        # set output file save path
        save_path = Path(f"{c.PROJECT_DIR}//README.md")
        # count tokens
        tokens = count_tokens(parts, log)
        # perform a request
        requested = promptify(save_path, parts, log)
        return tokens if requested else 0
    else:
        log.warning('> no prompt configured for README.md creation: check [AI_README_PROMPT] value in config file')
        return 0


def manage_code_analysis(subjects: dict[str, str], log: logging.Logger) -> int:
    """
    Manage tasks related to script analysis md file creation.

    :param subjects: script / project files dictionary
    :param log: log object
    :type subjects: dict[str, str]
    :type log: logging.Logger
    :return: number of tokens used
    :rtype: int
    """
    if c.AI_ANALYSIS_PROMPT:
        tokens = 0
        for directory, scripts in subjects.items():
            for script in scripts:
                script_name = Path(script).stem
                full_path = Path(directory) / script
                code = full_path.read_text(encoding="utf-8")
                if code:
                    parts = [{"text": c.AI_ANALYSIS_PROMPT + " " + code}]
                    # set output file save path
                    # ensure that analysis subdirectory exists
                    file_directory = Path(c.PROJECT_DIR) / 'AI analysis'
                    file_directory.mkdir(exist_ok=True)
                    save_path = Path(f"{file_directory}\\{script_name}.md")
                    # perform a request
                    requested = promptify(save_path, parts, log)
                    if requested:
                        # count tokens
                        tokens += count_tokens(parts, log)
        return tokens
    else:
        log.warning('> no prompt configured for README.md creation: check [AI_ANALYSIS_PROMPT] value in config file')
        return 0


def append_code_parts(parts: list[Any], subjects: dict[str, str], log: logging.Logger) -> list[Any]:
    """
    Attempt to add code as request parts.

    :param parts: request parts list
    :param subjects: script / project files dictionary
    :param log: log object
    :type parts: list[str]
    :type subjects: dict[str, str]
    :type log: logging.Logger
    :return: updated parts list
    :rtype: list[Any]
    """
    log.info(f'> combining code into request parts')
    for directory, scripts in subjects.items():
        for script in scripts:
            full_path = Path(directory) / script
            content = full_path.read_text(encoding="utf-8")
            if content:
                parts.append({"text": f"```python\n{content}\n```"})
    return parts


def count_tokens(parts: list[Any], log: logging.Logger) -> int:
    """
    Attempt to calculate tokens in parts list.

    :param parts: request parts list
    :param log: log object
    :type parts: list[Any]
    :type log: logging.Logger
    :return: token count value
    :rtype: int
    :raise Exception: token calculation exception, returning 0
    """
    try:
        encoding = tiktoken.encoding_for_model(c.GPT_MODEL)
        total_tokens = 0
        for part in parts:
            text = part.get("text", "")
            tokens = len(encoding.encode(text))
            total_tokens += tokens
        log.info(f'> request tokens: {total_tokens}')
        return total_tokens
    except Exception as exc:
        log.warning(f'> cannot count request tokens: {exc}')
        return 0


def promptify(save_path: pathlib.Path, parts: list[Any], log: logging.Logger) -> bool:
    """
    Execute POST request for given payload.

    :param save_path: output file save path
    :param parts: request parts list
    :param log: log object
    :type save_path: pathlib.Path
    :type parts: list[Any]
    :type log: logging.Logger
    :return: request completion bool state
    :rtype: bool
    :raise Exception: unexpected code exception
    """
    try:
        _api_key = os.getenv(c.API_KEY_VAR)
        _api_endpoint = os.getenv(c.API_ENDPOINT_VAR)
        # Prepare the full request body
        body = {"contents": [{"role": "user", "parts": parts}]}
        headers = {"Content-type": "application/json", "api-key": _api_key}
        # execute API POST request
        log.info('requesting Chat AI response')
        response = requests.post(_api_endpoint, headers=headers, json=body)
        # depending on a response status proceed with decoding and export to file
        if response.status_code == 200:
            log.info(f"> response successful")
            payload = response.json()
            md_content = payload["candidates"][0]["content"]["parts"][0]["text"]
            # Save the response to a file
            save_path.write_text(md_content, encoding="utf-8")
            log.info(f"> saved file: {save_path}")
            return True
        else:
            log.warning(f"> response unsuccessful: {response.status_code}, response: {response.text}")
            return False
    # handle exceptions
    except Exception as exc:
        log.warning(f"> unspecified exception encountered: {exc}, manual debug required. Script will now exit.")
        return False


if __name__ == '__main__':
    main()
