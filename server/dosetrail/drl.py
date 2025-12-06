"""Diagnostic reference levels and the checks run on every new study.

DRLs are national and change every few years, so they live in `drl.yaml`, which each site edits.
A DRL is not a dose limit: exceeding it means "look at why", which is exactly what an alert asks.
"""

from dataclasses import dataclass