from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID
from ..core.db import get_db
from ..dependencies import require_organization_id, require_write_role
from ..models import ContactList
from ..schemas import ContactListCreate, ContactListRead

router = APIRouter(prefix="/v1/contact-lists", tags=["contact-lists"])

@router.get("", response_model=list[ContactListRead])
def list_contact_lists(
    organization_id: UUID = Depends(require_organization_id),
    db: Session = Depends(get_db),
):
    return db.scalars(select(ContactList).where(ContactList.organization_id == organization_id).order_by(ContactList.created_at.desc())).all()

@router.post("", response_model=ContactListRead, status_code=status.HTTP_201_CREATED)
def create_contact_list(
    payload: ContactListCreate,
    organization_id: UUID = Depends(require_organization_id),
    _role: str = Depends(require_write_role),
    db: Session = Depends(get_db),
):
    contact_list = ContactList(organization_id=organization_id, **payload.model_dump())
    db.add(contact_list)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="List name already exists in this workspace") from exc
    db.refresh(contact_list)
    return contact_list
