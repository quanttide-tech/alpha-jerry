# TODO — 当前任务

---

## v0.1.0（当前）

### Phase 1.1：工程基建
- [x] pyproject.toml / .python-version / CHANGELOG / CONTRIBUTING / ROADMAP / TODO

### Phase 1.2：评分引擎
- [ ] 从 ROADMAP 提取 scorer.py
- [ ] tests/test_scorer.py（9 个测试）

### Phase 1.3：评级 + 报告引擎
- [ ] 从 ROADMAP 提取 rater.py / reporter.py
- [ ] tests/test_rater.py + test_reporter.py

### Phase 1.4：测试数据重构
- [ ] tests/conftest.py（session 级 fixture 加载）
- [ ] tests/fixtures/（JSON 测试数据）
- [ ] 测试改用 tmp_path

---

## v0.2.0

- [ ] CLI 入口 main.py（click）
- [ ] Agent 编排层 agent/orchestrator.py

## v0.3.0

- [ ] Gradio UI ui/app.py

## v0.4.0

- [ ] 持股监控 engine/monitor.py
- [ ] 热点追踪 engine/hot_tracker.py
- [ ] 推送 engine/pusher.py
- [ ] 调度 engine/scheduler.py
