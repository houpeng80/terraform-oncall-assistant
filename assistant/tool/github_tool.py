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

# def get_github_content(file_path: str) -> str | list | None:
#     repo_url = "https://api.github.com/repos/{username}/{repo_name}/contents/{file_path}"
#     repo_url = repo_url.replace('{username}', 'huaweicloud')
#     repo_url = repo_url.replace('{repo_name}', 'terraform-provider-huaweicloud')
#     repo_url = repo_url.replace('{file_path}', file_path)
#     response = requests.get(repo_url, headers=headers)
#     if response.status_code == 200:
#         repo_res = response.json()
#         # 说明是具体的文件，返回的是文件内容
#         if isinstance(repo_res, dict):
#             repo_content = repo_res["content"]
#             decoded_text = base64.b64decode(repo_content).decode('utf-8')
#             return decoded_text
#         # 说明是文件夹，返回的是文件列表
#         elif isinstance(repo_res, list):
#             return repo_res
#         return "file type error"
#     elif response.status_code == 404:
#         return NOT_FOUND_ERROR
#     else:
#         raise Exception(f"Failed to fetch data. Status code: {response.status_code}")
#
# def get_json_file(resource_type: str, file_name:str) -> str:
#     file_path = "docs/json/{resource_type}/{file_name}.json"
#     if resource_type == "data_source":
#         file_path = file_path.replace("{resource_type}", "data-sources")
#         file_path = file_path.replace("{file_name}", file_name)
#     elif resource_type == "resource":
#         file_path = file_path.replace("{resource_type}", "resources")
#         file_path = file_path.replace("{file_name}", file_name)
#     else:
#         return RESOURCE_TYPE_ERROR
#
#     # 从docs/json 中查找文件是否存在，如果存在，说明发布的版本已经支持，如果不存在，说明发布的版本还未支持
#     file_content = get_github_content(file_path)
#     if file_content == NOT_FOUND_ERROR:
#         return NOT_FOUND_ERROR
#
#     return get_github_content(file_path)
#
# def get_docs_file(resource_type: str, file_name:str) -> str:
#     file_path = "docs/{resource_type}/{file_name}.md"
#     if resource_type == "data_source":
#         file_path = file_path.replace("{resource_type}", "data-sources")
#         file_path = file_path.replace("{file_name}", file_name)
#     elif resource_type == "resource":
#         file_path = file_path.replace("{resource_type}", "resources")
#         file_path = file_path.replace("{file_name}", file_name)
#     else:
#         return RESOURCE_TYPE_ERROR
#
#     # 从 docs/data-sources、docs/resources 中查找文件内容
#     file_content = get_github_content(file_path)
#     if file_content == NOT_FOUND_ERROR:
#         return ""
#
#     return file_content
#
# @tool
# def get_latest_released_file_content(resource_type: str, resource_name:str) -> str:
#     """
#     used to get the resource info from latest released version
#     triggered when the resource info from latest released version
#
#     :param resource_type:
#     :param resource_name:
#     :return:
#     """
#     if not resource_name.startswith('huaweicloud_'):
#         return "file name error, should start with `huaweicloud_`"
#
#     file_name = resource_name.replace('huaweicloud_', '')
#
#     # 从docs/json 中查找文件是否存在，如果存在，说明发布的版本已经支持，如果不存在，说明发布的版本还未支持
#     file_content = get_json_file(resource_type, file_name)
#     if file_content == NOT_FOUND_ERROR:
#         return NOT_FOUND_ERROR
#
#     # 从 docs/data-sources、docs/resources 中查找文件内容
#     file_content = get_docs_file(resource_type, file_name)
#     return file_content
#
# @tool
# def get_committed_but_not_released_file_content(resource_type: str, resource_name:str) -> str:
#     """
#     used to get the resource info from the repo that has been committed but not yet released,
#     triggered when get the resource info from the repo that has been committed but not yet released
#
#     :param resource_type: the type of resource
#     :param resource_name: the name of the resource
#     :return: the docs of the resource which is committed but not yet released
#     """
#     if not resource_name.startswith('huaweicloud_'):
#         return "file name error, should start with `huaweicloud_`"
#
#     file_name = resource_name.replace('huaweicloud_', '')
#
#     # 从 docs/data-sources、docs/resources 中查找文件内容
#     file_content = get_docs_file(resource_type, file_name)
#     return file_content

# @tool
# def get_latest_provider_version()->str:
#     """
#     used to get huaweicloud terraform provider latest version
#     triggered only when get huaweicloud terraform provider latest version
#     :return:
#     """
#     repo_url = "https://api.github.com/repos/{username}/{repo_name}/releases/latest"
#     repo_url = repo_url.replace('{username}', 'huaweicloud')
#     repo_url = repo_url.replace('{repo_name}', 'terraform-provider-huaweicloud')
#     response = requests.get(repo_url, headers=headers)
#     if response.status_code == 200:
#         repo_res = response.json()
#         latest_tag = repo_res["tag_name"]
#         return latest_tag
#     elif response.status_code == 404:
#         return NOT_FOUND_ERROR
#     else:
#         raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

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
def pull_latest_provider_code():
    """
    used to pull the latest huaweicloud terraform code from github
    triggered only when pull the latest huaweicloud terraform code from github
    :return:
    """
    pull_code()

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
