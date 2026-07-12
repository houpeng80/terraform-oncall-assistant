import requests
from bs4 import BeautifulSoup


def search_github(keyword):
    # GitHub API的搜索URL，q参数用于搜索
    url = f"https://api.github.com/search/repositories?q={keyword}"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    # GitHub API速率限制，可能需要认证（例如使用token）来避免限制
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 如果响应状态码不是200，抛出异常

    data = response.json()
    if data["total_count"] > 0:
        print(f"找到 {data['total_count']} 个仓库，包含关键字 '{keyword}'")
        for repo in data["items"]:
            print(f"仓库名: {repo['name']}, URL: {repo['html_url']}")
    else:
        print(f"没有找到包含关键字 '{keyword}' 的仓库")


# 使用函数搜索特定的关键字
# print(search_github("huaweicloud"))


def search_keyword_in_github(repo_url, keyword):
    # 请求GitHub仓库的HTML内容
    response = requests.get(repo_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有文本内容，这里可以根据需要调整选择器
        texts = soup.find_all(string=True)
        for text in texts:
            if keyword.lower() in text.lower():
                print(text.title())
                # print(f"Found keyword '{keyword}' in text: {text.title()}")
                return True
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    return False


# 使用示例
repo_url = 'https://github.com/huaweicloud/terraform-provider-huaweicloud/blob/master/docs/api/'  # 替换为实际的仓库URL
keyword = '/v2/{project_id}/instances/{instance_id}/backups'  # 你要搜索的关键字
search_keyword_in_github(repo_url, keyword)
