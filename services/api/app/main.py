from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .routers import campaigns, contacts, dashboard, domains, health, lists, organizations

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.2.0", docs_url="/docs" if settings.app_env != "production" else None)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(health.router)
app.include_router(organizations.router)
app.include_router(dashboard.router)
app.include_router(domains.router)
app.include_router(contacts.router)
app.include_router(lists.router)
app.include_router(campaigns.router)
