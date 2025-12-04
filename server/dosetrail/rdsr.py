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