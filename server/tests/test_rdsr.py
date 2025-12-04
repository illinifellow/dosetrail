from pydicom import Dataset
from pydicom.sequence import Sequence

from dosetrail.drl import Level, check
from dosetrail.rdsr import parse


def code(value, meaning, scheme="DCM"):
    c = Dataset()
    c.CodeValue, c.CodingSchemeDesignator, c.CodeMeaning = value, scheme, meaning
    return Sequence([c])


def num(concept, value):
    item = Dataset()
    item.ValueType = "NUM"
    item.ConceptNameCodeSequence = code(*concept)
    mv = Dataset()
    mv.NumericValue = str(value)
    item.MeasuredValueSequence = Sequence([mv])
    return item


def ct_event(uid, anatomy, ctdi, dlp):
    ev = Dataset()
    ev.ConceptNameCodeSequence = code("113819", "CT Acquisition")
    u = Dataset()
    u.ConceptNameCodeSequence = code("113769", "Irradiation Event UID")
    u.UID = uid
    region = Dataset()