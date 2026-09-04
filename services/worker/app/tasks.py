from .celery_app import celery_app

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5})
def verify_domain_dns(self, domain_id: str) -> dict[str, str]:
    # Adapter implementation arrives in Phase 2. The task boundary is established now
    # so DNS work is never performed inside an HTTP request lifecycle.
    return {"domain_id": domain_id, "status": "queued_for_adapter"}

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5})
def recalculate_domain_health(self, domain_id: str) -> dict[str, str]:
    return {"domain_id": domain_id, "status": "health_recalculation_scheduled"}

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def ingest_delivery_event(self, event: dict) -> dict[str, str]:
    return {"event_type": str(event.get("event_type", "unknown")), "status": "accepted"}
