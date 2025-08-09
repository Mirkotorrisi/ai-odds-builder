import joblib
import numpy as np
from models.prediction_output import PredictionOutput
from tensorflow.keras.models import load_model

MARKET_MODELS = ("market_1X2", "market_OU", "market_BTTS")

model_paths = [f"assets/{market}_model.keras" for market in MARKET_MODELS]
scaler_paths = [f"assets/{market}_scaler.joblib" for market in MARKET_MODELS]

TEAM_MAP_PATH = "assets/team_id_map.joblib"

TARGET_COLS = [
    ["outcome1", "outcomeX", "outcome2"],
    ["outcomeOver", "outcomeUnder"],
    ["outcomeGG", "outcomeNG"]
]

models = []
scalers = []
for model_path, scaler_path in zip(model_paths, scaler_paths):
    model = load_model(model_path)
    scaler = joblib.load(scaler_path)
    models.append(model)
    scalers.append(scaler)

team_map = joblib.load(TEAM_MAP_PATH)

def predict_match_odds(home_name: str, away_name: str) -> PredictionOutput:
    """
    It returns the predicted odds for a match between home_name and away_name.
    """
    # Optional cleaning
    home_name = home_name.strip().title()
    away_name = away_name.strip().title()

    # Check team existence
    if home_name not in team_map:
        raise ValueError(f"Home team not found in training: '{home_name}'")
    if away_name not in team_map:
        raise ValueError(f"Away team not found in training: '{away_name}'")

    # Convert to numeric IDs
    home_id = np.array([[team_map[home_name]]])
    away_id = np.array([[team_map[away_name]]])

    # Prediction
    results = {}
    for model, scaler, target_cols in zip(models, scalers, TARGET_COLS):
        # Predict and inverse transform
        pred_scaled = model.predict([home_id, away_id], verbose=0)
        pred = scaler.inverse_transform(pred_scaled)[0]

        # Round the predictions
        pred = np.round(pred, 2)

        # Merge this market's predictions into the results dict
        results.update(dict(zip(target_cols, pred)))

    # Create and return a single PredictionOutput with all markets
    return results

