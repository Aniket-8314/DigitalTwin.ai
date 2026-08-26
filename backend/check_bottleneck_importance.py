import pandas as pd

from app.ml.bottleneck import (
    BottleneckPredictor,
    FEATURE_COLUMNS,
)


MODEL_FILE = "data/bottleneck_model.joblib"


model = BottleneckPredictor()

model.load(MODEL_FILE)


importance = pd.DataFrame(
    {
        "feature": FEATURE_COLUMNS,
        "importance": model.model.feature_importances_,
    }
)


importance = importance.sort_values(
    "importance",
    ascending=False,
)


print("Bottleneck Feature Importance")

print("=" * 50)

print(importance.to_string(index=False))
