from fastapi import APIRouter, HTTPException, Body
from models.prediction_payload import PredictionPayload
from models.prediction_output import PredictionOutput
from models.league_output import LeagueOutput
from typing_extensions import Annotated


from utils.logger import logger
from utils.get_match_id import get_match_id
from utils.harmonize_odds import harmonize_odds
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
                raw_odds = predict_match_odds(match["home_team"], match["away_team"])
                home, draw, away = harmonize_odds([raw_odds["outcome1"], raw_odds["outcomeX"], raw_odds["outcome2"]])
                over, under = harmonize_odds([raw_odds["outcomeOver"], raw_odds["outcomeUnder"]])
                gg, ng = harmonize_odds([raw_odds["outcomeGG"], raw_odds["outcomeNG"]])
                result.append({
                    "id": f"{match['home_team']}_{match['away_team']}_{match['timestamp']}",
                    "sport_key": "serie_a", #Hardcoded for Serie A
                    "matchId": get_match_id(match["home_team"], match["away_team"], match["timestamp"]),
                    "teams": [match["home_team"], match["away_team"]],
                    "start": match["timestamp"],
                    "odds": {
                        "home": home,
                        "away": away,
                        "draw": draw,
                        "over": over,
                        "under": under,
                        "gg": gg,
                        "ng": ng
                    }
                })
            except Exception as e:
                logger.error(f"Error predicting odds for match {match['home_team']} vs {match['away_team']}: {e}")


    except Exception as e:
        logger.error(f"Error occurred while getting odds: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong while getting odds")
    return LeagueOutput(events=result)
