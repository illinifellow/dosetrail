"""Mammography dose extraction from projection X-ray RDSR."""

from collections.abc import Iterator
from dataclasses import dataclass, field

from pydicom import Dataset


@dataclass
class MammoView:
    uid: str
    breast: str
    view: str