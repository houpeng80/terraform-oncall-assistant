import logging

from typing import override, Callable

from langchain.agents.middleware import AgentMiddleware
from langchain.agents.middleware.types import ModelRequest, ModelResponse, ModelCallResult
from langgraph.prebuilt.tool_node import ToolCallRequest

from assistant.lead_agent.agent_state import OncallAgentState
from assistant.tool.tool_registry import get_tools_by_intent

logger = logging.getLogger(__name__)

class DynamicToolMiddleware(AgentMiddleware[OncallAgentState]):

    state_schema = OncallAgentState

    def __init__(self, agent_name: str | None = None):
        super().__init__()
        self._agent_name = agent_name

    @override
    def wrap_model_call(
            self,
            request: ModelRequest,
            handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelCallResult:
        intent = request.state["intent"]
        tools = get_tools_by_intent(intent)
        updated_request = request.override(tools=[*request.tools, tools[0]])
        return handler(updated_request)

    @override
    def awrap_model_call(
            self,
            request: ModelRequest,
            handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelCallResult:
        intent = request.state["intent"]
        tools = get_tools_by_intent(intent)
        updated_request = request.override(tools=[*request.tools, *tools])
        return handler(updated_request)

    @override
    def wrap_tool_call(self, request: ToolCallRequest, handler):
        intent = request.state["intent"]
        tools = get_tools_by_intent(intent)
        tool_map = {tool.name: tool for tool in tools}
        tool_call_name = request.tool_call["name"]
        if tool_call_name in tool_map:
            return handler(request.override(tool=tool_map[tool_call_name]))

        return handler(request)

    @override
    def awrap_tool_call(self, request: ToolCallRequest, handler):
        intent = request.state["intent"]
        tools = get_tools_by_intent(intent)
        tool_map = {tool.name: tool for tool in tools}
        tool_call_name = request.tool_call["name"]
        if tool_call_name in tool_map:
            return handler(request.override(tool=tool_map[tool_call_name]))

        return handler(request)

