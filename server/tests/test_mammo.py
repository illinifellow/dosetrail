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
        u,
        coded(("111027", "Breast Laterality"), breast),
        coded(("111031", "View Position"), view),
        num(("111637", "Average Glandular Dose"), dose),
        num(("111633", "Compressed Breast Thickness"), thickness),
    ])
    return ev


def report(*events):
    ds = Dataset()
    ds.StudyInstanceUID = "1.2.3"
    ds.ContentSequence = Sequence(list(events))
    return ds

