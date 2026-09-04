from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID
from ..core.db import get_db
from ..dependencies import require_organization_id, require_write_role
from ..models import Contact
from ..schemas import ContactCreate, ContactRead

router = APIRouter(prefix="/v1/contacts", tags=["contacts"])

@router.get("", response_model=list[ContactRead])
def list_contacts(
    q: str | None = Query(default=None, max_length=160),
    limit: int = Query(default=100, ge=1, le=500),
    organization_id: UUID = Depends(require_organization_id),
    db: Session = Depends(get_db),
):
    query = select(Contact).where(Contact.organization_id == organization_id)
    if q:
        query = query.where(Contact.email.ilike(f"%{q.strip()}%"))
    return db.scalars(query.order_by(Contact.created_at.desc()).limit(limit)).all()

@router.post("", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
def create_contact(
    payload: ContactCreate,
    organization_id: UUID = Depends(require_organization_id),
    _role: str = Depends(require_write_role),
    db: Session = Depends(get_db),
):
    contact = Contact(organization_id=organization_id, **payload.model_dump())
    contact.email = contact.email.lower().strip()
    db.add(contact)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Contact already exists in this workspace") from exc
    db.refresh(contact)
    return contact
