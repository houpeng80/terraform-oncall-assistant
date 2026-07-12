from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import HumanMessage, AIMessageChunk
from langchain_core.tools import BaseTool
from langgraph.checkpoint.memory import InMemorySaver

from assistant.config.config import get_app_config
from assistant.middleware.clarification_middleware import ClarificationMiddleware
from assistant.middleware.log_middleware import LoggingMiddleware
from assistant.middleware.memory_middleware import MemoryMiddleware
from assistant.middleware.summarization_middleware import ContextSummarizationMiddleware
from assistant.middleware.token_usage_middleware import TokenUsageMiddleware
from assistant.model.factory import get_model
from assistant.react.agent_state import AssistantAgentState
from assistant.react.prompt import apply_prompt_template

AGENT_NAME = "terraform_oncall_assistant"

class LeaderAgent:
    def __init__(self, config: dict[str, Any]):
        agent_config = get_app_config()
        model = get_model(agent_config.model_type)
        self.model = model
        self.agent_config = agent_config
        self.config = config
        self.check_pointer = InMemorySaver()

    def react(self, question: str):
        input_message = {
            "messages": [HumanMessage(content=question)],
            "input_token_statistics": 0,
            "output_token_statistics": 0,
            "total_token_statistics": 0,
        }
        agent = self.create_assistant_agent()

        try:
            stream = agent.stream(
                input=input_message,
                config=self.config,
                stream_mode=["messages", "updates"],
                version="v2",
            )
            for chunk in stream:
                # print(chunk)
                if self.agent_config.print_thinking_process:
                    if chunk["type"] == "updates":
                        for node_name, update in chunk["data"].items():
                            # 模型请求调用工具
                            if node_name == "model" and update["messages"][-1].tool_calls:
                                print(
                                    f"\n[ready to call tool]: name={update['messages'][-1].tool_calls[0]['name']}, args={update['messages'][-1].tool_calls[0]['args']}")
                            # 工具执行结果
                            elif node_name == "tools" and update['messages'][-1].content:
                                print(f"\n[tool return]: result={update['messages'][-1].content}")
                    elif chunk["type"] == "messages" and chunk["data"] is not None and len(chunk["data"]) > 0:
                        if isinstance(chunk["data"][0], AIMessageChunk) and chunk["data"][0].content is not None:
                            print(chunk["data"][0].content, end="", flush=True)

        except Exception as e:
            print(f"\n--- ❌ fail to deal question: {e}---")

        state = agent.get_state(self.config).values
        return state

    def create_assistant_agent(self):
        agent = create_agent(
            name=AGENT_NAME,
            model=self.model,
            checkpointer=self.check_pointer,
            system_prompt=self.build_system_prompt_template(),
            middleware=self.build_middlewares(),
            tools=self.build_tools(),
            state_schema=AssistantAgentState
        )
        return agent

    def build_system_prompt_template(self) -> str:
        return apply_prompt_template(user_id=self.config["configurable"]["user_id"], agent_name=AGENT_NAME,)

    def build_middlewares(self) -> list[AgentMiddleware]:
        middlewares: list[AgentMiddleware] = [
            LoggingMiddleware(agent_name=AGENT_NAME),
            TokenUsageMiddleware(agent_name=AGENT_NAME),
            MemoryMiddleware(agent_name=AGENT_NAME),
            ContextSummarizationMiddleware(
                model=self.model,
                agent_name=AGENT_NAME,
                trigger=[
                    ("messages", self.agent_config.summarization_trigger_messages),
                    ("tokens", self.agent_config.summarization_trigger_tokens)
                ]
            ),
            ClarificationMiddleware(agent_name=AGENT_NAME)
        ]
        return middlewares

    def build_tools(self) -> list[BaseTool] | None:
        return None
