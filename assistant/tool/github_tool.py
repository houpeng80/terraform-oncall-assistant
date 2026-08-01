import os

from dotenv import load_dotenv

from langchain_core.tools import tool

from assistant.utils.github_utils import get_latest_version

load_dotenv(encoding="utf-8")

NOT_FOUND_ERROR = "not found from github"
FILE_TYPE_ERROR = "file type error"
RESOURCE_TYPE_ERROR = "resource type error"

headers = {"Authorization": f"token {os.getenv("GITHUB_TOKEN")}"}

@tool
def get_latest_provider_version()->str:
    """
    used to get the latest huaweicloud terraform provider latest version
    triggered only when get the latest huaweicloud terraform provider latest version
    :return:
    """
    version = get_latest_version()
    return version