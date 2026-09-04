from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..models import Organization
from ..schemas import OrganizationCreate, OrganizationRead

router = APIRouter(prefix="/v1/organizations", tags=["organizations"])

@router.post("", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
def create_organization(payload: OrganizationCreate, db: Session = Depends(get_db)):
    organization = Organization(name=payload.name.strip(), slug=payload.slug.lower().strip())
    db.add(organization)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Workspace slug already exists") from exc
    db.refresh(organization)
    return organization

@router.get("/{organization_id}", response_model=OrganizationRead)
def get_organization(organization_id, db: Session = Depends(get_db)):
    organization = db.scalar(select(Organization).where(Organization.id == organization_id))
    if not organization:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return organization
