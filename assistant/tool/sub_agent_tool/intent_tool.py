from langchain_core.tools import tool

from assistant.sub_agents.intent_recognition.intent_recognize import IntentRecognize

@tool
def intent_recognize(user_input: str) -> tuple[str, dict[str, str],list[str],str]:
    """this tool is used to recognize the user intent, triggered only when recognize the user intent
    :param user_input: the user input
    :return: intent, parameters, missing_params, reasoning
    """

    intent_confidence = IntentRecognize(config={"thread_id": "intent_confidence"})
    res = intent_confidence.intent_recognize(query=user_input)
    return res.intent, res.params, res.missing_params, res.reasoning