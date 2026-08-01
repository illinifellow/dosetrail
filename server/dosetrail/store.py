"""Writes a parsed report and its alerts in one transaction. Plain SQL through psycopg: the
queries are few, and the dashboard's percentile and window queries read better as SQL than as ORM."""

import hashlib
import hmac
import os

from psycopg import Connection

from .drl import Level, check
from .rdsr import DoseReport

SECRET = os.environ.get("DOSETRAIL_PSEUDONYM_KEY", "").encode()


def patient_key(issuer: str, patient_id: str) -> str:
    if not SECRET:
        raise RuntimeError("set DOSETRAIL_PSEUDONYM_KEY; patient ids are never stored in clear")
    return hmac.new(SECRET, f"{issuer}|{patient_id}".encode(), hashlib.sha256).hexdigest()


def save(conn: Connection, report: DoseReport, levels: list[Level]) -> list[tuple[str, str]]:
    with conn.transaction():
        patient = conn.execute(
            """INSERT INTO patients (key, sex, birth_year) VALUES (%s, %s, %s)
               ON CONFLICT (key) DO UPDATE SET sex = EXCLUDED.sex RETURNING id""",
            (patient_key(report.issuer, report.patient_id), report.sex, report.birth_year),
        ).fetchone()[0]
        conn.execute(
            """INSERT INTO studies (study_uid, patient_id, performed_at, modality, device, protocol,
                                    total_dlp, total_dap, fluoro_seconds, effective_msv)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (study_uid) DO UPDATE SET total_dlp = EXCLUDED.total_dlp, total_dap = EXCLUDED.total_dap,
                 fluoro_seconds = EXCLUDED.fluoro_seconds, effective_msv = EXCLUDED.effective_msv""",
            (report.study_uid, patient, report.performed_at, report.modality, report.device, report.protocol,