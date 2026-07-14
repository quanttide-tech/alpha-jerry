# 技术债务

## xlsx 数据来源标注不可维护

`DATA_SOURCE` 字典（`engine/collector.py`）手动维护了每个字段的数据来源，写入 xlsx 第二个 sheet。

**问题**：新建或删除字段时，必须同步更新 `DATA_SOURCE`，否则来源说明会和实际数据不一致。当前没有任何机制保证两者同步——`DATA_SOURCE` 中的 key 和实际输出列可能随时漂移。

**根因**：这些 metadata 是纯描述性文本，无法通过类型系统或测试自动约束。每个字段的来源是"同花顺利润表"还是"计算值"是领域知识，代码无法自行推断。

**根治方向**：如果要彻底解决，需要把字段定义从分散的列表/字典（`FIELD_MAP`、`REQUIRED_FIELDS`、`DEFAULT_ZERO_FIELDS`、`THS_DEBT_METRICS` 等）收拢为单一字段注册表（例如 dataclass 或 YAML 配置），在字段定义处声明来源，自动生成 `DATA_SOURCE`。但这样做引入了新的抽象层，收益（xlsx 多一个 sheet）与成本（一人项目维护一份额外注册表）不成比例。

**结论**：当前手动维护。如果 `DATA_SOURCE` 和实际列不一致，不影响数据采集，只影响 xlsx 中「数据来源」sheet 的准确性。
