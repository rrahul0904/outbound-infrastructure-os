# Security, Compliance and Abuse Controls

This product must not rely on users behaving perfectly. Enforcement belongs in platform policy.

## Mandatory controls

- verified domain ownership before infrastructure changes;
- organization-level sending suspension and emergency stop;
- unsubscribe headers and one-click unsubscribe where applicable;
- global and workspace suppression lists;
- complaint ingestion and immediate suppression;
- hard-bounce suppression;
- velocity/rate controls per workspace/domain/mailbox/IP;
- suspicious signup/payment/activity review hooks;
- auditable admin actions;
- retention controls for message bodies and reply content;
- export/delete workflows supporting privacy obligations;
- clear acceptable-use policy and abuse reporting.

## Design rule

No campaign API may bypass suppression, health, complaint or ownership checks. The scheduler consumes policy-approved capacity rather than deciding policy itself.
