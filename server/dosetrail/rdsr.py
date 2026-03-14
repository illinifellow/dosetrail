"""Reads what matters out of a Radiation Dose Structured Report.

An RDSR is a tree of SR content items (TID 10001 for projection X-ray, TID 10011 for CT). We walk
it by concept codes rather than by position, because every vendor orders and nests the tree
differently; the codes are what the standard fixes.
"""

from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import datetime

from pydicom import Dataset

# (scheme, value) of the concepts we read
CT_ACQUISITION = ("DCM", "113819")
IRRADIATION_EVENT = ("DCM", "113706")
EVENT_UID = ("DCM", "113769")
ACQUISITION_TYPE = ("DCM", "113820")
TARGET_REGION = ("DCM", "123014")
MEAN_CTDIVOL = ("DCM", "113830")
DLP = ("DCM", "113838")
SCAN_LENGTH = ("DCM", "113825")
KVP = ("DCM", "113733")
DLP_TOTAL = ("DCM", "113813")
DAP = ("DCM", "122130")
DAP_TOTAL = ("DCM", "113722")
FLUORO_TIME_TOTAL = ("DCM", "113730")
PROTOCOL = ("DCM", "125203")

# CT DLP to effective dose, mSv per mGy·cm, adult (ICRP 102 / Shrimpton et al.)
K_FACTORS = {
    "head": 0.0021, "neck": 0.0059, "chest": 0.014, "abdomen": 0.015, "pelvis": 0.015,
    "abdomen and pelvis": 0.015, "chest, abdomen and pelvis": 0.015, "spine": 0.015,
}


@dataclass
class Event:
    uid: str
    kind: str
    anatomy: str | None = None
    ctdi_vol: float | None = None
    dlp: float | None = None
    scan_length_mm: float | None = None
    dap: float | None = None
    kvp: float | None = None


@dataclass
class DoseReport:
    study_uid: str
    patient_id: str
    issuer: str
    sex: str | None
    birth_year: int | None