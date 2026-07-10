import json
import uuid

from assistant.memory.queue import get_memory_queue
from assistant.memory.storage import get_memory_storage
from assistant.memory.updater import update_memory_from_conversation, _create_empty_memory, _save_memory_to_file, \
    get_memory_data, delete_memory_data, clear_memory_data, _validate_confidence, create_memory_fact, \
    delete_memory_fact, update_memory_fact

memory_data = {
    "user": {},
    "history": {},
    "facts": [
        {"content": "User uses PostgreSQL", "category": "knowledge", "confidence": 0.9},
        {"content": "User prefers SQLAlchemy", "category": "preference", "confidence": 0.8},
    ],
}

facts=[
    {
        "id": "fact_export",
        "content": "User prefers concise responses.",
        "category": "preference",
        "confidence": 0.9,
        "createdAt": "2026-03-20T00:00:00Z",
        "source": "thread-1",
    },
    {
        "id": "fact_correction",
        "content": "Use make dev for local development.",
        "category": "correction",
        "confidence": 0.95,
        "createdAt": "2026-03-20T00:00:00Z",
        "source": "thread-1",
        "sourceError": "The agent previously suggested npm start.",
    }
]

test_data = {
    "version": "1.0",
    "lastUpdated": "2026-03-26T12:00:00Z",
    "user": {
        "workContext": {"summary": "", "updatedAt": ""},
        "personalContext": {"summary": "", "updatedAt": ""},
        "topOfMind": {"summary": "", "updatedAt": ""},
    },
    "history": {
        "recentMonths": {"summary": "", "updatedAt": ""},
        "earlierContext": {"summary": "", "updatedAt": ""},
        "longTermBackground": {"summary": "", "updatedAt": ""},
    },
    "facts": facts or [],
}

# get_memory_storage().save(test_data, "test_user_id")
# print(get_memory_storage().load("test_user_id"))
# get_memory_storage().delete("test_user_id")

# empty_memory = _create_empty_memory()
# print(empty_memory)
# _save_memory_to_file(get_memory_data("user_1"), "test_user_id_2")
# print(get_memory_data("test_user_id_2"))
# delete_memory_data("test_user_id_2")
# clear_memory_data("test_user_id_2")
# print(_validate_confidence(8))

# print(create_memory_fact(
#     content = "nice content",
#     category = "project",
#     confidence = 0.9,
#     user_id = "test_user_id",
# ))

# delete_memory_fact("fact_106e1da3", "test_user_id")

# print(update_memory_fact(
#     fact_id = "fact_bfc4b0f3",
#     content = "nice content update",
#     category = "project",
#     confidence = 0.3,
#     user_id = "test_user_id",
# ))

print(json.dumps(test_data, indent=2))



# memory_queue = get_memory_queue()
#
# memory_queue.add(
#     thread_id="test_thread_id",
#     messages=["conversation"],
#     agent_name="terraform_oncall_assistant_agent",
#     user_id="test_user_id",
#     correction_detected=True,
#     reinforcement_detected=True,
# )

# update_memory_from_conversation(
#     thread_id="test_thread_id",
#     messages=["conversation"],
#     user_id="test_user_id",
#     correction_detected=True,
#     reinforcement_detected=True,
# )

