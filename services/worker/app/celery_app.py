import os
from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("outbound-worker", broker=redis_url, backend=redis_url, include=["app.tasks"])
celery_app.conf.update(task_serializer="json", result_serializer="json", accept_content=["json"], task_acks_late=True, worker_prefetch_multiplier=1, timezone="UTC")
