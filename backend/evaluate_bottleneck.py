import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

from app.ml.bottleneck import (
    BottleneckPredictor,
    FEATURE_COLUMNS,
)


DATA_FILE = "data/bottleneck_dataset.csv"


df = pd.read_csv(DATA_FILE)


X = df[FEATURE_COLUMNS]

y = df["future_bottleneck"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)


train_df = X_train.copy()

train_df["future_bottleneck"] = y_train.values


test_df = X_test.copy()


model = BottleneckPredictor()

model.fit(train_df)


predictions = model.model.predict(X_test)

probabilities = model.model.predict_proba(X_test)[:, 1]


print("DIGITALTWIN.AI")

print("Bottleneck Model Evaluation")

print("=" * 50)


print(
    "\nAccuracy:",
    round(
        accuracy_score(
            y_test,
            predictions,
        ),
        4,
    ),
)


print(
    "ROC-AUC:",
    round(
        roc_auc_score(
            y_test,
            probabilities,
        ),
        4,
    ),
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        predictions,
    )
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
    )
)
