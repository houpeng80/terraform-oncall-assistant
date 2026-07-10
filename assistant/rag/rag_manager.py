import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from mem0 import Memory

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from mem0.configs.base import MemoryConfig

load_dotenv(encoding="utf-8")

# embedding_mode = OpenAIEmbeddings(
#     model=os.getenv("QWEN_MODEL"),
#     base_url=os.getenv("QWEN_BASE_URL"),
#     api_key=os.getenv("QWEN_API_KEY"),
#     dimensions=1024
# )

llm = ChatOpenAI(
    model=os.getenv("DEEPSEEK_MODEL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

config = {
    # "llm": {
    #     "provider": "openai",
    #     "config": {
    #         "model": os.getenv("DEEPSEEK_MODEL"),  # 或 deepseek-reasoner
    #         "api_key": os.getenv("DEEPSEEK_API_KEY"),
    #         "temperature": 0.2,
    #         "max_tokens": 2000,
    #         "openai_base_url": os.getenv("DEEPSEEK_BASE_URL")
    #     }
    # },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": os.getenv("QWEN_MODEL"),
            "api_key": os.getenv("QWEN_API_KEY"),
            "openai_base_url": os.getenv("QWEN_BASE_URL"),
            "embedding_dims": 1024,
        }
    },
    "vector_store": {
        "provider": "chroma",
        "config": {
            "path": "./my_chroma_memories",  # 本地持久化路径
            "collection_name": "user_memories"
        }
    }
}

#
# embedder = OpenAIEmbeddings(
#     model=os.getenv("QWEN_MODEL"),
#     api_key=os.getenv("QWEN_API_KEY"),
#     base_url=os.getenv("QWEN_BASE_URL"),
#     dimensions=1024,
# )

# 方式1：直接传入已经实例化的对象
# config = {
#     "vector_store": {
#         "provider": "chroma",
#         "config": {
#             "path": "./my_chroma_memories",  # 本地持久化路径
#             "collection_name": "user_memories"
#         }
#     }
# }

# 初始化 Memory
# cfg = MemoryConfig()
memory = Memory.from_config(config)

# 用户 ID（用于隔离不同用户的记忆）
user_id = "user_local_001"

# === 添加记忆 ===
print("正在添加记忆...")
# memory.add("我住在杭州，喜欢西湖边散步。", user_id=user_id)
# memory.add("我对人工智能和大模型开发很感兴趣。", user_id=user_id)
# memory.add("我不喝咖啡，只喝茶。", user_id=user_id)

# === 查询相关记忆 ===
query = "用户住哪？"
print(f"\n查询问题: {query}")
# results = memory.search(query, user_id=user_id)
results = memory.search(query, filters={'user_id': user_id})

print("检索到的相关记忆:")
for i, mem in enumerate(results['results'], 1):
    print(f"{i}. {mem['memory']}")
    # print(f"{i}. {mem['text']}")

# === （可选）让 LLM 基于记忆生成回答 ===
# 注意：Mem0 本身不直接提供“带记忆的问答”接口，但你可以组合使用
context = "\n".join([mem["memory"] for mem in results['results']])
prompt = f"""你是一个贴心的助手，请根据用户的记忆回答问题。
用户的记忆：
{context}


请直接回答，不要提及“根据记忆”等字样。"""

response = llm.invoke([SystemMessage(content=prompt), HumanMessage(content=query)])
# response = memory.llm.generate_response(messages=[{"role": "system", "content": prompt},{"role": "user", "content": query}])
print(f"\nLLM 回答: {response}")
