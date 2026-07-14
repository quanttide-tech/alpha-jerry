import pandas as pd
from pathlib import Path
from datetime import datetime


def today_str():
    return datetime.now().strftime("%y%m%d")


def read_xlsx(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")
    return pd.read_excel(path, dtype={"股票代码": str})


def write_xlsx(df: pd.DataFrame, path: Path, metadata: dict | None = None):
    """写入 xlsx，可选写入第二个 sheet 作为数据来源说明。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="数据", index=False)
        if metadata:
            meta_df = pd.DataFrame([
                {"字段": k, "数据来源": v} for k, v in metadata.items()
            ])
            meta_df.to_excel(writer, sheet_name="数据来源", index=False)


def winsorize(series: pd.Series, lower: float = -5, upper: float = 5) -> pd.Series:
    return series.clip(lower, upper)
