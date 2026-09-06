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