from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID
from ..core.db import get_db
from ..dependencies import require_organization_id, require_write_role
from ..models import SendingDomain
from ..schemas import DomainCreate, DomainRead

router = APIRouter(prefix="/v1/domains", tags=["domains"])

@router.get("", response_model=list[DomainRead])
def list_domains(organization_id: UUID = Depends(require_organization_id), db: Session = Depends(get_db)):
    return db.scalars(select(SendingDomain).where(SendingDomain.organization_id == organization_id).order_by(SendingDomain.created_at.desc())).all()

@router.post("", response_model=DomainRead, status_code=status.HTTP_201_CREATED)
def create_domain(
    payload: DomainCreate,
    organization_id: UUID = Depends(require_organization_id),
    _role: str = Depends(require_write_role),
    db: Session = Depends(get_db),
):
    domain = SendingDomain(organization_id=organization_id, domain=payload.domain.lower().strip())
    db.add(domain)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Domain is already registered in this workspace") from exc
    db.refresh(domain)
    return domain
