from pydantic import BaseModel

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
    category: str
    question: str          # 给Agent的问题
    standard_answer: str      # 标准答案

# unknow 测试
UNKNOW_BENCHMARK_TASKS = [
    BenchTask(
        task_id="unknow_001",
        category="unknow",
        question="我好看吗",
        standard_answer="unknow",
    ),
    BenchTask(
        task_id="unknow_002",
        category="unknow",
        question="当前天气怎么样",
        standard_answer="unknow",
    ),
    BenchTask(
        task_id="unknow_003",
        category="unknow",
        question="你是谁",
        standard_answer="unknow",
    ),
    BenchTask(
        task_id="unknow_004",
        category="unknow",
        question="你知道我是谁不",
        standard_answer="unknow",
    )
]

# query_oncall 测试
QUERY_ONCALL_BENCHMARK_TASKS = [
    BenchTask(
        task_id="query_oncall_001",
        category="query_oncall",
        question="当前oncall是谁",
        standard_answer="query_oncall",
    ),
    BenchTask(
        task_id="query_oncall_002",
        category="query_oncall",
        question="这周谁值班",
        standard_answer="query_oncall",
    ),
    BenchTask(
        task_id="query_oncall_003",
        category="query_oncall",
        question="这个问题找谁排查",
        standard_answer="query_oncall",
    ),
]

# query_latest_version 测试
QUERY_LATEST_VERSION_BENCHMARK_TASKS = [
    BenchTask(
        task_id="query_latest_version_001",
        category="query_latest_version",
        question="provider的最新版本是多少",
        standard_answer="query_latest_version",
    ),
    BenchTask(
        task_id="query_latest_version_002",
        category="query_latest_version",
        question="现在provider发布到哪个版本了",
        standard_answer="query_latest_version",
    ),
    BenchTask(
        task_id="query_latest_version_003",
        category="query_latest_version",
        question="当前provider的版本是多少",
        standard_answer="query_latest_version",
    ),
]

# query_reference_docs 测试
QUERY_REFERENCE_DOCS_BENCHMARK_TASKS = [
    BenchTask(
        task_id="query_reference_docs_001",
        category="query_reference_docs",
        question="provider的参考文档是啥",
        standard_answer="query_reference_docs",
    ),
    BenchTask(
        task_id="query_reference_docs_002",
        category="query_reference_docs",
        question="参考文档在哪里",
        standard_answer="query_reference_docs",
    ),
    BenchTask(
        task_id="query_reference_docs_003",
        category="query_reference_docs",
        question="有没有使用文档",
        standard_answer="query_reference_docs",
    ),
    BenchTask(
        task_id="query_reference_docs_004",
        category="query_reference_docs",
        question="有没有说明文档",
        standard_answer="query_reference_docs",
    ),
    BenchTask(
        task_id="query_reference_docs_005",
        category="query_reference_docs",
        question="这个参数怎么用",
        standard_answer="query_reference_docs",
    ),
    BenchTask(
        task_id="query_reference_docs_006",
        category="query_reference_docs",
        question="huaweicloud_lts_aom_access资源的这个参数支持吗",
        standard_answer="query_reference_docs",
    )
]

# whether_support_special_region 测试
WHETHER_SUPPORT_SPECIAL_REGION_BENCHMARK_TASKS = [
    BenchTask(
        task_id="whether_support_special_region_001",
        category="whether_support_special_region",
        question="provider都在哪几个region上线了?",
        standard_answer="whether_support_special_region",
    ),
    BenchTask(
        task_id="whether_support_special_region_002",
        category="whether_support_special_region",
        question="provider支持北京四这个region吗?",
        standard_answer="whether_support_special_region",
    ),
    BenchTask(
        task_id="whether_support_special_region_003",
        category="whether_support_special_region",
        question="provider支持cn-north-4这个region吗？",
        standard_answer="whether_support_special_region",
    ),
]

# query_resource_by_name 测试
QUERY_RESOURCE_BY_NAME_BENCHMARK_TASKS = [
    BenchTask(
        task_id="query_resource_by_name_001",
        category="query_resource_by_name",
        question="huaweicloud_lts_aom_access这个支持吗",
        standard_answer="query_resource_by_name",
    ),
    BenchTask(
        task_id="query_resource_by_name_002",
        category="query_resource_by_name",
        question="huaweicloud_lts_aom_access是啥",
        standard_answer="query_resource_by_name",
    ),
    BenchTask(
        task_id="query_resource_by_name_003",
        category="query_resource_by_name",
        question="huaweicloud_lts_aom_access这个资源/resource支持吗",
        standard_answer="query_resource_by_name",
    ),
    BenchTask(
        task_id="query_resource_by_name_004",
        category="query_resource_by_name",
        question="huaweicloud_lts_aom_access这个资源/resource是啥",
        standard_answer="query_resource_by_name",
    ),
    BenchTask(
        task_id="query_resource_by_name_005",
        category="query_resource_by_name",
        question="RDS服务huaweicloud_lts_aom_access这个支持吗",
        standard_answer="query_resource_by_name",
    ),
    BenchTask(
        task_id="query_resource_by_name_006",
        category="query_resource_by_name",
        question="RDS 服务huaweicloud_lts_aom_access这个是啥",
        standard_answer="query_resource_by_name",
    ),
    BenchTask(
        task_id="query_resource_by_name_007",
        category="query_resource_by_name",
        question="RDS服务huaweicloud_lts_aom_access这个资源/resource支持吗",
        standard_answer="query_resource_by_name",
    ),
    BenchTask(
        task_id="query_resource_by_name_008",
        category="query_resource_by_name",
        question="RDS 服务huaweicloud_lts_aom_access这个资源/resource是啥",
        standard_answer="query_resource_by_name",
    ),
]

