import pandas as pd

from app.ml.defect import (
    DefectPredictor,
)


DATA_FILE = "data/defect_dataset.csv"

MODEL_FILE = "data/defect_model.joblib"


df = pd.read_csv(DATA_FILE)


print("DIGITALTWIN.AI")

print("Defect Predictor Training")

print("=" * 50)

print("Records:", len(df))

print("\nClass distribution:")

print(df["future_defect"].value_counts())


model = DefectPredictor()

model.fit(df)

model.save(MODEL_FILE)


print("\nModel saved:", MODEL_FILE)
