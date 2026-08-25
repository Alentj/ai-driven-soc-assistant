from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import SecurityAlert
from schemas import AlertCreate

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.post("/")
def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db)
):
    new_alert = SecurityAlert(
        rule_id=alert.rule_id,
        severity=alert.severity,
        agent_name=alert.agent_name,
        description=alert.description
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert


@router.get("/")
def get_alerts(db: Session = Depends(get_db)):
    return db.query(SecurityAlert).all()