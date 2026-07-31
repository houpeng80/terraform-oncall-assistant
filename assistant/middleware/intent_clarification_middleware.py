import json
import logging
from collections.abc import Callable
from hashlib import sha256
from typing import override

from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import ToolMessage
from langgraph.constants import END
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.types import Command, interrupt

from assistant.lead_agent.agent_state import AssistantAgentState

logger = logging.getLogger(__name__)

class IntentClarificationMiddleware(AgentMiddleware[AssistantAgentState]):

    state_schema = AssistantAgentState

    def __init__(self, agent_name: str | None = None):
        super().__init__()
        self._agent_name = agent_name

    def _stable_message_id(self, tool_call_id: str, formatted_message: str) -> str:
        """Build a deterministic message ID so retried clarification calls replace, not append."""
        if tool_call_id:
            return f"param_check:{tool_call_id}"
        digest = sha256(formatted_message.encode("utf-8")).hexdigest()[:16]
        return f"param_check:{digest}"

    def _handle_clarification(self, request: ToolCallRequest, err_msg: str) -> Command:
        args = request.tool_call.get("args", {})
        intent = args.get("intent", "")
        missing_params = args.get("missing_params", [])
        reasoning = args.get("reasoning", "")

        message_parts = [f"❓ 参数缺失： ", f"{", ".join(missing_params)}", f"reasoning: {reasoning}"]

        formatted_message = "\n".join(message_parts)
        # Get the tool call ID
        tool_call_id = request.tool_call.get("id", "")

        # Create a ToolMessage with the formatted question
        # This will be added to the message history
        tool_message = ToolMessage(
            id=self._stable_message_id(tool_call_id, formatted_message),
            content=formatted_message,
            tool_call_id=tool_call_id,
            name="intent_and_params_check",
        )
        print(formatted_message)

        # interrupt({
        #     "reason": "参数缺失",
        #     "course": reasoning,
        #     "message": f"请输入缺少的参数：{",".join(missing_params)}："
        # })

        return Command(
            update={"messages": [tool_message]},
            goto="model",
        )

    @override
    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:
        """Intercept ask_clarification tool calls and interrupt execution (sync version).

        Args:
            request: Tool call request
            handler: Original tool execution handler

        Returns:
            Command that interrupts execution with the formatted clarification message
        """
        if request.tool_call.get("name") != "intent_and_params_check":
            return handler(request)

        response = handler(request)
        tool_res = tuple(json.loads(response.content))
        if not tool_res[0]:
            self._handle_clarification(request, tool_res[1])

        return response

    @override
    async def awrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:
        """Intercept ask_clarification tool calls and interrupt execution (async version).

        Args:
            request: Tool call request
            handler: Original tool execution handler (async)

        Returns:
            Command that interrupts execution with the formatted clarification message
        """
        # Check if this is an ask_clarification tool call
        if request.tool_call.get("name") != "intent_and_params_check":
            # Not a clarification call, execute normally
            return await handler(request)

        response = handler(request)
        tool_res = tuple(json.loads(response.content))
        if not tool_res[0]:
            self._handle_clarification(request, response)

        return response
