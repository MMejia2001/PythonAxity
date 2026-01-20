from infer import predict_one


def test_predict_one_returns_expected_shape():
    result = predict_one(
        "models/buy_classifier.joblib",
        age=30,
        income=20000,
        city="CDMX",
        visited_pages=7,
    )

    assert "prediction" in result
    assert "probability" in result
    assert result["prediction"] in (0, 1)
    assert 0.0 <= result["probability"] <= 1.0
