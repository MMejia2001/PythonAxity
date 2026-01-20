import joblib
import pandas as pd


def predict_one(
    model_path: str, age: float, income: float, city: str, visited_pages: int
) -> dict:
    clf = joblib.load(model_path)

    X_new = pd.DataFrame(
        [
            {
                "age": age,
                "income": income,
                "city": city,
                "visited_pages": visited_pages,
            }
        ]
    )

    proba = clf.predict_proba(X_new)[0][1]  # probabilidad de "bought=1"
    pred = int(proba >= 0.5)

    return {"prediction": pred, "probability": round(float(proba), 4)}


def main() -> None:
    result = predict_one(
        "models/buy_classifier.joblib",
        age=30,
        income=20000,
        city="CDMX",
        visited_pages=7,
    )
    print(result)


if __name__ == "__main__":
    main()
