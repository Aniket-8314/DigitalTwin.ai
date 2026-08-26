import csv
from collections import Counter


FILE_PATH = "data/production_events.csv"


with open(
    FILE_PATH,
    "r",
    encoding="utf-8",
) as file:

    rows = list(csv.DictReader(file))


print("DIGITALTWIN.AI DATASET")
print("=" * 40)

print(
    "Total records:",
    len(rows),
)

print(
    "Unique vehicles:",
    len(set(row["vehicle_id"] for row in rows)),
)

print(
    "Unique stations:",
    len(set(row["station_id"] for row in rows)),
)

print(
    "Columns:",
    len(rows[0]),
)


print("\nStation distribution:")

counts = Counter(row["station_id"] for row in rows)

for station, count in sorted(counts.items()):

    print(
        station,
        "→",
        count,
    )


print("\nSensor availability:")

sensor_counts = Counter(row["sensor_available"] for row in rows)

for value, count in sensor_counts.items():

    print(
        value,
        "→",
        count,
    )
