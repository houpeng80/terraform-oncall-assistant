import json
import pandas as pd
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage
from openai import OpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

from assistant.config.config import get_app_config
from assistant.model import get_model
from benckmark.agent.intent_recognize.benckmark_data import BenchTask

model = get_model(get_app_config().model_type)

# ===================== 3. LLM评测裁判 Judge =====================
def judge_task(task: BenchTask, agent_output: dict) -> dict:
    """裁判打分，返回四个维度分数+评语"""
    prompt = f"""
【评测任务】
问题：{task.question}
标准答案：{task.ground_truth}
Agent最终回答：{agent_output['final_answer']}
Agent思考过程：{json.dumps(agent_output['step_records'], ensure_ascii=False)}
要求：
1. 按照4个维度分别打出0~10整数分数：correctness答案正确性、planning规划能力、tool_efficiency工具效率、reflection纠错能力
2. 返回JSON格式，key为四个维度+comment评语
"""
    resp = CLIENT.chat.completions.create(model=MODEL_JUDGE, messages=[{"role":"user","content":prompt}], temperature=0)
    raw = resp.choices[0].message.content
    # 提取json
    json_str = raw[raw.find("{"):raw.rfind("}")+1]
    score_data = json.loads(json_str)
    return score_data

# ===================== 4. 批量运行Benchmark & 结果统计 =====================
def run_benchmark():
    all_results = []
    for task in BENCHMARK_TASKS:
        print(f"\n===== 开始评测任务 {task.task_id} | {task.category} =====")
        agent = SimpleAgent()
        start_t = time.time()
        agent_res = agent.run(task)
        cost_t = time.time() - start_t
        scores = judge_task(task, agent_res)
        record = {
            "task_id": task.task_id,
            "category": task.category,
            "cost_time": round(cost_t,2),
            "step_used": agent_res["step_count"],
            "agent_ans": agent_res["final_answer"],
            "scores": scores
        }
        all_results.append(record)
        print(f"得分：{scores}，耗时：{cost_t}s")
    return all_results

# ===================== 5. 结果可视化 =====================
def visualize_result(results):
    # 按类别聚合平均分
    cat_score = {}
    for item in results:
        cat = item["category"]
        if cat not in cat_score:
            cat_score[cat] = {d:[] for d in DIMENSIONS}
        for dim in DIMENSIONS:
            cat_score[cat][dim].append(item["scores"][dim])

    cats = list(cat_score.keys())
    avg_scores = []
    for c in cats:
        avg = [sum(cat_score[c][d])/len(cat_score[c][d]) for d in DIMENSIONS]
        avg_scores.append(avg)

    # 绘图
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    x = list(range(len(DIMENSIONS)))
    for idx, cat in enumerate(cats):
        plt.plot(x, avg_scores[idx], marker="o", label=cat)
    plt.xticks(x, DIMENSIONS)
    plt.legend()
    plt.title("Agent Benchmark 各维度平均分")
    plt.ylabel("分数 0-10")
    plt.grid(True, alpha=0.3)
    plt.show()

# ===================== 入口执行 =====================
if __name__ == "__main__":
    bench_res = run_benchmark()
    visualize_result(bench_res)
    # 保存评测报告
    with open("agent_bench_report.json","w",encoding="utf-8") as f:
        json.dump(bench_res, f, ensure_ascii=False, indent=2)
    print("\n评测完成，报告已保存 agent_bench_report.json")