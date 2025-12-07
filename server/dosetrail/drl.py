"""Diagnostic reference levels and the checks run on every new study.

DRLs are national and change every few years, so they live in `drl.yaml`, which each site edits.
A DRL is not a dose limit: exceeding it means "look at why", which is exactly what an alert asks.
"""

from dataclasses import dataclass
from pathlib import Path

import yaml

from .rdsr import DoseReport


@dataclass(frozen=True)
class Level:
    name: str
    match: tuple[str, ...]
    ctdi_vol: float | None = None
    dlp: float | None = None
    dap: float | None = None


def load(path: Path) -> list[Level]:
    raw = yaml.safe_load(path.read_text())
    return [
        Level(name=d["name"], match=tuple(m.lower() for m in d["match"]), ctdi_vol=d.get("ctdi_vol"), dlp=d.get("dlp"), dap=d.get("dap"))
        for d in raw["levels"]
    ]


def level_for(report: DoseReport, levels: list[Level]) -> Level | None:
    text = f"{report.protocol or ''} {' '.join(e.anatomy or '' for e in report.events)}".lower()
    return next((lv for lv in levels if any(m in text for m in lv.match)), None)

