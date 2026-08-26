import pandas as pd

from app.ml.features import create_features
from app.ml.defect_labels import (
    create_defect_labels,
)


INPUT_FILE = "data/production_events.csv"

OUTPUT_FILE = "data/defect_dataset.csv"


df = pd.read_csv(INPUT_FILE)


features = create_features(df)


labeled = create_defect_labels(features)


labeled.to_csv(
    OUTPUT_FILE,
    index=False,
)


print("DIGITALTWIN.AI")

print("Defect Dataset")

print("=" * 50)

print("Records:", len(labeled))

print("\nDefect distribution:")

print(labeled["future_defect"].value_counts())

print("\nSaved:", OUTPUT_FILE)
