CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS organizations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name varchar(180) NOT NULL,
  slug varchar(100) NOT NULL UNIQUE,
  created_at timestamptz NOT NULL DEFAULT now()
);

DO $$ BEGIN
  CREATE TYPE domain_status AS ENUM ('pending_ns','provisioning','dns_validation','warming','ready','degraded','blacklisted','paused','disabled');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

CREATE TABLE IF NOT EXISTS organization_members (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  subject_id varchar(180) NOT NULL,
  email varchar(320),
  role varchar(32) NOT NULL DEFAULT 'member',
  status varchar(32) NOT NULL DEFAULT 'active',
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (organization_id, subject_id)
);
CREATE INDEX IF NOT EXISTS ix_org_members_org_role ON organization_members(organization_id, role);

CREATE TABLE IF NOT EXISTS sending_domains (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  domain varchar(253) NOT NULL,
  status domain_status NOT NULL DEFAULT 'pending_ns',
  health_score integer NOT NULL DEFAULT 0 CHECK (health_score BETWEEN 0 AND 100),
  safe_daily_capacity integer NOT NULL DEFAULT 0 CHECK (safe_daily_capacity >= 0),
  sending_enabled boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (organization_id, domain)
);
CREATE INDEX IF NOT EXISTS ix_sending_domains_org_status ON sending_domains(organization_id, status);

CREATE TABLE IF NOT EXISTS contacts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  email varchar(320) NOT NULL,
  first_name varchar(120),
  last_name varchar(120),
  company varchar(180),
  verification_status varchar(32) NOT NULL DEFAULT 'pending',
  suppressed boolean NOT NULL DEFAULT false,
  suppression_reason varchar(80),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (organization_id, email)
);
CREATE INDEX IF NOT EXISTS ix_contacts_org_verification ON contacts(organization_id, verification_status);

CREATE TABLE IF NOT EXISTS contact_lists (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  name varchar(180) NOT NULL,
  description varchar(500),
  source varchar(64) NOT NULL DEFAULT 'manual',
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (organization_id, name)
);

CREATE TABLE IF NOT EXISTS contact_list_memberships (
  list_id uuid NOT NULL REFERENCES contact_lists(id) ON DELETE CASCADE,
  contact_id uuid NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  added_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (list_id, contact_id)
);

CREATE TABLE IF NOT EXISTS campaigns (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  name varchar(180) NOT NULL,
  status varchar(32) NOT NULL DEFAULT 'draft',
  policy_mode varchar(32) NOT NULL DEFAULT 'balanced',
  daily_limit integer NOT NULL DEFAULT 0 CHECK (daily_limit >= 0),
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_campaigns_org_status ON campaigns(organization_id, status);

CREATE TABLE IF NOT EXISTS campaign_steps (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id uuid NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
  position integer NOT NULL CHECK (position > 0),
  delay_hours integer NOT NULL DEFAULT 0 CHECK (delay_hours >= 0),
  subject_template varchar(500) NOT NULL,
  body_template text NOT NULL,
  format varchar(32) NOT NULL DEFAULT 'plain_text',
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (campaign_id, position)
);

CREATE TABLE IF NOT EXISTS suppression_entries (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  email_hash varchar(128) NOT NULL,
  reason varchar(64) NOT NULL,
  source varchar(64) NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (organization_id, email_hash)
);

CREATE TABLE IF NOT EXISTS domain_health_snapshots (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  domain_id uuid NOT NULL REFERENCES sending_domains(id) ON DELETE CASCADE,
  health_score integer NOT NULL CHECK (health_score BETWEEN 0 AND 100),
  bounce_rate numeric(8,5) NOT NULL DEFAULT 0,
  complaint_rate numeric(8,5) NOT NULL DEFAULT 0,
  blacklist_hits integer NOT NULL DEFAULT 0,
  recorded_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_domain_health_domain_recorded ON domain_health_snapshots(domain_id, recorded_at DESC);

CREATE TABLE IF NOT EXISTS delivery_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  campaign_id uuid REFERENCES campaigns(id) ON DELETE SET NULL,
  event_type varchar(48) NOT NULL,
  provider_message_id varchar(255),
  recipient_hash varchar(128),
  metadata_json text,
  occurred_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_delivery_events_org_time ON delivery_events(organization_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS ix_delivery_events_campaign_type ON delivery_events(campaign_id, event_type);

CREATE TABLE IF NOT EXISTS audit_logs (
  id bigserial PRIMARY KEY,
  organization_id uuid REFERENCES organizations(id) ON DELETE SET NULL,
  actor_id varchar(128),
  action varchar(128) NOT NULL,
  entity_type varchar(64),
  entity_id varchar(128),
  metadata_json text,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_audit_logs_org_time ON audit_logs(organization_id, created_at DESC);
