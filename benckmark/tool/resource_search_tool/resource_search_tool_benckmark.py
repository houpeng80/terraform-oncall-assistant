import re

# 工具池
tools = {
    "calculator": {
        "desc": "用于数学计算，输入数学表达式字符串",
        "func": lambda expr: eval(expr)
    },
    "search": {
        "desc": "联网搜索实时信息，无法靠内部知识回答时使用",
        "func": lambda query: f"【模拟搜索结果】关于「{query}」的最新信息：xxx实时数据"
    }
}

def llm_decide(query: str):
    """模拟大模型决策：判断调用哪个工具、传入参数"""
    # 匹配数学算式
    math_pattern = r"[\d\+\-\*\/\(\)\.]+"
    math_match = re.search(math_pattern, query)

    # 场景1：计算题 → 调用计算器
    if any(word in query for word in ["等于", "计算", "算一下", "+", "-", "*", "/"]) and math_match:
        expr = math_match.group()
        return {"tool": "calculator", "params": expr}

    # 场景2：需要实时资讯/外部信息 → 调用搜索
    if any(word in query for word in ["最新", "今天", "实时", "2026", "天气", "新闻"]):
        return {"tool": "search", "params": query}

    # 场景3：无需工具，直接回答
    return {"tool": None, "params": None}


def agent_run(user_query: str):
    print(f"用户问题：{user_query}\n")
    decision = llm_decide(user_query)

    # 无需工具
    if decision["tool"] is None:
        return f"直接回答：{user_query} 无需调用工具"

    # 执行工具
    tool_name = decision["tool"]
    tool_param = decision["params"]
    print(f"Agent 决定调用工具：{tool_name}，参数：{tool_param}")
    tool_result = tools[tool_name]["func"](tool_param)
    print(f"工具返回结果：{tool_result}\n")

    # LLM整合结果输出
    final_ans = f"结合工具结果回答：{tool_result}"
    return final_ans


# ========== 测试演示 ==========
if __name__ == "__main__":
    # 测试1：数学计算，触发计算器工具
    print(agent_run("计算 123 * 45 + 78 / 2"))
    print("-" * 60)

    # 测试2：实时信息，触发搜索工具
    print(agent_run("今天北京天气怎么样"))
    print("-" * 60)

    # 测试3：普通闲聊，不调用工具
    print(agent_run("什么是智能体"))