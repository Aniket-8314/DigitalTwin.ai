import pandas as pd

from app.ml.bottleneck import (
    BottleneckPredictor,
)


DATA_FILE = "data/bottleneck_dataset.csv"

MODEL_FILE = "data/bottleneck_model.joblib"


df = pd.read_csv(DATA_FILE)


print("DIGITALTWIN.AI")

print("Bottleneck Predictor Training")

print("=" * 50)

print("Records:", len(df))

print("\nLabel distribution:")

print(df["future_bottleneck"].value_counts())


model = BottleneckPredictor()

model.fit(df)

model.save(MODEL_FILE)


print("\nModel saved:", MODEL_FILE)