# query_resource_by_api 测试
QUERY_RESOURCE_BY_API_BENCHMARK_TASKS = [
    BenchTask(
        task_id="query_resource_by_api_001",
        category="query_resource_by_api",
        question="/v3/{project_id}/lts/access-config 这个API支持吗",
        standard_answer="query_resource_by_api",
    ),
    BenchTask(
        task_id="query_resource_by_api_002",
        category="query_resource_by_api",
        question="v3/{project_id}/lts/access-config 这个API集成了吗",
        standard_answer="query_resource_by_api",
    ),
    BenchTask(
        task_id="query_resource_by_api_003",
        category="query_resource_by_api",
        question="哪里用到了 /v3/{project_id}/lts/access-config 这个API",
        standard_answer="query_resource_by_api",
    ),
    BenchTask(
        task_id="query_resource_by_api_004",
        category="query_resource_by_api",
        question="DELETE /v3/{project_id}/lts/access-config 这个API支持吗",
        standard_answer="query_resource_by_api",
    ),
    BenchTask(
        task_id="query_resource_by_api_005",
        category="query_resource_by_api",
        question="DELETE /v3/{project_id}/lts/access-config 这个API集成了吗",
        standard_answer="query_resource_by_api",
    ),
    BenchTask(
        task_id="query_resource_by_api_006",
        category="query_resource_by_api",
        question="哪个资源用到了DELETE /v3/{project_id}/lts/access-config 这个API",
        standard_answer="query_resource_by_api",
    ),
    BenchTask(
        task_id="query_resource_by_api_007",
        category="query_resource_by_api",
        question="LTS 服务的 /v3/{project_id}/lts/access-config 这个API支持吗",
        standard_answer="query_resource_by_api",
    ),
    BenchTask(
        task_id="query_resource_by_api_008",
        category="query_resource_by_api",
        question="LTS 服务的 /v3/{project_id}/lts/access-config 这个API集成了吗",
        standard_answer="query_resource_by_api",
    ),
    BenchTask(
        task_id="query_resource_by_api_009",
        category="query_resource_by_api",
        question="哪个资源用到了LTS 服务的 /v3/{project_id}/lts/access-config 这个API",
        standard_answer="query_resource_by_api",
    ),
    BenchTask(
        task_id="query_resource_by_api_010",
        category="query_resource_by_api",
        question="LTS 服务的 DELETE /v3/{project_id}/lts/access-config 这个API支持吗",
        standard_answer="query_resource_by_api",
    ),
    BenchTask(
        task_id="query_resource_by_api_011",
        category="query_resource_by_api",
        question="LTS 服务的 DELETE /v3/{project_id}/lts/access-config 这个API集成了吗",
        standard_answer="query_resource_by_api",
    ),
    BenchTask(
        task_id="query_resource_by_api_012",
        category="query_resource_by_api",
        question="哪个资源用到了LTS 服务的 DELETE /v3/{project_id}/lts/access-config 这个API",
        standard_answer="query_resource_by_api",
    ),
]

# query_resource_by_content 测试
QUERY_RESOURCE_BY_CONTENT_BENCHMARK_TASKS = [
    BenchTask(
        task_id="query_resource_by_content_001",
        category="query_resource_by_content",
        question="支持创建备份吗",
        standard_answer="query_resource_by_content",
    ),
    BenchTask(
        task_id="query_resource_by_content_002",
        category="query_resource_by_content",
        question="可以创建实例吗",
        standard_answer="query_resource_by_content",
    ),
    BenchTask(
        task_id="query_resource_by_content_003",
        category="query_resource_by_content",
        question="支持创建RDS备份吗",
        standard_answer="query_resource_by_content",
    ),
    BenchTask(
        task_id="query_resource_by_content_004",
        category="query_resource_by_content",
        question="可以创建DCS实例吗",
        standard_answer="query_resource_by_content",
    ),
]

BENCHMARK_TASKS = [
    *UNKNOW_BENCHMARK_TASKS,
    *QUERY_ONCALL_BENCHMARK_TASKS,
    *QUERY_LATEST_VERSION_BENCHMARK_TASKS,
    *QUERY_REFERENCE_DOCS_BENCHMARK_TASKS,
    *WHETHER_SUPPORT_SPECIAL_REGION_BENCHMARK_TASKS,
    *QUERY_RESOURCE_BY_NAME_BENCHMARK_TASKS,
    *QUERY_RESOURCE_BY_API_BENCHMARK_TASKS,
    *QUERY_RESOURCE_BY_CONTENT_BENCHMARK_TASKS,
]
