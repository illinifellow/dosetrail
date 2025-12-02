-- Patients are stored under a keyed hash of issuer + patient id: the registry can follow one
-- person across studies without holding their identifiers.
CREATE TABLE patients (
  id          bigserial PRIMARY KEY,