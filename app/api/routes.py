from fastapi import APIRouter, Depends
from app.schemas.awards import AwardsResponse
from sqlalchemy.orm import Session
from app.services.awards_service import get_awards_intervals
from app.db.session import get_db

router = APIRouter(tags=["Awards"])

@router.get("/producers/awards-intervals", response_model=AwardsResponse)
def get_producer_award_intervals(db: Session = Depends(get_db)):    
    return get_awards_intervals(db)
