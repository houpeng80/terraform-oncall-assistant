from langchain.agents.middleware import TodoListMiddleware

SYSTEM_PROMPT = """
在开始任务前，必须先使用 write_todos 制定计划：
1. 将任务分解为多个可独立执行的子步骤
2. 按优先级排序
3. 每完成一步需更新状态
"""

class TodoMiddleware(TodoListMiddleware):

    def __init__(self):
        super(self.__class__, self).__init__(system_prompt=SYSTEM_PROMPT,tool_description="使用此工具创建、更新或删除你的任务清单")