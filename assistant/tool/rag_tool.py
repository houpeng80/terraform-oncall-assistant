from langchain_core.tools import tool

from assistant.rag.rag_manager import rag_keyword_search

@tool
def rag_search_tool(resource_type: str, content: str) -> list[str]:
    """ this tool is used to get the related resource/data_source info by resource_type and account,
    triggered only when get the related resource/data_source info by resource_type and account"""

    query = ""
    if resource_type == "resource":
        query = f"Manager {content}"
    if resource_type == "data_source":
        query = f"Use this data source to get {content}"

    return rag_keyword_search(query)