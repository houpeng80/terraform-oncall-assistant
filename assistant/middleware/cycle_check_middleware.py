import logging
from typing import override, Any

from langgraph.runtime import Runtime
from langchain.agents.middleware import AgentMiddleware
from langgraph.typing import ContextT
from langchain.agents.middleware.types import hook_config

from assistant.config.config import get_app_config
from assistant.react.agent_state import AssistantAgentState

logger = logging.getLogger(__name__)

class CycleCheckMiddleware(AgentMiddleware[AssistantAgentState]):

    def __init__(self, agent_name: str | None = None):
        super().__init__()
        self._agent_name = agent_name

    @hook_config(can_jump_to=["end"])
    @override
    def before_model(self, state: AssistantAgentState, runtime: Runtime[ContextT]) -> dict[str, Any] | None:
        logger.info("invoke the model for the %s time", state["model_cycle_time"])
        if state["model_cycle_time"] > get_app_config().model_cycle_max:
            return {
                "jump_to": "end"
            }
        return None

    @hook_config(can_jump_to=["end"])
    @override
    def abefore_model(self, state: AssistantAgentState, runtime: Runtime[ContextT]) -> dict[str, Any] | None:
        logger.info("invoke the model for the %s time", state["model_cycle_time"])
        if state["model_cycle_time"] > get_app_config().model_cycle_max:
            return {
                "jump_to": "end"
            }

        return None

    @override
    def after_model(self, state: AssistantAgentState, runtime: Runtime) -> dict[str, Any] | None:
        return {
            "model_cycle_time" : state["model_cycle_time"] + 1
        }

    @override
    def aafter_model(self, state: AssistantAgentState, runtime: Runtime) -> dict[str, Any] | None:
        return {
            "model_cycle_time": state["model_cycle_time"] + 1
        }

