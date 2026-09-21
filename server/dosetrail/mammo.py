"""Mammography dose extraction from projection X-ray RDSR."""

from collections.abc import Iterator
from dataclasses import dataclass, field

from pydicom import Dataset


@dataclass
class MammoView:
    uid: str
    breast: str
    view: str
    average_glandular_dose_mgy: float | None = None
    compressed_breast_thickness_mm: float | None = None


@dataclass
class MammoDoseReport:
    study_uid: str
    views: list[MammoView] = field(default_factory=list)

    @property
    def totals_by_breast(self) -> dict[str, float]:
        totals: dict[str, float] = {}
        for view in self.views:
            if view.average_glandular_dose_mgy is None:
                continue
            totals[view.breast] = round(totals.get(view.breast, 0.0) + view.average_glandular_dose_mgy, 3)
        return totals


def _code(item: Dataset) -> tuple[str, str, str] | None:
    seq = item.get("ConceptNameCodeSequence")
    if not seq:
        return None
    code = seq[0]
    return str(code.CodingSchemeDesignator), str(code.CodeValue), str(code.CodeMeaning).lower()


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
    return None


def _matches(item: Dataset, *needles: str) -> bool:
    code = _code(item)
    if not code:
        return False
    haystack = " ".join(code).lower()
    return any(needle in haystack for needle in needles)


def _breast(text: str | None) -> str:
    value = (text or "unknown").lower()
    if "left" in value or value == "l":
        return "left"
    if "right" in value or value == "r":
        return "right"
    return "unknown"


def _view(text: str | None) -> str:
    value = (text or "unknown").upper().replace(" ", "")
    if "MLO" in value:
        return "MLO"
    if "CC" in value:
        return "CC"
    return text or "unknown"


def _event(container: Dataset) -> MammoView:
    view = MammoView(uid="", breast="unknown", view="unknown")
    for item in _walk(container.get("ContentSequence")):
        if _matches(item, "irradiation event uid"):
            view.uid = _text(item) or ""
        elif _matches(item, "laterality", "breast laterality"):
            view.breast = _breast(_text(item))
        elif _matches(item, "view position", "projection"):
            view.view = _view(_text(item))
        elif _matches(item, "average glandular dose", "mean glandular dose"):
            view.average_glandular_dose_mgy = _num(item)
        elif _matches(item, "compressed breast thickness", "compression thickness"):
            view.compressed_breast_thickness_mm = _num(item)
    return view


def parse(ds: Dataset) -> MammoDoseReport:
    report = MammoDoseReport(study_uid=str(ds.StudyInstanceUID))
    for item in _walk(ds.ContentSequence):
        if _matches(item, "irradiation event x-ray data", "projection x-ray radiation dose"):
            event = _event(item)
            if event.average_glandular_dose_mgy is not None or event.compressed_breast_thickness_mm is not None: