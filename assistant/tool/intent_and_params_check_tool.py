from typing import get_args

from langchain_core.tools import tool

from assistant.sub_agents.intent_recognition.intent_recognize import intent_literal

@tool
def intent_and_params_check(intent: str, missing_params: list[str], reasoning: str)->tuple[bool, str]:
    """
    used to check whether the intent is correct and whether the params are missing
    triggered only when check whether the intent is correct and whether the params are missing
    :return:
    """
    if intent not in get_args(intent_literal):
        return False, f"the intent {intent} is not recognized"

    if intent == "query_resource_by_name":
        if missing_params and len(missing_params) > 0:
            missing_params_str = ",".join(missing_params)
            return False, f"the params {missing_params_str} are missing"

    if intent == "query_resource_by_api":
        if missing_params and len(missing_params) > 0:
            missing_params_str = ",".join(missing_params)
            return False, f"the params {missing_params_str} are missing"

    if intent == "query_resource_by_content":
        if missing_params and len(missing_params) > 0:
            missing_params_str = ",".join(missing_params)
            return False, f"the params {missing_params_str} are missing"

    return True, "success"