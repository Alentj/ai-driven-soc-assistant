from pydantic import BaseModel


class AlertCreate(BaseModel):
    rule_id: str | None = None
    severity: int | None = None
    agent_name: str | None = None
    description: str | None = None