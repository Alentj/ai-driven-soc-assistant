from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, SecurityAlert
from schemas import AlertCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Driven SOC Assistant API",
    version="0.3.0"
)


@app.get("/")
def root():
    return {
        "message": "AI-Driven SOC Assistant Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/alerts")
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


@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(SecurityAlert).all()

    return alerts