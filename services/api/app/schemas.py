from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from .models import DomainStatus

class DomainCreate(BaseModel):
    organization_id: UUID
    domain: str = Field(min_length=3, max_length=253, pattern=r"^[A-Za-z0-9.-]+$")

class DomainRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    organization_id: UUID
    domain: str
    status: DomainStatus
    health_score: int
    safe_daily_capacity: int
    sending_enabled: bool
    created_at: datetime

class CampaignCreate(BaseModel):
    organization_id: UUID
    name: str = Field(min_length=2, max_length=180)
    policy_mode: str = Field(default="balanced", pattern=r"^(balanced|sequential|follow_up_priority)$")
    daily_limit: int = Field(default=0, ge=0, le=1000000)

class CampaignRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    organization_id: UUID
    name: str
    status: str
    policy_mode: str
    daily_limit: int
    created_at: datetime
