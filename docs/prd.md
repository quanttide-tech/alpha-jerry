---
tags: [协作]
date: 2026-06-21
---

# PRD — 产品需求文档

开发一套低成本、开源的 AI Agent 工具，覆盖 A 股基本面分析的完整工作流，帮助投资者识别优质公司并监控持仓。

## 技术选型

| 层级 | 技术 | 理由 |
|:--|:--|:--|
| 语言 | Python 3.11+ | 数据处理 + AI 生态最成熟 |
| LLM API | DeepSeek API | 国产性价比最优，百万 token 约 ¥1-2 |
| 网页 UI | Gradio | 聊天界面 + DataFrame 表格，组件丰富 |
| 数据采集 | akshare | 开源 A 股数据接口，覆盖东财/同花顺 |
| 数据处理 | pandas / openpyxl | xlsx 读写 + 向量化计算 |
| 定时调度 | schedule | 轻量级 Python 调度库 |
| 推送 | smtplib + 企业微信 webhook | 免费稳定 |

## 项目结构

```
alpha-jerry/
├── pyproject.toml
├── CHANGELOG.md
├── CONTRIBUTING.md
├── ROADMAP.md
├── TODO.md
├── src/
│   └── alpha_jerry/
│       ├── config/
│       │   ├── settings.py
│       │   ├── scoring_rules.py
│       │   ├── industry_map.py
│       │   └── industry_weights.py
│       ├── engine/
│       │   ├── collector.py
│       │   ├── scorer.py
│       │   ├── rater.py
│       │   ├── reporter.py
│       │   ├── monitor.py
│       │   ├── hot_tracker.py
│       │   ├── pusher.py
│       │   └── scheduler.py
│       ├── agent/
│       │   └── orchestrator.py
│       ├── ui/
│       │   └── app.py
│       └── utils/
│           ├── formulas.py
│           ├── helpers.py
│           └── sw_mapper.py
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   ├── test_collector.py
│   ├── test_formulas.py
│   └── verify_collect.py
├── data/
│   ├── 财务/
│   ├── 分析/
│   ├── 持股/
│   ├── 热点/
│   ├── 缓存/
│   └── 日志/
├── docs/
│   ├── brd.md
│   └── prd.md
```

## 架构总览

```
┌──────────────────────────────────────────┐
│              Gradio Web UI               │
│         (对话面板 + 表格 + 图表)           │
└────────────────┬─────────────────────────┘
                 │
┌────────────────▼─────────────────────────┐
│           Agent 编排层 (orchestrator)     │
│   自然语言 → LLM 意图识别 → 路由引擎      │
│   工具: collect / score / report         │
│         hold / monitor / hot / push      │
└────────────────┬─────────────────────────┘
                 │
┌────────────────▼─────────────────────────┐
│              核心引擎层 (engine)           │
│                                         │
│  collector  scorer  rater  reporter     │
│  monitor  hot_tracker  pusher  scheduler│
└────────────────┬─────────────────────────┘
                 │
┌────────────────▼─────────────────────────┐
│              数据层 (data/)               │
│  财务/ 分析/ 持股/ 热点/ 缓存/ 日志/       │
└──────────────────────────────────────────┘
```

三层分离：Core Engine 不依赖 UI 和 Agent，可独立脚本调用；Agent 层封装 LLM，做意图识别和工具编排；Gradio UI 只负责展示和交互。

## 数据采集引擎

### 流程

```
akshare 获取全 A 股票列表
  → 逐只爬取最新财报（资产负债表 + 利润表 + 现金流量表）
  → 字段映射标准化
  → 计算衍生指标（ALR / CR / EM / NPR / OPM / NPM / IPR / CFR）
  → 保存 data/财务/YYMMDD.xlsx
```

### 数据源接口

| 接口 | 数据源 | 用途 |
|:--|:--|:--|
| `ak.stock_info_a_code_name()` | 东财 | 全部 A 股代码 + 名称（批量 1 次） |
| `ak.stock_financial_debt_new_ths(symbol, "按报告期")` | 同花顺 | 资产负债表 |
| `ak.stock_financial_benefit_new_ths(symbol, "按报告期")` | 同花顺 | 利润表 |
| `ak.stock_financial_cash_new_ths(symbol, "按报告期")` | 同花顺 | 现金流量表 |
| `ak.stock_profile_cninfo(symbol)` | 巨潮 | 个股概况：上市日期 |
| `sw_index_first_info()` + `index_component_sw(code)` | 申万指数 | 全 A 股 → 申万一级行业映射 |

### 字段空值策略

