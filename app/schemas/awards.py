from pydantic import BaseModel

class AwardInterval(BaseModel):
    producer: str
    interval: int
    previousWin: int
    followingWin: int

class AwardsResponse(BaseModel):
    min: list[AwardInterval]
    max: list[AwardInterval]
    