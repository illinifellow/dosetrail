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
    item.ConceptNameCodeSequence = code(*concept)
    item.ConceptCodeSequence = code(value, meaning or value, "SRT")
    return item


def num(concept, value):
    item = Dataset()
    item.ValueType = "NUM"
    item.ConceptNameCodeSequence = code(*concept)
    mv = Dataset()
    mv.NumericValue = str(value)
    item.MeasuredValueSequence = Sequence([mv])
    return item


def event(uid, breast, view, dose, thickness):
    ev = Dataset()
    ev.ConceptNameCodeSequence = code("113706", "Irradiation Event X-Ray Data")
    u = Dataset()
    u.ConceptNameCodeSequence = code("113769", "Irradiation Event UID")
    u.UID = uid
    ev.ContentSequence = Sequence([