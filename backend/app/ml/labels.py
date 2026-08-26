import pandas as pd


def create_bottleneck_labels(
    df: pd.DataFrame,
    horizon: int = 5,
) -> pd.DataFrame:

    df = df.copy()

    df = df.sort_values(
        [
            "station_id",
            "timestamp",
        ]
    ).reset_index(drop=True)

    grouped = df.groupby(
        "station_id",
        group_keys=False,
    )

    future_cycle = grouped["cycle_time"].shift(-horizon)

    future_takt = grouped["takt_time"].shift(-horizon)

    df["future_bottleneck"] = (future_cycle > future_takt).astype(int)

    return df
