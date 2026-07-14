import pytest
from alpha_jerry.engine.collector import THS_DEBT_METRICS, THS_BENEFIT_METRICS, THS_CASH_METRICS


@pytest.mark.integration
def test_ths_debt_api_field_names():
    import akshare as ak
    df = ak.stock_financial_debt_new_ths(symbol="000001", indicator="按报告期")
    assert df is not None and not df.empty
    actual = set(df["metric_name"].unique())
    expected = set(THS_DEBT_METRICS)
    missing = expected - actual
    assert not missing, f"资产负债表 API 缺少预期指标: {missing}"


@pytest.mark.integration
def test_ths_benefit_api_field_names():
    import akshare as ak
    df = ak.stock_financial_benefit_new_ths(symbol="000001", indicator="按报告期")
    assert df is not None and not df.empty
    actual = set(df["metric_name"].unique())
    expected = set(THS_BENEFIT_METRICS)
    missing = expected - actual
    assert not missing, f"利润表 API 缺少预期指标: {missing}"


@pytest.mark.integration
def test_ths_cash_api_field_names():
    import akshare as ak
    df = ak.stock_financial_cash_new_ths(symbol="000001", indicator="按报告期")
    assert df is not None and not df.empty
    actual = set(df["metric_name"].unique())
    expected = set(THS_CASH_METRICS)
    missing = expected - actual
    assert not missing, f"现金流量表 API 缺少预期指标: {missing}"
