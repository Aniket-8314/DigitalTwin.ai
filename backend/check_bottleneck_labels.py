import pandas as pd


df = pd.read_csv("data/bottleneck_dataset.csv")


columns = [
    "timestamp",
    "station_id",
    "cycle_time",
    "takt_time",
    "cycle_vs_takt",
    "queue_length",
    "queue_delta",
    "vibration",
    "torque",
    "future_bottleneck",
]


print(df[columns].tail(30).to_string(index=False))
