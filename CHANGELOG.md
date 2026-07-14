# Changelog

## [0.1.0] - 2026-07-14

### Added
- 初始化项目结构：pyproject.toml、CHANGELOG、CONTRIBUTING、ROADMAP、TODO
- 数据采集引擎（collector）：同花顺/东财/巨潮四接口，全 A 股财报采集
- 配置模块：settings / industry_map / industry_weights / scoring_rules
- 工具模块：formulas（衍生指标计算）、helpers（xlsx 读写）、sw_mapper（申万行业映射）
- 测试：test_collector（映射/过滤/清洗）、test_formulas（指标计算）、verify_collect（真实采集验证）

### Changed
- 重构为 src/ 包布局，包名 `alpha_jerry`
- requirements.txt → pyproject.toml
