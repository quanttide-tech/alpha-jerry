# AlphaJerry

A 股基本面分析 AI Agent。数据采集 → 评分评级 → 荐股报告 → 持仓监控 → 热点追踪 → 推送。

## 技术选型

| 层级 | 技术 | 理由 |
|:--|:--|:--|
| 语言 | Python 3.11+ | 数据处理 + AI 生态最成熟 |
| LLM API | DeepSeek API | 国产性价比最优，百万 token 约 ¥1-2 |
| 网页 UI | Gradio | 聊天界面 + DataFrame 表格 |
| 数据采集 | akshare | 开源 A 股数据接口，覆盖东财/同花顺 |
| 数据处理 | pandas / openpyxl | xlsx 读写 + 向量化计算 |
| 定时调度 | schedule | 轻量级 Python 调度库 |
| 推送 | smtplib + 企业微信 webhook | 免费稳定 |

## 项目结构

```
alpha-jerry/
├── pyproject.toml
├── src/alpha_jerry/  →  config/  engine/  agent/  ui/  utils/
├── tests/            →  test_collector  test_formulas  verify_collect
├── data/             →  财务/  分析/  持股/  热点/  缓存/  日志/
└── docs/             →  dev-guide.md（领域规则）
```

## 架构

```
Gradio UI  ←→  Agent 编排层 (orchestrator)  ←→  核心引擎层 (engine)  ←→  数据层 (data/)
```

三层分离：Core Engine 不依赖 UI 和 Agent，可独立脚本调用。

## 快速开始

```bash
uv sync
uv run pytest tests/ -v -m "not integration"
```

## 功能

| 步骤 | 功能 | 产出 |
|------|------|------|
| ① 采集 | akshare 四个接口爬全 A 股最新财报 | `data/财务/YYMMDD.xlsx` |
| ② 评分 | 一票否决 + 三维度评分（成长/稳健/回报）加权 | `data/财务/YYMMDD-评分.xlsx` |
| ③ 评级 | 综合分 → 皇冠明珠/优秀白马/鸡肋/垃圾 | `data/财务/YYMMDD-评级.xlsx` |
| ④ 报告 | Top 20 + 公司分类 + AI 点评 | `data/分析/YYMMDD-荐股.xlsx` |

**扩展功能：** 热点追踪（微博/百度 + LLM 分析）、持股监控（评分变化 → 操作建议）、邮件推送、定时调度（9:00 / 17:00）。

## CLI 命令

```bash
uv run python -m alpha_jerry.engine.collector     # 采集
uv run python -m alpha_jerry.engine.scorer        # 评分
uv run python -m alpha_jerry.engine.rater         # 评级
uv run python -m alpha_jerry.engine.reporter      # 荐股报告
uv run pytest tests/ -v                           # 测试
```

## 成本

LLM 日耗 ≈ ¥0.05（20 只点评 × 1 次 + 热点分析 × 2 次）。

## 文档

- [开发指南](docs/dev-guide.md) — 特征工程、评分规则、评级标准
- [路线图](ROADMAP.md) — 版本规划
- [贡献指南](CONTRIBUTING.md) — 测试 / 运行 / 发布
