from pydantic import BaseModel, Field

class PredictionOutput(BaseModel):
    '''Represents the predicted outcomes.'''
    outcome1: float = Field(..., description="Predicted odds for outcome 1")
    outcomeX: float = Field(..., description="Predicted odds for outcome X")
    outcome2: float = Field(..., description="Predicted odds for outcome 2")
    outcomeOver: float = Field(..., description="Predicted odds for over")
    outcomeUnder: float = Field(..., description="Predicted odds for under")
    outcomeGG: float = Field(..., description="Predicted odds for both teams to score")
    outcomeNG: float = Field(..., description="Predicted odds for not both teams to score")
