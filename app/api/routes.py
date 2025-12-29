from fastapi import APIRouter
from app.schemas.awards import AwardsResponse
from app.services.awards_service import build_awards

router = APIRouter(tags=["Awards"])

@router.get("/producers/awards-intervals", response_model=AwardsResponse)
def get_producer_award_intervals():    
    return build_awards()
