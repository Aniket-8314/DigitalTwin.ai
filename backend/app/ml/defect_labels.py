import pandas as pd


def create_defect_labels(
    df: pd.DataFrame,
    threshold: float = 0.70,
) -> pd.DataFrame:

    df = df.copy()

    df["future_defect"] = (df["quality_score"] < threshold).astype(int)

    return df
