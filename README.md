# Outbound Infrastructure OS

A production-oriented control plane for compliant outbound email infrastructure: domain onboarding, DNS automation, sender health, contact verification, campaign orchestration, reply intelligence, reputation monitoring, and policy-driven sending.

> Status: Phase 0/1 foundation. The repo contains the web console, API service, worker service, PostgreSQL schema, Redis/Celery queue foundation, Docker Compose environment, CI, architecture documentation, and the first operator dashboard.

## Product principles

- **Infrastructure-first:** sending health and policy enforcement are first-class product capabilities.
- **Compliance by design:** suppression, unsubscribe, complaint, abuse and audit controls are built into the data model.
- **Portable:** Docker-first and designed to run on local Docker, Kubernetes, or major clouds/VPCs.
- **Control plane / data plane separation:** application state is separate from high-volume delivery telemetry.
- **No provider lock-in:** DNS, verification, mail transport, object storage and LLM integrations are adapter based.

## Repository layout

```text
apps/web/          Next.js operator/customer console
services/api/      FastAPI control-plane API
services/worker/   Celery async jobs and scheduled health tasks
infra/             local infrastructure and database bootstrap
docs/              architecture, roadmap, security and operating model
.github/workflows/ CI checks
```

## Local development

1. Copy `.env.example` to `.env`.
2. Run `docker compose up --build` on a machine with Docker.
3. Open `http://localhost:3000` for the web console.
4. Open `http://localhost:8000/docs` for the API docs.

The API defaults to PostgreSQL in Docker. The web console uses `NEXT_PUBLIC_API_URL` and can render its operational demo state even before backend services are connected.

## Phase roadmap

- Phase 1: organizations, auth, domains, contacts, campaigns, dashboard, audit trail.
- Phase 2: authoritative DNS adapter, SPF/DKIM/DMARC automation, domain verification state machine.
- Phase 3: mail transport adapters, queue-backed scheduling, bounce/reply processing, rate and capacity enforcement.
- Phase 4: warmup/reputation engine, blacklist monitoring, automated throttling and remediation.
- Phase 5: AI reply classification, content assistance, infrastructure recommendations, campaign optimization.
- Phase 6: integrations, public API, webhooks, MCP, enterprise controls, Kubernetes/cloud deployment packs.

See `docs/architecture.md` and `docs/roadmap.md` for the implementation contract.
