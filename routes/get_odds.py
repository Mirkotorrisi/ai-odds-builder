from fastapi import APIRouter, HTTPException, Body
from models.prediction_payload import PredictionPayload
from models.prediction_output import PredictionOutput
from models.league_output import LeagueOutput
from typing_extensions import Annotated


from utils.logger import logger
from utils.get_match_id import get_match_id
from services.fetch_matches import fetch_matches
from services.predict_odds import predict_match_odds

router = APIRouter()

@router.post("/odds/match", response_model=PredictionOutput)
def get_match_odds(body: Annotated[PredictionPayload, Body()]) -> PredictionOutput:
    logger.info(f"Received POST on /odds endpoint, homeName: {body.homeName}, awayName: {body.awayName}")
    try:
        res = predict_match_odds(body.homeName, body.awayName)

    except Exception as e:
        logger.error(f"Error occurred while getting odds: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong while getting odds")
    return res

@router.get("/odds", response_model=LeagueOutput)
def get_all_odds() -> LeagueOutput:
    logger.info(f"Received GET on /odds endpoint")
    try:
        # Fetching the serie A fixtures and standings
        matches = fetch_matches()
        if not matches:
            raise HTTPException(status_code=404, detail="No matches found")
        result = []
        for match in matches:
            try:
                odds = predict_match_odds(match["home_team"], match["away_team"])
                result.append({
                    "id": f"{match['home_team']}_{match['away_team']}_{match['timestamp']}",
                    "sport_key": "serie_a", #Hardcoded for Serie A
                    "matchId": get_match_id(match["home_team"], match["away_team"], match["timestamp"]),
                    "teams": [match["home_team"], match["away_team"]],
                    "start": match["timestamp"],
                    "odds": {
                        "home": round(float(odds["outcome1"]), 2),
                        "away": round(float(odds["outcome2"]), 2),
                        "draw": round(float(odds["outcomeX"]), 2),
                        "over": round(float(odds["outcomeOver"]), 2),
                        "under": round(float(odds["outcomeUnder"]), 2),
                        "gg": round(float(odds["outcomeGG"]), 2),
                        "ng": round(float(odds["outcomeNG"]), 2)
                    }
                })
            except Exception as e:
                logger.error(f"Error predicting odds for match {match['home_team']} vs {match['away_team']}: {e}")


    except Exception as e:
        logger.error(f"Error occurred while getting odds: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong while getting odds")
    return LeagueOutput(events=result)
