# Contributing

## 测试

### 测试分层

| 层 | 工具 | 位置 | 职责 |
|---|------|------|------|
| **单元测试** | `pytest` | `tests/` | 数据映射、过滤、清洗、指标计算逻辑 |
| **集成测试** | `pytest -m integration` | `tests/test_collector.py` | akshare API 字段名验证、真实采集验证 |

### 运行

```bash
# 单元测试
uv run pytest tests/ -v -m "not integration"

# 全部测试（含集成）
uv run pytest tests/ -v

# 集成测试单独
uv run pytest tests/ -v -m integration

# 验证采集（采样 5 只）
uv run python tests/verify_collect.py
```

### 目录约定

```
tests/
├── conftest.py          # 共享 fixture 和工具检测
├── test_collector.py    # 采集引擎测试
├── test_formulas.py     # 指标计算测试
└── verify_collect.py    # 真实接口验证脚本
```

### 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 测试文件 | `test_*.py` | `test_collector.py` |
| 测试函数 | `test_<场景>` | `test_veto_pass` |

## 发布

```bash
# 更新 CHANGELOG.md
# 更新 pyproject.toml 中 version
# 提交 + 打标签
git commit -m "chore: bump version to x.y.z"
git tag vx.y.z
git push --tags
```
