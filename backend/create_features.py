import pandas as pd

from app.ml.features import create_features


INPUT_FILE = "data/production_events.csv"

OUTPUT_FILE = "data/features.csv"


df = pd.read_csv(INPUT_FILE)


print(
    "Original shape:",
    df.shape,
)


features = create_features(df)


features.to_csv(
    OUTPUT_FILE,
    index=False,
)


print("Feature dataset created:")

print(
    "Shape:",
    features.shape,
)

print(
    "Saved to:",
    OUTPUT_FILE,
)

print("\nFeatures:")

for column in features.columns:

    print(
        " -",
        column,
    )
