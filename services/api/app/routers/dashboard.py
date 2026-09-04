from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from uuid import UUID
from ..core.db import get_db
from ..dependencies import require_organization_id
from ..models import Campaign, Contact, ContactList, SendingDomain
from ..schemas import DashboardSummary

router = APIRouter(prefix="/v1/dashboard", tags=["dashboard"])

@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(
    organization_id: UUID = Depends(require_organization_id),
    db: Session = Depends(get_db),
):
    def count(model):
        return db.scalar(select(func.count()).select_from(model).where(model.organization_id == organization_id)) or 0
    ready_domains = db.scalar(select(func.count()).select_from(SendingDomain).where(SendingDomain.organization_id == organization_id, SendingDomain.status == "ready")) or 0
    return DashboardSummary(
        domains=count(SendingDomain),
        ready_domains=ready_domains,
        contacts=count(Contact),
        contact_lists=count(ContactList),
        campaigns=count(Campaign),
    )
