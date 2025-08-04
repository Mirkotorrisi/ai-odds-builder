from pydantic import BaseModel, Field
from typing import List

class Odds(BaseModel):
    home: float = Field(..., description="Odds for home team to win")
    away: float = Field(..., description="Odds for away team to win")
    draw: float = Field(..., description="Odds for a draw")
    over: float = Field(..., description="Odds for over")
    under: float = Field(..., description="Odds for under")
    gg: float = Field(..., description="Odds for both teams to score")
    ng: float = Field(..., description="Odds for not both teams to score")


class Event(BaseModel):
    id: str = Field(..., description="Unique identifier for the event")
    sport_key: str = Field(..., description="Key identifying the sport/league")
    matchId: str = Field(..., description="Unique identifier for the match")
    teams: List[str] = Field(..., description="List of teams participating in the event")
    start: str = Field(..., description="Start time of the event in ISO format")
    odds: Odds = Field(..., description="Predicted odds for various outcomes")

class LeagueOutput(BaseModel):
    '''Represents the predicted outcomes. For an array of events in a league.'''
    events: List[Event] = Field(..., description="Array of events with their predicted odds")
