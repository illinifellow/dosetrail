"""The DICOM side: a Storage SCP that modalities and the PACS send dose reports to.

pynetdicom is the reason this server is Python. It is the complete, maintained implementation of
the DICOM network protocol (association negotiation, presentation contexts, C-STORE, C-ECHO) — the
part that every scanner speaks and that nothing in the JavaScript ecosystem implements reliably.
"""

import argparse
import logging
import os
from pathlib import Path

import httpx
from psycopg_pool import ConnectionPool
from pynetdicom import AE, evt
from pynetdicom.sop_class import (
    Verification,
    XRayRadiationDoseSRStorage,
    EnhancedXRayRadiationDoseSRStorage,
    PatientRadiationDoseSRStorage,
)

from . import drl
from .rdsr import parse
from .store import save

log = logging.getLogger("dosetrail.scp")
DOSE_CLASSES = [XRayRadiationDoseSRStorage, EnhancedXRayRadiationDoseSRStorage, PatientRadiationDoseSRStorage]


def handler(pool: ConnectionPool, levels: list[drl.Level], webhook: str | None):
    def on_store(event: evt.Event) -> int:
        ds = event.dataset