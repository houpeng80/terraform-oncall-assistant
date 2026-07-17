import asyncio

import httpx
import requests
from requests import Timeout

import vipertls

# @tool
def web_search(url: str):
    """从指定url地址查询所需要的数据。
    当需要根据api地址获取网页信息时触发。

    Args:
        url: 要查询的地址
    """
    client = vipertls.Client(impersonate="chrome_145", timeout=30)
    response = client.get(url)
    response.response
    return response.text
    # return response.content.decode('utf-8')

def web_search2(url: str) -> str:
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("成功")
            return response.text
        elif response.status_code == 404:
            print("资源未找到")
        elif response.status_code == 403:
            print("权限不足")
        elif response.status_code == 500:
            print("服务器错误")
        else:
            print(f"其他状态码: {response.status_code}")
    except Timeout:
        print("请求超时")
    except ConnectionError:
        print("连接失败")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")

    return ""

def web_search3(url: str):
    data = asyncio.run(fetch_data(url))
    print(data)

async def fetch_data(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

if __name__ == "__main__":
    path = "https://registry.terraform.io/providers/huaweicloud/huaweicloud/latest/docs/resources/dcs_all_sessions_kill"
    res = web_search2(path)
    print(res)
