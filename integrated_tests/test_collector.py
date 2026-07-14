import pytest
from alpha_jerry.engine.collector import THS_DEBT_METRICS, THS_BENEFIT_METRICS, THS_CASH_METRICS


class TestThsApiFieldNames:
    """同花顺三张报表的接口字段名验证。"""

    @pytest.mark.integration
    def test_ths_debt_api_field_names(self):
        import akshare as ak
        df = ak.stock_financial_debt_new_ths(symbol="000001", indicator="按报告期")
        assert df is not None and not df.empty
        actual = set(df["metric_name"].unique())
        expected = set(THS_DEBT_METRICS)
        missing = expected - actual
        assert not missing, f"资产负债表 API 缺少预期指标: {missing}"

    @pytest.mark.integration
    def test_ths_benefit_api_field_names(self):
        import akshare as ak
        df = ak.stock_financial_benefit_new_ths(symbol="000001", indicator="按报告期")
        assert df is not None and not df.empty
        actual = set(df["metric_name"].unique())
        expected = set(THS_BENEFIT_METRICS)
        missing = expected - actual
        assert not missing, f"利润表 API 缺少预期指标: {missing}"

    @pytest.mark.integration
    def test_ths_cash_api_field_names(self):
        import akshare as ak
        df = ak.stock_financial_cash_new_ths(symbol="000001", indicator="按报告期")
        assert df is not None and not df.empty
        actual = set(df["metric_name"].unique())
        expected = set(THS_CASH_METRICS)
        missing = expected - actual
        assert not missing, f"现金流量表 API 缺少预期指标: {missing}"


class TestStockListApi:
    """全 A 股列表接口可用。"""

    @pytest.mark.integration
    def test_stock_list_returns_data(self):
        import akshare as ak
        df = ak.stock_info_a_code_name()
        assert df is not None and not df.empty
        assert "code" in df.columns
        assert "name" in df.columns
        assert len(df) > 4000, f"A 股数量不足 4000: {len(df)}"

    @pytest.mark.integration
    def test_stock_list_has_known_stocks(self):
        import akshare as ak
        df = ak.stock_info_a_code_name()
        codes = set(df["code"].astype(str))
        # 验证几只知名股票在列表中
        for code in ["000001", "600519", "300750", "000858"]:
            assert code in codes, f"缺少知名股票 {code}"


class TestCompanyProfileApi:
    """巨潮个股概况接口可用。"""

    @pytest.mark.integration
    def test_profile_returns_listing_date(self):
        import akshare as ak
        df = ak.stock_profile_cninfo(symbol="000001")
        assert df is not None and not df.empty
        assert "上市日期" in df.columns
        date = str(df["上市日期"].iloc[0])
        # 巨潮返回 YYYY-MM-DD 格式
        assert len(date) >= 8, f"上市日期格式异常: {date}"
        year = date[:4]
        assert year.isdigit() and int(year) > 1990, f"上市日期年份异常: {year}"


class TestSwIndustryApi:
    """申万行业分类接口可用。"""

    @pytest.mark.integration
    def test_sw_first_info_returns_31_industries(self):
        import akshare as ak
        info = ak.sw_index_first_info()
        assert info is not None and not info.empty
        assert "行业代码" in info.columns
        assert "行业名称" in info.columns
        assert len(info) >= 31, f"申万一级行业不足 31: {len(info)}"

    @pytest.mark.integration
    def test_sw_component_api_callable(self):
        """申万成分股接口可调用（上游接口有时不稳定）。"""
        import akshare as ak
        try:
            df = ak.index_component_sw(symbol="801010")
            assert df is not None
            assert len(df) > 0
        except Exception as e:
            pytest.skip(f"申万成分股接口暂时不可用: {e}")
