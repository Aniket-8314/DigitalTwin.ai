import pandas as pd

from app.ml.features import create_features
from app.ml.labels import create_bottleneck_labels


INPUT_FILE = "data/production_events.csv"

OUTPUT_FILE = "data/bottleneck_dataset.csv"


df = pd.read_csv(INPUT_FILE)

features = create_features(df)

labeled = create_bottleneck_labels(
    features,
    horizon=5,
)

# Remove rows where there isn't enough
# future data to create a label.

labeled = labeled.dropna(subset=["future_bottleneck"])

labeled.to_csv(
    OUTPUT_FILE,
    index=False,
)

print("Bottleneck dataset created")

print("Shape:", labeled.shape)

print("\nLabel distribution:")

print(labeled["future_bottleneck"].value_counts())
