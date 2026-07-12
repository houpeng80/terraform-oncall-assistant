import logging
from typing import override, Any

from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from langchain.agents.middleware.types import StateT
from langgraph.runtime import Runtime
from langgraph.typing import ContextT

logger = logging.getLogger(__name__)

class AuthMiddleware(AgentMiddleware):

    def __init__(self, agent_name: str):
        super().__init__()
        self._agent_name = agent_name

    @override
    def before_agent(self, state: AgentState, runtime: Runtime) -> dict | None:
        """ validate user info, get user_id and then set to config"""
        return None

    def abefore_agent(self, state: StateT, runtime: Runtime[ContextT]) -> dict[str, Any] | None:
        """ validate user info, get user_id and then set to config"""
        return None
