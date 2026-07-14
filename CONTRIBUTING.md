# Contributing

## 运行须知

### 初次运行

- 全量采集约 5000 只股票，每只 4 次 API 调用，耗时约 60-90 分钟
- 后续运行仅更新 PubDate 晚于上次记录的股票（增量）
- 单只失败 3 次跳过，记录到 `data/日志/failures.log`

### 环境变量

```bash
cp .env.example .env
# 填入 DEEPSEEK_API_KEY（热点分析和点评需要）
```

## 测试

### 测试分层

| 层 | 工具 | 位置 | 职责 |
|---|------|------|------|
| **单元测试** | `pytest` | `tests/` | 数据映射、过滤、清洗、指标计算逻辑 |
| **集成测试** | `pytest -m integration` | `integrated_tests/` | akshare API 字段名验证、真实采集验证 |

### 运行

```bash
# 单元测试（不调外部 API）
uv run pytest tests/ -v

# 集成测试单独（调 akshare 真实接口）
uv run pytest integrated_tests/ -v -m integration

# 全部测试
uv run pytest tests/ integrated_tests/ -v

# 验证采集（采样 5 只）
uv run python tests/verify_collect.py
```

### 目录约定

```
tests/              # 单元测试（不依赖外部 API）
├── test_collector.py    # 采集引擎测试
├── test_formulas.py     # 指标计算测试
└── verify_collect.py    # 真实接口验证脚本
integrated_tests/   # 集成测试（调外部 API）
└── test_collector.py    # akshare 接口字段名验证
```

### 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 测试文件 | `test_*.py` | `test_collector.py` |
| 测试函数 | `test_<场景>` | `test_veto_pass` |

## 定时调度

```bash
# 每日 9:00 和 17:00 自动执行：热点追踪 → 持股监控 → 推送
```

实现参考 `ROADMAP.md` v0.4.0。

## 发布

```bash
# 更新 CHANGELOG.md
# 更新 pyproject.toml 中 version
git commit -m "chore: bump version to x.y.z"
git tag vx.y.z
git push --tags
```
