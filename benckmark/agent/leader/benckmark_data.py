import time
import json
import matplotlib.pyplot as plt
from pydantic import BaseModel, Field
from openai import OpenAI

# 评测维度
DIMENSIONS = [
    "correctness",    # 答案正确性 0-10
    "planning",       # 规划能力 0-10
    "tool_efficiency",# 工具调用效率 0-10
    "reflection"      # 自我纠错能力 0-10
]

# ===================== 1. 定义Benchmark任务结构 =====================
class BenchTask(BaseModel):
    task_id: str
    category: str          # 分类：数学推理/工具查询/多步骤规划/纠错任务
    question: str          # 给Agent的问题
    ground_truth: str      # 标准答案
    need_tool: bool        # 是否必须调用工具才能完成
    max_step: int = 5      # 最大允许思考步数

# 自建测试数据集（可无限扩充）
BENCHMARK_TASKS = [
    BenchTask(
        task_id="math_001",
        category="math_reason",
        question="一个商店进价100元的商品，加价30%售卖，再打9折出售，最终利润是多少？",
        ground_truth="售价=100*1.3*0.9=117元，利润=17元",
        need_tool=False,
        max_step=3
    ),
    BenchTask(
        task_id="plan_001",
        category="multi_step_plan",
        question="帮我规划下午流程：16点健身1小时，健身前买水，健身结束吃晚餐，晚餐需要预留40分钟，18:30必须到家，请问最晚几点出门买水？",
        ground_truth="最晚15:30出门买水",
        need_tool=False,
        max_step=4
    ),
    BenchTask(
        task_id="tool_001",
        category="tool_use",
        question="查询2026年8月1日是星期几，再计算距离2026年国庆节还有多少天",
        ground_truth="2026-08-01周六，距离国庆(10.1)共61天",
        need_tool=True,
        max_step=5
    ),
    BenchTask(
        task_id="error_001",
        category="reflection",
        question="小明计算：2*(3+5)=11，找出错误并给出正确结果",
        ground_truth="错误：2*8算成11，正确结果16",
        need_tool=False,
        max_step=2
    )
]

# ===================== 2. 简易可工具调用Agent（被测对象） =====================
class SimpleAgent:
    def __init__(self):
        self.step_records = []  # 记录每一步思考&动作
        self.tools = {
            "date_calc": self.tool_date_calc
        }

    def tool_date_calc(self, start_date: str, target_date: str):
        """日期计算工具"""
        from datetime import datetime
        fmt = "%Y-%m-%d"
        d1 = datetime.strptime(start_date, fmt)
        d2 = datetime.strptime(target_date, fmt)
        diff = (d2 - d1).days
        weekday = d1.weekday() + 1
        week_map = {1:"周一",2:"周二",3:"周三",4:"周四",5:"周五",6:"周六",7:"周日"}
        return f"{start_date}是{week_map[weekday]}，相差天数：{diff}"

    def run(self, task: BenchTask) -> dict:
        """Agent执行单个任务，支持思考+工具调用"""
        messages = [{"role": "system", "content": "你是智能Agent，可以调用工具date_calc(start_date, target_date)做日期计算。思考分步执行，需要工具就输出【TOOL:函数名|参数json】，回答最终答案输出【ANSWER:xxx】"}]
        messages.append({"role": "user", "content": task.question})
        steps = 0
        final_answer = ""

        while steps < task.max_step:
            steps += 1
            resp = CLIENT.chat.completions.create(model=MODEL_AGENT, messages=messages, temperature=0)
            content = resp.choices[0].message.content.strip()
            self.step_records.append({"step": steps, "content": content})
            messages.append({"role": "assistant", "content": content})

            # 触发工具调用
            if content.startswith("【TOOL:"):
                try:
                    tool_part = content.replace("【TOOL:", "").replace("】", "")
                    func_name, args_str = tool_part.split("|")
                    args = json.loads(args_str)
                    func = self.tools[func_name]
                    tool_res = func(**args)
                    messages.append({"role": "user", "content": f"工具返回结果：{tool_res}"})
                except Exception as e:
                    messages.append({"role": "user", "content": f"工具调用失败：{str(e)}，重新思考"})
                continue

            # 拿到最终答案
            if "【ANSWER:" in content:
                final_answer = content.split("【ANSWER:")[-1].replace("】", "")
                break
        return {
            "final_answer": final_answer,
            "step_count": steps,
            "step_records": self.step_records
        }

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