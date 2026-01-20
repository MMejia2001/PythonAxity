import os

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def main() -> None:
    df = pd.read_csv("data/customers.csv")

    # 1) Limpieza mínima
    # - separa X (features) y y (target)
    X = df.drop(columns=["bought"])
    y = df["bought"].astype(int)

    # columnas numéricas y categóricas
    num_cols = ["age", "income", "visited_pages"]
    cat_cols = ["city"]

    # 2) Preprocesamiento
    # - numéricas: rellenar missing con mediana
    # - categóricas: rellenar missing con "Unknown" y one-hot
    numeric = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric, num_cols),
            ("cat", categorical, cat_cols),
        ]
    )

    # 3) Modelo simple
    model = LogisticRegression(max_iter=500)

    clf = Pipeline(
        steps=[
            ("prep", preprocessor),
            ("model", model),
        ]
    )

    # 4) Train/test split (solo para tener una validación rápida)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    clf.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)

    print(f"Accuracy (test): {acc:.3f}")

    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, "models/buy_classifier.joblib")
    print("Modelo guardado en models/buy_classifier.joblib")


if __name__ == "__main__":
    main()
