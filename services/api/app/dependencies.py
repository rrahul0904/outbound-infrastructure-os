from uuid import UUID
from fastapi import Depends, Header, HTTPException, status

_ALLOWED_ROLES = {"owner", "admin", "member", "viewer"}
_WRITE_ROLES = {"owner", "admin", "member"}


def require_organization_id(x_organization_id: str = Header(..., alias="X-Organization-ID")) -> UUID:
    try:
        return UUID(x_organization_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid X-Organization-ID header") from exc


def require_actor_role(x_actor_role: str = Header("member", alias="X-Actor-Role")) -> str:
    role = x_actor_role.lower().strip()
    if role not in _ALLOWED_ROLES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid X-Actor-Role header")
    return role


def require_write_role(role: str = Depends(require_actor_role)) -> str:
    if role not in _WRITE_ROLES:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Workspace role is read-only")
    return role
