import pandas as pd

import joblib
from pathlib import Path

from backend.auth import category_color, risk_category_from_score

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'balanced_best_diabetes_pipeline.pkl'


def predict_risk(glucose, blood_pressure, bmi, age, insulin):
    model = joblib.load(MODEL_PATH)
    df = pd.DataFrame(
        [[glucose, blood_pressure, bmi, age, insulin]],
        columns=['Glucose', 'BloodPressure', 'BMI', 'Age', 'Insulin'],
    )
    for col in ['Glucose', 'BloodPressure', 'BMI', 'Insulin']:
        if df[col].iloc[0] == 0:
            df.at[0, col] = float('nan')
    probability = float(model.predict_proba(df)[0, 1])
    score = probability * 100
    category = risk_category_from_score(score)
    return {
        'probability': probability,
        'score': score,
        'category': category,
        'category_color': category_color(category),
    }
