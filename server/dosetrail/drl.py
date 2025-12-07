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


def check(report: DoseReport, levels: list[Level], cumulative_msv: float, repeat_within_hours: bool) -> list[tuple[str, str]]:
    """Returns (kind, detail) for every reason this study deserves a second look."""
    alerts: list[tuple[str, str]] = []
    lv = level_for(report, levels)
    if lv:
        if lv.dlp and report.total_dlp and report.total_dlp > lv.dlp:
            alerts.append(("above_drl", f"DLP {report.total_dlp:.0f} mGy·cm above the {lv.name} DRL of {lv.dlp:.0f}"))
        worst = max((e.ctdi_vol or 0 for e in report.events), default=0)
        if lv.ctdi_vol and worst > lv.ctdi_vol:
            alerts.append(("above_drl", f"CTDIvol {worst:.1f} mGy above the {lv.name} DRL of {lv.ctdi_vol:.1f}"))
        if lv.dap and report.total_dap and report.total_dap > lv.dap:
            alerts.append(("above_drl", f"DAP {report.total_dap:.1f} Gy·cm² above the {lv.name} DRL of {lv.dap:.1f}"))