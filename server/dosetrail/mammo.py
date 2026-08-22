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