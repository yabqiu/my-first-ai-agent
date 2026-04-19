import os.path

from langchain.tools import tool
import requests

@tool
def read_file(filepath: str) -> str:
    """read file content by filepath"""

    if not os.path.exists(filepath):
        return f"Error: file {filepath} not exist"
    with open(filepath, "r") as f:
        return f.read()

@tool
def write_file(filepath: str, content: str) -> None:
    """write content to file by filepath"""

    with open(filepath, "w") as f:
        f.write(content)

    return f"wrote file {filepath}"

@tool
def web_fetch(url: str) -> str:
    """fetch web HTML content by url"""

    return requests.get(url).text