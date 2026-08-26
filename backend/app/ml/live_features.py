import pandas as pd

from app.ml.history import (
    FeatureHistory,
    StationObservation,
)


def build_live_features(
    history: FeatureHistory,
    station_id: str,
    takt_time: float,
    sensor_available: bool,
) -> pd.DataFrame:

    observations = history.get(station_id)

    if not observations:
        return pd.DataFrame()

    rows = []

    for observation in observations:

        rows.append(
            {
                "cycle_time": observation.cycle_time,
                "temperature": observation.temperature,
                "vibration": observation.vibration,
                "torque": observation.torque,
                "queue_length": observation.queue_length,
                "health": observation.health,
                "takt_time": takt_time,
            }
        )

    df = pd.DataFrame(rows)

    # -------------------------------------
    # Rolling cycle features
    # -------------------------------------

    df["cycle_time_mean_5"] = df["cycle_time"].rolling(5, min_periods=1).mean()

    df["cycle_time_std_5"] = (
        df["cycle_time"].rolling(5, min_periods=1).std().fillna(0.0)
    )

    df["cycle_time_delta"] = df["cycle_time"].diff().fillna(0.0)

    df["cycle_vs_takt"] = df["cycle_time"] / df["takt_time"]

    # -------------------------------------
    # Temperature
    # -------------------------------------

    df["temperature_delta"] = df["temperature"].diff().fillna(0.0)

    # -------------------------------------
    # Vibration
    # -------------------------------------

    df["vibration_delta"] = df["vibration"].diff().fillna(0.0)

    # -------------------------------------
    # Torque
    # -------------------------------------

    df["torque_mean_5"] = df["torque"].rolling(5, min_periods=1).mean()

    df["torque_deviation"] = df["torque"] - df["torque_mean_5"]

    # -------------------------------------
    # Queue
    # -------------------------------------

    df["queue_delta"] = df["queue_length"].diff().fillna(0.0)

    # -------------------------------------
    # Health
    # -------------------------------------

    df["health_delta"] = df["health"].diff().fillna(0.0)

    df["sensor_available"] = sensor_available

    return df
