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
    performed_at: datetime
    modality: str
    device: str
    protocol: str | None
    total_dlp: float | None = None
    total_dap: float | None = None
    fluoro_seconds: float | None = None
    events: list[Event] = field(default_factory=list)

    @property
    def effective_msv(self) -> float | None:
        """Effective dose from DLP per event and anatomy; None for projection imaging, where DAP
        conversion depends on geometry the report does not carry reliably."""
        if self.modality != "CT" or not self.events:
            return None
        total = 0.0
        for e in self.events:
            k = K_FACTORS.get((e.anatomy or "").lower())
            if k is None or e.dlp is None:
                return None
            total += e.dlp * k
        return round(total, 2)


def _code(item: Dataset) -> tuple[str, str] | None:
    seq = item.get("ConceptNameCodeSequence")
    return (seq[0].CodingSchemeDesignator, seq[0].CodeValue) if seq else None


def _walk(items) -> Iterator[Dataset]:
    for item in items or []:
        yield item
        yield from _walk(item.get("ContentSequence"))


def _num(item: Dataset) -> float | None:
    mv = item.get("MeasuredValueSequence")
    return float(mv[0].NumericValue) if mv else None


def _text(item: Dataset) -> str | None:
    if "ConceptCodeSequence" in item:
        return str(item.ConceptCodeSequence[0].CodeMeaning)
    if "TextValue" in item:
        return str(item.TextValue)
    if "UID" in item:
        return str(item.UID)