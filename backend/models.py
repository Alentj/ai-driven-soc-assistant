from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from database import Base


class SecurityAlert(Base):
    __tablename__ = "security_alerts"

    id = Column(Integer, primary_key=True, index=True)

    rule_id = Column(String, nullable=True)
    severity = Column(Integer, nullable=True)
    agent_name = Column(String, nullable=True)
    description = Column(String, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )