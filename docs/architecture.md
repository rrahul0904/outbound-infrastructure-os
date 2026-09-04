# Technical Architecture

## 1. Objective

Build a multi-tenant outbound infrastructure control plane that manages compliant sending domains, sender capacity, contacts, campaigns, delivery events, replies and reputation without coupling the product to one cloud or one mail provider.

## 2. Architecture boundaries

```text
Customer / Operator
       |
       v
+--------------------+
| Next.js Web Console|
+---------+----------+
          |
          v
+--------------------+       +----------------------+
| FastAPI Control API|------>| PostgreSQL Control DB|
+---------+----------+       +----------------------+
          |
          +---------------> Redis / durable task queue
                              |
                              v
                    +----------------------+
                    | Async Worker Services|
                    +----+-----+-----+-----+
                         |     |     |
                   DNS adapter |  reputation/verification adapters
                               |
                         mail transport adapter
                               |
                               v
                      Delivery / Reply Events
                               |
                               v
                    Event ingestion + policy engine
```

## 3. Control plane vs event plane

**PostgreSQL control plane** stores organizations, users, configuration, domains, campaign definitions, policy, suppression, audit and current operational state.

**Event plane** starts in PostgreSQL for MVP but is intentionally isolated behind event APIs. At high scale it can move to ClickHouse/Kafka/S3-compatible object storage without changing the control-plane contracts.

## 4. Domain lifecycle state machine

```text
PENDING_NS -> PROVISIONING -> DNS_VALIDATION -> WARMING -> READY
                                     |             |        |
                                     v             v        v
                                  DEGRADED <---- health policy
                                     |
                    +----------------+----------------+
                    v                                 v
                BLACKLISTED                         PAUSED
                    |                                 |
                    +---------------+-----------------+
                                    v
                                 DISABLED
```

Transitions are server-enforced and audited. Campaign code cannot force a domain to READY.

## 5. Sending policy engine

Every candidate send must pass:

1. organization/account state;
2. contact suppression and unsubscribe checks;
3. contact verification/risk policy;
4. campaign schedule/window;
5. domain/mailbox readiness;
6. domain/mailbox/IP capacity;
7. bounce/complaint/reputation thresholds;
8. per-recipient contact frequency rules;
9. provider-specific rate limits;
10. global abuse and emergency-stop controls.

The scheduler allocates only approved capacity. Health changes can revoke capacity and cause queued recipients to be rebalanced.

## 6. Service evolution

MVP starts as a modular monolith plus workers. Split only when scale/ownership warrants it:

- identity/workspace service
- domain/DNS service
- contacts/verification service
- campaigns/scheduler service
- delivery event ingestion service
- reply/inbox service
- reputation/policy service
- notification service
- billing/usage service

## 7. Portability

The application contract is Docker-first. Production may run on:

- Kubernetes (EKS/AKS/GKE/OpenShift/on-prem),
- generic VM/VPC deployments,
- managed container platforms,
- local Docker Compose for development/demo.

PostgreSQL, Redis, S3-compatible object storage, secrets, DNS and mail transport are accessed behind standard interfaces/adapters.

## 8. Security

- tenant ID enforced server-side on every data access path;
- secrets never sent to the browser;
- envelope encryption for provider credentials;
- hashed suppression identifiers where raw addresses are unnecessary;
- immutable audit records for privileged actions;
- per-workspace and global kill switches;
- idempotency keys on externally triggered mutations/events;
- webhook signatures and replay protection;
- least-privilege service identities;
- configurable retention for message content and delivery metadata.

## 9. Scale targets

Initial target: tens of thousands of organizations, millions of contacts, millions of events/day.

Scale path:

- horizontally scale API/worker pods;
- partition or offload delivery telemetry;
- Redis-backed distributed scheduling/locks;
- append-only event stream for high-volume delivery data;
- object storage for imports/exports and large payloads;
- materialized analytics views / ClickHouse for interactive telemetry;
- provider/domain/IP sharding at the worker/data-plane level.
