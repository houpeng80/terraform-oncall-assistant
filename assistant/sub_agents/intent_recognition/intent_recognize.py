from typing import Literal, Any
from pydantic import BaseModel, Field

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from assistant.config.config import get_app_config
from assistant.model import get_model
from assistant.sub_agents.intent_recognition.prompt import SYSTEM_PROMPT

AGENT_NAME = "intent_recognize_agent"

intent_literal = Literal[
    "query_oncall",
    "query_latest_version",
    "query_reference_docs",
    "whether_support_special_region",
    "query_resource_by_name",
    "query_resource_by_api",
    "query_resource_by_content",
    "unknow"
]

params_literal = Literal[
    "service_type",
    "resource_type",
    "resource_name",
    "api_method",
    "api_url",
    "content"
]

class IntentResult(BaseModel):
    """意图识别结果的结构化输出模型"""
    intent: intent_literal = Field(description="用户输入所对应的业务意图")
    confidence: float = Field(
        description="模型对意图判断的置信度分数，取值范围 0 到 1",
        ge=0,
        le=1
    )
    params: dict[params_literal, str] = Field(description="用户要执行业务的参数",)
    missing_params: list[str] = Field(description="用户要执行业务缺失的参数")
    reasoning: str = Field(description="简短说明做出该意图判断的理由")

class IntentRecognize:
    def __init__(self, config: dict[str, Any]):
        self.model = get_model(get_app_config().model_type)
        self.agent_config = get_app_config()
        self.check_pointer = InMemorySaver()
        self.config = config
        self.agent = self.create_intent_recognize_agent()

    def intent_recognize(self, query:str) -> IntentResult:
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config=self.config,
        )
        # 直接从结果中提取意图识别对象
        intent_info = result["structured_response"]
        return intent_info

    def create_intent_recognize_agent(self):
        agent = create_agent(
            model=self.model,
            checkpointer=InMemorySaver(),
            system_prompt=SYSTEM_PROMPT,
            response_format=IntentResult,
        )
        return agent

if __name__ == "__main__":
    agent_config = get_app_config()
    model = get_model(agent_config.model_type)
    config = {"configurable": {"thread_id": "user-001"}}

    query1 = "帮我查一下 RDS 服务的 huaweicloud_rds_notify_replace_node 这个资源支持吗"
    query2 = "帮我查一下 RDS 服务的 POST /v3/{project_id}/instances/{instance_id}/db-jobs/{job_id}/switch 这个API支持吗"
    query3 = "帮我查一下 DCS 服务支持创建实例吗"
    query4 = "provider支持北京四这个region吗"
    query5 = "有没有provider的参考文档"
    query6 = "当前oncall是谁"
    query7 = "rds 实例这个支持name这个字段吗"
    query8 = "当前天气怎么样"
    query9 = "我好看吗"
    query10 = "帮我查一下 RDS 服务的 /v3/{project_id}/instances/{instance_id}/db-jobs/{job_id}/switch 这个API支持吗"
    query11 = "可以查询当前所有的规格吗"

    intent_confidence = IntentRecognize(config=config)
    # querys = [query11]
    # for query in querys:
    #     res = intent_confidence.intent_recognize(model=model, query=query)
    #     print("=====================")
    #     print(f"识别意图: {res.intent}")
    #     print(f"置信度: {res.confidence}")
    #     print(f"参数: {res.params}")
    #     print(f"推理理由: {res.reasoning}")

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["q", "quit"]:
            break

        res = intent_confidence.intent_recognize(query=user_input)
        print("=====================")
        print(f"识别意图: {res.intent}")
        print(f"置信度: {res.confidence}")
        print(f"参数: {res.params}")
        print(f"缺失的参数: {res.missing_params}")
        print(f"推理理由: {res.reasoning}")
