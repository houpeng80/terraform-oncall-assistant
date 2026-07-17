from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os

from assistant.rag.es_manager import es_keyword_search

# 阿里云向量配置
os.environ["OPENAI_API_KEY"] = "sk-xxx"
os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
embeddings = OpenAIEmbeddings(model="text-embedding-v3")
chroma_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

def multi_retrieval(query: str, top_k=4):
    # 1. ES关键词召回
    es_res = es_keyword_search(query, top_k)
    # 2. Chroma语义向量召回
    vec_res = chroma_db.similarity_search_with_score(query, k=top_k)

    # 统一转换成 chunk_id 维度数据
    combine = {}
    # ES结果存入字典
    for item in es_res:
        cid = item["chunk_id"]
        combine[cid] = {
            "content": item["content"],
            "es_score": item["score"],
            "vec_score": 0.0
        }
    # 向量结果合并，更新相似度分数
    for doc, vec_score in vec_res:
        cid = doc.metadata["chunk_id"]
        if cid in combine:
            combine[cid]["vec_score"] = vec_score
        else:
            combine[cid] = {
                "content": doc.page_content,
                "es_score": 0.0,
                "vec_score": vec_score
            }
    # 简单融合排序：向量相似度为主
    final_list = sorted(combine.values(), key=lambda x: x["vec_score"], reverse=True)
    return final_list
