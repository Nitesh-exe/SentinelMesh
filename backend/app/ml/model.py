from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier


class IntrusionModel:
    def __init__(self) -> None:
        self.model = RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced",
        )

    def fit(self, x: list[list[float]], y: list[str]) -> None:
        self.model.fit(x, y)

    def predict(self, x: list[list[float]]) -> tuple[str, float]:
        prediction = str(self.model.predict(x)[0])
        probabilities = self.model.predict_proba(x)[0]

        confidence = float(max(probabilities))

        return prediction, confidence

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, path)

    def load(self, path: Path) -> None:
        self.model = joblib.load(path)