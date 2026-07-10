from langchain_core.tools import tool

@tool("ask_clarification")
def oncall_schedule()->str:
    return "https://onebox.huawei.comv/v/29f3e6bf2c40905380d59c25b09387?type=0"