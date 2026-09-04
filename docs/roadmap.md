# End-to-End Implementation Roadmap

## Phase 0 — Foundation (current)
- monorepo, Docker, CI
- Next.js console shell
- FastAPI control plane
- PostgreSQL schema
- Redis/Celery worker boundary
- domain/campaign API primitives
- architecture/security contracts

## Phase 1 — Product core
- authentication + organizations + RBAC
- workspace onboarding
- domain registry/detail screens
- contacts, lists, CSV import, custom fields
- verification abstraction and results
- campaigns/sequences/schedules
- centralized audit log
- subscription/usage data model
- operator/admin console

## Phase 2 — Domain automation
- DNS provider interface
- nameserver ownership proof
- subdomain strategy
- SPF/DKIM/DMARC/MX generation and verification
- DKIM key lifecycle
- DNS drift detection
- readiness state machine and UI timeline

## Phase 3 — Sending and event ingestion
- provider-agnostic transport contract
- queue-backed scheduler
- sender/domain capacity allocation
- idempotent send attempts
- delivery/bounce/complaint webhook ingestion
- suppression and retry semantics
- reply ingestion/threading
- master inbox

## Phase 4 — Reputation intelligence
- warmup program model
- domain/mailbox/IP health scoring
- blacklist adapter framework
- automated throttle/pause/rebalance
- incident history and remediation workflows
- certification tests for policy decisions

## Phase 5 — AI intelligence
- reply classification
- human-approved response suggestions
- content linting/risk checks
- campaign recommendations
- infrastructure anomaly summarization
- bounded, evidence-backed optimization agents

## Phase 6 — Enterprise/platform
- public REST API, API keys and webhooks
- MCP server and workflow integrations
- CRM/connectors
- SSO/SAML, SCIM, advanced RBAC
- data retention/legal hold controls
- Kubernetes manifests/Helm
- multi-region and disaster recovery
- cost/usage observability
