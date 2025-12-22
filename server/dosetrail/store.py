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