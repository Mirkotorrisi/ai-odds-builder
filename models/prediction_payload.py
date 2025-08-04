from pydantic import BaseModel, Field

class PredictionPayload(BaseModel):
    '''
    Represents the input payload for odds prediction.
    '''
    model_config = { "extra": "forbid" }
    homeName: str = Field(default=None, strip_whitespace=True, min_length=1)
    awayName: str = Field(default=None, strip_whitespace=True, min_length=1)