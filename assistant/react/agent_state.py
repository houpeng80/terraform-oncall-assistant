from langchain.agents import AgentState

class AssistantAgentState(AgentState):
    # 基础信息
    request_message: str  # 用户原始请求

    model_cycle_time: int

    input_token_statistics: int
    output_token_statistics: int
    total_token_statistics: int