- 必填字段（缺失则丢弃整行）：`Code` `Name` `Rev` `NP` `TA` `TL` `SE` `CA` `CL` `OCF` `PubDate` `Period` `ListDate` `行业属性`
- 可空默认 `0`：`InvP` `NRI` `LTL` `FA` `IA` `ICF` `CFF`
- 可空保留：`GP` `OP` `RE` `APIC` `EPS` `BVPS` `ROE` `净利润同比增长率` `主营收入同比增长率`

## 评分引擎

### 流程

```
读取 data/财务/YYMMDD.xlsx
  → 一票否决筛选
  → 行业分类映射（申万 → 5 大类）
  → 成长性评分（营收增速 + 净利增速）
  → 稳健性评分（资产负债率 + 流动比率）
  → 资金回报评分（ROE）
  → 读取行业权重表
  → 综合分 = 成长分×w1 + 稳健分×w2 + 回报分×w3
  → 保存 data/财务/YYMMDD-评分.xlsx
```

### 一票否决

| 否决项 | 实现方式 | 标记 |
|:--|:--|:--|
| 造假嫌疑 | 规则自动：OCF/NP<0.5 | `Fraud` |
| 诚信问题 | LLM 联网搜索（二期） | `Credibility` |
| 行业毁灭 | LLM 联网搜索（二期） | `IndustryDeath` |

### 行业权重

```python
INDUSTRY_WEIGHTS = {
    "周期资源":     {"growth": 0.25, "stability": 0.35, "return": 0.40},
    "大消费":       {"growth": 0.30, "stability": 0.30, "return": 0.40},
    "证券金融":     {"growth": 0.30, "stability": 0.30, "return": 0.40},
    "科技/制造":   {"growth": 0.50, "stability": 0.20, "return": 0.30},
    "公用事业/基建": {"growth": 0.20, "stability": 0.40, "return": 0.40},
}
```

## 评级引擎

| 综合分 | 评级 |
|:--|:--|
| 8.5 - 10.0 | 皇冠明珠 |
| 7.0 - 8.4 | 优秀白马 |
| 5.5 - 6.9 | 鸡肋/观察 |
| < 5.5 | 垃圾时间 |

否决股票标为「否决」，不参与评级。

## 报告引擎

- 取前 20 名，按公司类型分类（千里马 / 现金牛 / 护城河）
- LLM 生成核心亮点（≤30 字）+ 点评（≤50 字）

### 公司类型判定

| 条件 | 类型 |
|------|------|
| 科技/制造 且 营收增速 > 15% | 千里马 |
| 公用事业/基建 且 营收增速 > 15% | 千里马 |
| 周期资源 且 营收增速 > 30% | 千里马 |
| 大消费 且 毛利率 > 50% | 护城河 |
| 毛利率 > 40% 且 ROE > 15 | 护城河 |
| 其余 | 现金牛 |

### 日耗 LLM 估算

| 调用 | 日频 | Token 估算 | 花费 |
|:--|:--|:--|:--|
| 荐股点评 20 只 | 1 次 | ~3000 | < ¥0.01 |
| 热点分析 | 2 次 | ~2000/次 | < ¥0.01 |
| 合计 | | | < ¥0.05/天 |

## 热点追踪

```
9:00 / 17:00 触发
  → 爬取百度 / 微博热搜前 10
  → 合并去重，关键词匹配行业
  → LLM 分析：市场机会 + 受益板块 + 关联个股
  → 输出 data/热点/YYMMDD-09.md（-17.md）
```

## 持股监控

- 逐只重新采集最新财报 → 重新评分
- 对比上次评分变化 → 操作建议（持有 / 加仓 / 减仓 / 止损）

| 综合分变化 | 建议 |
|:--|:--|
| 上升 > 1 | 加仓 |
| 下降 1 - 2 | 减仓 |
| 下降 > 2 | 止损 |
| 其余 | 持有 |

## 消息推送

| 渠道 | 内容 | 方式 |
|:--|:--|:--|
| 邮件 | 完整分析 + HTML 表格 | `smtplib` |
| 微信（可选） | 持仓摘要 + Top 5 热点 | 企业微信群机器人 webhook |

## 定时调度

```
09:00  → hot_tracker + monitor + push
17:00  → hot_tracker + monitor + push
财报季后 → 手动全量更新
```

## CLI 命令清单

| 命令 | 功能 |
|------|------|
| `python -m alpha_jerry.engine.collector` | 数据采集 |
| `python -m alpha_jerry.engine.scorer` | 评分 |
| `python -m alpha_jerry.engine.rater` | 评级 |
| `python -m alpha_jerry.engine.reporter` | 生成荐股报告 |
