import logging
from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, TodoListMiddleware
from langchain_core.messages import HumanMessage, AIMessageChunk, ToolMessage
from langchain_core.tools import BaseTool
from langgraph.checkpoint.memory import InMemorySaver

from assistant.config.config import get_app_config
from assistant.middleware.clarification_middleware import ClarificationMiddleware
from assistant.middleware.cycle_check_middleware import CycleCheckMiddleware
from assistant.middleware.dynamic_system_porompt_middleware import build_system_prompt_template
from assistant.middleware.log_middleware import LoggingMiddleware
from assistant.middleware.memory_middleware import MemoryMiddleware
from assistant.middleware.summarization_middleware import ContextSummarizationMiddleware
from assistant.middleware.token_usage_middleware import TokenUsageMiddleware
from assistant.model.factory import get_model
from assistant.react.agent_state import AssistantAgentState
from assistant.tool import oncall_schedule, reference_docs, rag_search_tool
from assistant.tool.clarification_tool import ask_clarification_tool
from assistant.tool.file_tool import read_md
from assistant.tool.github_tool import get_latest_provider_version, checkout_branch, search_resource_from_code, \
    search_resource_by_api
from assistant.utils.github_utils import clone_code, test_code_exists, pull_code
from assistant.utils.schedule_utils import start_scheduler_sync_git_code, stop_scheduler_sync_git_code

logger = logging.getLogger(__name__)

AGENT_NAME = "terraform_oncall_assistant"

def init_local_code():
    exists = test_code_exists()
    if not exists:
        logger.info("begin to clone code from github")
        clone_code()
    else:
        logger.info("begin to pull latest code from github")
        # pull_code()

class LeaderAgent:
    def __init__(self, config: dict[str, Any]):
        agent_config = get_app_config()
        model = get_model(agent_config.model_type)
        self.model = model
        self.agent_config = agent_config
        self.config = config
        self.check_pointer = InMemorySaver()
        self.agent = self.create_assistant_agent()
        # init_local_code()
        # start_scheduler_sync_git_code()

    def __del__(self):
        stop_scheduler_sync_git_code()

    def deal_question(self):
        while True:
            user_input = input("\nUser: ")
            if user_input.lower() in ["q", "quit"]:
                break

            self.react(user_input)

    def react(self, question: str):
        input_message = {
            "messages": [HumanMessage(content=question)],
            "input_token_statistics": 0,
            "output_token_statistics": 0,
            "total_token_statistics": 0,
            "model_cycle_time": 1,
        }

        try:
            stream = self.agent.stream(
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
                            # 打印中断消息
                            if node_name == "__interrupt__":
                                print(update[0].value)
                            # 模型请求调用工具
                            if node_name == "model" and update["messages"][-1].tool_calls:
                                logger.info("[ready to call tool]: name=%s, args=%s", update['messages'][-1].tool_calls[0]['name'], update['messages'][-1].tool_calls[0]['args'])
                            # 工具执行结果
                            elif node_name == "tools" and update['messages'][-1].content:
                                logger.info("[tool return]: result=%s", update['messages'][-1].content)
                    elif chunk["type"] == "messages" and chunk["data"] is not None and len(chunk["data"]) > 0:
                        if isinstance(chunk["data"][0], AIMessageChunk) and chunk["data"][0].content is not None:
                            print(chunk["data"][0].content, end="", flush=True)
                        if isinstance(chunk["data"][0], ToolMessage) and chunk["data"][0].name == "ask_clarification" and chunk["data"][0].content is not None:
                            print(chunk["data"][0].content, end="", flush=True)

        except Exception as e:
            print(f"\n--- ❌ fail to deal question: {e}---")

        state = self.agent.get_state(self.config).values
        return state

    def create_assistant_agent(self):
        agent = create_agent(
            name=AGENT_NAME,
            model=self.model,
            checkpointer=self.check_pointer,
            # system_prompt=self.build_system_prompt_template(),
            middleware=self.build_middlewares(),
            tools=self.build_tools(),
            state_schema=AssistantAgentState
        )
        return agent

    # def build_system_prompt_template(self) -> str:
    #     return apply_prompt_template(user_id=self.config["configurable"]["user_id"], agent_name=AGENT_NAME,)

    def build_middlewares(self) -> list[AgentMiddleware]:
        middlewares: list[AgentMiddleware] = [
            LoggingMiddleware(agent_name=AGENT_NAME),
            TokenUsageMiddleware(agent_name=AGENT_NAME),
            CycleCheckMiddleware(agent_name=AGENT_NAME),
            MemoryMiddleware(agent_name=AGENT_NAME),
            ContextSummarizationMiddleware(
                model=self.model,
                agent_name=AGENT_NAME,
                trigger=[
                    ("messages", self.agent_config.summarization_trigger_messages),
                    ("tokens", self.agent_config.summarization_trigger_tokens)
                ],
                keep=("tokens", self.agent_config.summarization_trigger_tokens/3)
            ),
            ClarificationMiddleware(agent_name=AGENT_NAME),
            TodoListMiddleware(),
            build_system_prompt_template,
        ]
        return middlewares

    def build_tools(self) -> list[BaseTool] | None:
        tools = [
            oncall_schedule,
            reference_docs,
            ask_clarification_tool,
            get_latest_provider_version,
            # pull_latest_provider_code,
            checkout_branch,
            search_resource_from_code,
            search_resource_by_api,
            rag_search_tool,
            read_md,
        ]
        return tools
