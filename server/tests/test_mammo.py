from pydicom import Dataset
from pydicom.sequence import Sequence

from dosetrail.mammo import parse


def code(value, meaning, scheme="DCM"):
    c = Dataset()
    c.CodeValue, c.CodingSchemeDesignator, c.CodeMeaning = value, scheme, meaning
    return Sequence([c])


def coded(concept, value, meaning=None):
    item = Dataset()
    item.ValueType = "CODE"