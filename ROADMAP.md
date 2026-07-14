---
tags: [协作]
date: 2026-07-14
---

# AlphaJerry 路线图

A 股基本面分析 AI Agent。数据采集 → 评分评级 → 荐股报告 → 持仓监控 → 热点追踪 → 推送。

## 版本策略

当前所有组件处于 `0.MINOR.PATCH` 阶段。单仓单组件，版本号记录在 `CHANGELOG.md`。

| 版本 | 目标 | 状态 |
|------|------|------|
| v0.1.0 | 核心引擎可用 | 🏗️ 进行中 |
| v0.2.0 | CLI + Agent | 📋 规划 |
| v0.3.0 | Gradio UI | 📋 规划 |
| v0.4.0 | 监控运维自动化 | 📋 规划 |

---

## v0.1.0 — 核心引擎可用

> 采集 → 评分 → 评级 → 荐股报告全流程可跑。不依赖 CLI / Agent / UI。

### Phase 1.1：工程基建

- [x] pyproject.toml / .python-version / CHANGELOG / CONTRIBUTING / ROADMAP / TODO
- [x] src/ 包布局，导入路径更新

**验收：**

```bash
uv run pytest tests/ -v -m "not integration"
```

### Phase 1.2：评分引擎

- [ ] 从 ROADMAP 提取代码到 `src/alpha_jerry/engine/scorer.py`
  - `veto_check(row)` — 一票否决
  - `calc_growth_score(row)` — 成长性
  - `calc_stability_score(row)` — 稳健性
  - `calc_return_score(row)` — 回报性
  - `calc_composite_score(row, w_growth, w_stability, w_return)` — 综合分
  - `score_all(input_path, output_path)` — 批量评分

**测试：** `tests/test_scorer.py`（9 个场景）

**验收：**

```bash
uv run pytest tests/test_scorer.py -v            # 9 passed
uv run python -c "
from alpha_jerry.engine.scorer import score_all
df = score_all()
print(df[['股票代码','综合分','否决']].head())
"
```

### Phase 1.3：评级 + 报告引擎

- [ ] `src/alpha_jerry/engine/rater.py` — `apply_rating()` / `rate_all()`
- [ ] `src/alpha_jerry/engine/reporter.py` — `classify_company()` / `generate_report()`

**测试：** `tests/test_rater.py` + `tests/test_reporter.py`

**验收：**

```bash
uv run pytest tests/test_rater.py tests/test_reporter.py -v  # 4 passed
uv run python -c "
from alpha_jerry.engine.collector import collect_all
from alpha_jerry.engine.scorer import score_all
from alpha_jerry.engine.rater import rate_all
from alpha_jerry.engine.reporter import generate_report
collect_all(); score_all(); rate_all()
report = generate_report()
print(report[['股票代码','综合分','评级']].head(5))
"
```

### Phase 1.4：测试数据重构

- [ ] `tests/conftest.py` — session 级 fixture 加载
- [ ] `tests/fixtures/` — JSON 测试数据
- [ ] 测试改用 `tmp_path`

---

## v0.2.0 — CLI + Agent

> 通过 `python -m alpha_jerry` 等命令操作，不依赖 UI。

### Phase 2.1：CLI 入口

- [ ] `src/alpha_jerry/__main__.py` — click 命令组

| 命令 | 功能 |
|------|------|
| `collect` | 采集全 A 股财报 |
| `score` | 评分 + 评级 |
| `report` | 生成 Top 20 荐股报告 |
| `hold-add <code> <name>` | 添加持仓 |
| `hold-list` | 查看持仓 |

### Phase 2.2：Agent 编排层

- [ ] `src/alpha_jerry/agent/orchestrator.py` — DeepSeek Function Calling

**验收：**

```bash
uv run python -m alpha_jerry --help                  # 命令列表
uv run python -c "from alpha_jerry.agent.orchestrator import chat; print(chat('你好'))"
```

---

## v0.3.0 — Gradio UI

- [ ] `src/alpha_jerry/ui/app.py` — 三个 Tab：对话 / 一键分析 / 最新荐股

**验收：**

```bash
uv run python -m alpha_jerry ui          # 浏览器访问 http://127.0.0.1:7860
```

---

## v0.4.0 — 监控运维自动化

> 系统自动定时运行，推送分析结果。

### Phase 4.1：持股监控

- [ ] `src/alpha_jerry/engine/monitor.py` — 逐只持仓评分 + 操作建议

### Phase 4.2：热点追踪

- [ ] `src/alpha_jerry/engine/hot_tracker.py` — 微博/百度热搜 + LLM 分析

### Phase 4.3：推送 + 调度

- [ ] `src/alpha_jerry/engine/pusher.py` — SMTP 邮件推送
- [ ] `src/alpha_jerry/engine/scheduler.py` — 每日 9:00 / 17:00 定时执行

**验收：**

```bash
uv run python -c "from alpha_jerry.engine.scheduler import start,stop; start(); import time; time.sleep(2); stop()"
uv run python -c "from alpha_jerry.engine.hot_tracker import track_hotspots; print(track_hotspots())"
```

---

## 验收检查清单

| 版本 | 验收标准 | 检验命令 |
|------|---------|---------|
| v0.1.0 | 采集 → 评分 → 报告全流程可跑 | `live run pytest tests/ -v` |
| v0.1.0 | 单测全部通过 | `uv run pytest tests/ -v -m "not integration"` |
| v0.2.0 | CLI 命令可用 | `uv run python -m alpha_jerry --help` |
| v0.2.0 | Agent tool calling 正常 | `uv run python -c "from alpha_jerry.agent.orchestrator import chat; print(chat('你好'))"` |
| v0.3.0 | Gradio 界面可打开 | `uv run python -m alpha_jerry ui` |
| v0.4.0 | 调度器启停正常 | `uv run python -c "from alpha_jerry.engine.scheduler import start,stop; start();...;stop()"` |
| v0.4.0 | 热点采集成功 | `uv run python -c "from alpha_jerry.engine.hot_tracker import fetch_weibo_hot; print(len(fetch_weibo_hot()))"` |
