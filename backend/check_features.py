import pandas as pd


df = pd.read_csv("data/features.csv")


s14 = df[df["station_id"] == "S14"]


columns = [
    "timestamp",
    "cycle_time",
    "cycle_time_mean_5",
    "cycle_time_delta",
    "cycle_vs_takt",
    "temperature",
    "temperature_delta",
    "vibration",
    "vibration_delta",
    "torque",
    "torque_deviation",
    "queue_length",
    "queue_delta",
    "health",
    "health_delta",
]


print(s14[columns].tail(20).to_string(index=False))
