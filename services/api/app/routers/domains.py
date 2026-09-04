from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..models import SendingDomain
from ..schemas import DomainCreate, DomainRead

router = APIRouter(prefix="/v1/domains", tags=["domains"])

@router.get("", response_model=list[DomainRead])
def list_domains(db: Session = Depends(get_db)):
    return db.scalars(select(SendingDomain).order_by(SendingDomain.created_at.desc())).all()

@router.post("", response_model=DomainRead, status_code=status.HTTP_201_CREATED)
def create_domain(payload: DomainCreate, db: Session = Depends(get_db)):
    domain = SendingDomain(organization_id=payload.organization_id, domain=payload.domain.lower())
    db.add(domain)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Domain is already registered in this workspace") from exc
    db.refresh(domain)
    return domain
