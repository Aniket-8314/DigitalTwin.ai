import pandas as pd


WINDOW = 5


def create_features(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    # -----------------------------------------
    # Sort chronologically
    # -----------------------------------------

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = df.sort_values(
        [
            "station_id",
            "timestamp",
        ]
    ).reset_index(drop=True)

    # -----------------------------------------
    # Cycle-time features
    # -----------------------------------------

    grouped = df.groupby(
        "station_id",
        group_keys=False,
    )

    df["cycle_time_mean_5"] = grouped["cycle_time"].transform(
        lambda x: x.rolling(
            WINDOW,
            min_periods=1,
        ).mean()
    )

    df["cycle_time_std_5"] = (
        grouped["cycle_time"]
        .transform(
            lambda x: x.rolling(
                WINDOW,
                min_periods=1,
            ).std()
        )
        .fillna(0.0)
    )

    # -----------------------------------------
    # Cycle-time trend
    # -----------------------------------------

    df["cycle_time_delta"] = grouped["cycle_time"].diff().fillna(0.0)

    df["cycle_vs_takt"] = df["cycle_time"] / df["takt_time"]

    # -----------------------------------------
    # Temperature trend
    # -----------------------------------------

    df["temperature_delta"] = grouped["temperature"].diff().fillna(0.0)

    # -----------------------------------------
    # Vibration trend
    # -----------------------------------------

    df["vibration_delta"] = grouped["vibration"].diff().fillna(0.0)

    # -----------------------------------------
    # Torque deviation
    # -----------------------------------------

    df["torque_mean_5"] = grouped["torque"].transform(
        lambda x: x.rolling(
            WINDOW,
            min_periods=1,
        ).mean()
    )

    df["torque_deviation"] = df["torque"] - df["torque_mean_5"]

    # -----------------------------------------
    # Queue growth
    # -----------------------------------------

    df["queue_delta"] = grouped["queue_length"].diff().fillna(0.0)

    # -----------------------------------------
    # Health change
    # -----------------------------------------

    df["health_delta"] = grouped["health"].diff().fillna(0.0)

    return df
