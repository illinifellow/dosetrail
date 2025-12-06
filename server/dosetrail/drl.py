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