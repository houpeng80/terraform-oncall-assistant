import os

from dotenv import load_dotenv

from langchain_core.tools import tool

from assistant.utils.github_utils import get_latest_version, pull_code, checkout_code, \
    search_resource_by_name, search_resource_by_key_word

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

@tool
def checkout_branch(version: str) -> str | None:
    """
    used to check out the branch to the given version
    triggered only when check out the branch to the given version
    :return:
    """
    if not version:
        return f" version is required"
    checkout_code(version)
    return None

@tool
def search_resource_from_code(resource_type: str,resource_name: str, service_name: str) -> bool | str:
    """
    used to search the resource name by resource_name and service_name
    triggered only when search the resource name by resource_name and service_name
    :return:
    """
    if not resource_type or not resource_name or not service_name:
        return f"resource_name, service_name are all required"

    return search_resource_by_name(resource_type, service_name, resource_name)

@tool
def search_resource_by_api(api_method: str, api_url: str, service_name: str) -> str | list[str]:
    """
    used to search the resource name by api_method, api_url and service_name
    triggered only when search the resource name by api method, api_url and service_name
    :return:
    """
    if not api_method or not api_url or not service_name:
        return f"api_method, api_url and service_name are all required"

    return search_resource_by_key_word(f"{api_method} {api_url}", f"huaweicloud/services/{service_name}")

if "__main__" == __name__:
    search_resource_from_code("data_source", "huaweicloud_taurusdb_audit_logs_download_links", "taurusdb")
