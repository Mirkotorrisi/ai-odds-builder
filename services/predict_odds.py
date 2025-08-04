import joblib
import numpy as np
from models.prediction_output import PredictionOutput
from tensorflow.keras.models import load_model


MODEL_PATH = "assets/odds_embed_model.keras"
SCALER_PATH = "assets/odds_scaler.joblib"
TEAM_MAP_PATH = "assets/team_id_map.joblib"

TARGET_COLS = [
    "outcome1", "outcomeX", "outcome2",
    "outcomeOver", "outcomeUnder",
    "outcomeGG", "outcomeNG"
]

model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
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
    pred_scaled = model.predict([home_id, away_id], verbose=0)
    pred = scaler.inverse_transform(pred_scaled)[0]

    # Return as dictionary
    return dict(zip(TARGET_COLS, map(lambda x: round(x, 2), pred)))
