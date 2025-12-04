-- Patients are stored under a keyed hash of issuer + patient id: the registry can follow one
-- person across studies without holding their identifiers.
CREATE TABLE patients (
  id          bigserial PRIMARY KEY,
  key         text UNIQUE NOT NULL,
  sex         char(1),
  birth_year  smallint
);

CREATE TABLE studies (
  study_uid        text PRIMARY KEY,
  patient_id       bigint NOT NULL REFERENCES patients ON DELETE CASCADE,
  performed_at     timestamptz NOT NULL,
  modality         text NOT NULL,              -- CT, XA, RF, DX, MG
  device           text,                        -- manufacturer + model + station
  protocol         text,
  total_dlp        double precision,            -- mGy·cm, CT
  total_dap        double precision,            -- Gy·cm², projection
  fluoro_seconds   double precision,
  effective_msv    double precision,
  received_at      timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX studies_patient_time ON studies (patient_id, performed_at);
CREATE INDEX studies_protocol ON studies (modality, protocol);

CREATE TABLE events (
  id              bigserial PRIMARY KEY,