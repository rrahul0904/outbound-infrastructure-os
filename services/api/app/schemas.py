from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from .models import DomainStatus

class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=180)
    slug: str = Field(min_length=2, max_length=100, pattern=r"^[a-zA-Z0-9-]+$")

class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    slug: str
    created_at: datetime

class DomainCreate(BaseModel):
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

class ContactCreate(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    first_name: str | None = Field(default=None, max_length=120)
    last_name: str | None = Field(default=None, max_length=120)
    company: str | None = Field(default=None, max_length=180)

class ContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    organization_id: UUID
    email: str
    first_name: str | None
    last_name: str | None
    company: str | None
    verification_status: str
    suppressed: bool
    suppression_reason: str | None
    created_at: datetime

class ContactListCreate(BaseModel):
    name: str = Field(min_length=2, max_length=180)
    description: str | None = Field(default=None, max_length=500)
    source: str = Field(default="manual", max_length=64)

class ContactListRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    organization_id: UUID
    name: str
    description: str | None
    source: str
    created_at: datetime

class CampaignCreate(BaseModel):
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

class CampaignStepCreate(BaseModel):
    position: int = Field(ge=1, le=30)
    delay_hours: int = Field(default=0, ge=0, le=24 * 60)
    subject_template: str = Field(min_length=1, max_length=500)
    body_template: str = Field(min_length=1, max_length=20000)
    format: str = Field(default="plain_text", pattern=r"^(plain_text|rich_text|html)$")

class CampaignStepRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    campaign_id: UUID
    position: int
    delay_hours: int
    subject_template: str
    body_template: str
    format: str
    created_at: datetime

class DashboardSummary(BaseModel):
    domains: int
    ready_domains: int
    contacts: int
    contact_lists: int
    campaigns: int
