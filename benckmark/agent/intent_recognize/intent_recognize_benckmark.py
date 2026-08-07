import json
import time

from langchain_core.messages import SystemMessage, HumanMessage

from assistant.config.config import get_app_config
from assistant.model import get_model
from assistant.sub_agents.intent_recognition.intent_recognize import IntentRecognize

from benckmark.agent.intent_recognize.benckmark_data import BenchTask, BENCHMARK_TASKS, DIMENSIONS

model = get_model(get_app_config().model_type)

def judge_task(task: BenchTask, agent_output: dict) -> dict:
    """裁判打分，返回四个维度分数+评语"""
    prompt = f"""
【评测任务】
问题：{task.question}
标准答案：{task.standard_answer}
Agent最终回答：{agent_output.intent}
要求：
1. 按照4个维度分别打出0~10整数分数：correctness答案正确性、planning规划能力、tool_efficiency工具效率、reflection纠错能力
2. 返回JSON格式，key为四个维度+comment评语
"""
    messages = [SystemMessage(content=prompt)]
    resp = model.invoke(messages)
    return resp.content

def run_benchmark():
    all_results = []
    config = {"configurable": {"thread_id": "user-001"}}
    for task in BENCHMARK_TASKS:
        input_message = {
            "messages": [HumanMessage(content=task.question)],
            "input_token_statistics": 0,
            "output_token_statistics": 0,
            "total_token_statistics": 0,
            "model_cycle_time": 1,
        }
        print(f"\n===== 开始评测任务 {task.task_id} | {task.category} =====")
        agent = IntentRecognize(config=config)
        start_t = time.time()
        agent_res = agent.intent_recognize(input_message)
        print("agent_res: ", agent_res)
        cost_t = time.time() - start_t
        scores = judge_task(task, agent_res)
        record = {
            "task_id": task.task_id,
            "category": task.category,
            "cost_time": round(cost_t,2),
            "intent": agent_res.intent,
            "params": agent_res.params,
            "missing_params": agent_res.missing_params,
            "reasoning": agent_res.reasoning,
            "scores": scores
        }
        all_results.append(record)
        print(f"得分：{scores}，耗时：{cost_t}s")
    return all_results

if __name__ == "__main__":
    bench_res = run_benchmark()
    print("================")
    print(bench_res)
    print("================")
    with open("agent_bench_report.json","w",encoding="utf-8") as f:
        json.dump(bench_res, f, ensure_ascii=False, indent=2)
    print("\n评测完成，报告已保存 agent_bench_report.json")