import jieba
import warnings
import numpy as np

from rank_bm25 import BM25Okapi
from elasticsearch import Elasticsearch
from elasticsearch import ElasticsearchWarning

warnings.filterwarnings("ignore", category=ElasticsearchWarning)

# 2. 准备分词后的文档（关键步骤）
# docs = [
#     "Python 是一种编程语言",
#     "Python 也用于数据分析",
#     "BM25 用于信息检索",
#     "BM25 是TF-IDE的扩展"
# ]
# tokenized_corpus = [list(jieba.cut(doc)) for doc in docs]
#
# # 3. 初始化模型
# bm25 = BM25Okapi(tokenized_corpus)
#
# # 4. 准备分词后的查询并打分
# query_raw = "扩展"
# tokenized_query = list(jieba.cut(query_raw))
#
# scores = bm25.get_scores(tokenized_query)
# sorted_doc = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
#
# for doc, score in sorted_doc:
#     print(doc, score)
# ```:ml-citation{ref="5,10" appearance="aggregated" data="citationList"}
#
# :::ml-data{name=citationList}
# ```json

def get_from_es() -> list:
    es = Elasticsearch("http://localhost:9200")
    index_name = "my_index"
    query = {
        "query": {
            "match_all": {}
        }
    }
    response = es.search(index=index_name, body=query)
    documents = response['hits']['hits']
    print(f"documents type: {type(documents)}")
    return documents

def search(query_text):
    documents = get_from_es()
    texts = [doc['_source']['title'] for doc in documents]
    print(f"documents: {documents}")
    print(f"texts: {texts}")
    bm25 = BM25Okapi(texts)
    # 将查询转换为索引中的格式（通常是分词）
    doc_scores = bm25.get_scores(query_text)  # 获取查询得分，这里的得分可以用来排序结果
    sorted_doc = sorted(zip(texts, doc_scores), key=lambda x: x[1], reverse=True)
    for doc, score in sorted_doc:
        print(doc, score)
    sorted_indexes = np.argsort(doc_scores)[::-1]  # 对索引进行降序排序以获取最高得分的文档索引
    print(f"doc_scores: {doc_scores}")
    print(f"sorted_indexes: {sorted_indexes}")
    top_docs = [documents[i]['_source'] for i in sorted_indexes[:10]]  # 获取前10个文档作为结果（可根据需要调整数量）
    return top_docs

if __name__ == '__main__':
    # documents = get_from_es()
    # print("======================================")
    # print(f"documents: {documents}")
    # print("======================================")
    query = "Java"
    results = search(query)
    print(results)