from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID
from ..core.db import get_db
from ..dependencies import require_organization_id, require_write_role
from ..models import Campaign, CampaignStep
from ..schemas import CampaignCreate, CampaignRead, CampaignStepCreate, CampaignStepRead

router = APIRouter(prefix="/v1/campaigns", tags=["campaigns"])

@router.get("", response_model=list[CampaignRead])
def list_campaigns(organization_id: UUID = Depends(require_organization_id), db: Session = Depends(get_db)):
    return db.scalars(select(Campaign).where(Campaign.organization_id == organization_id).order_by(Campaign.created_at.desc())).all()

@router.post("", response_model=CampaignRead, status_code=status.HTTP_201_CREATED)
def create_campaign(
    payload: CampaignCreate,
    organization_id: UUID = Depends(require_organization_id),
    _role: str = Depends(require_write_role),
    db: Session = Depends(get_db),
):
    campaign = Campaign(organization_id=organization_id, **payload.model_dump())
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

@router.get("/{campaign_id}/steps", response_model=list[CampaignStepRead])
def list_campaign_steps(
    campaign_id: UUID,
    organization_id: UUID = Depends(require_organization_id),
    db: Session = Depends(get_db),
):
    campaign = db.scalar(select(Campaign).where(Campaign.id == campaign_id, Campaign.organization_id == organization_id))
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db.scalars(select(CampaignStep).where(CampaignStep.campaign_id == campaign_id).order_by(CampaignStep.position)).all()

@router.post("/{campaign_id}/steps", response_model=CampaignStepRead, status_code=status.HTTP_201_CREATED)
def create_campaign_step(
    campaign_id: UUID,
    payload: CampaignStepCreate,
    organization_id: UUID = Depends(require_organization_id),
    _role: str = Depends(require_write_role),
    db: Session = Depends(get_db),
):
    campaign = db.scalar(select(Campaign).where(Campaign.id == campaign_id, Campaign.organization_id == organization_id))
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    step = CampaignStep(campaign_id=campaign_id, **payload.model_dump())
    db.add(step)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Campaign step position already exists") from exc
    db.refresh(step)
    return step
