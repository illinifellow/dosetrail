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
    region.ConceptNameCodeSequence = code("123014", "Target Region")
    region.ConceptCodeSequence = code("T-D1100", anatomy, "SRT")
    ev.ContentSequence = Sequence([u, region, num(("113830", "Mean CTDIvol"), ctdi), num(("113838", "DLP"), dlp)])
    return ev


def report(*events):
    ds = Dataset()
    ds.StudyInstanceUID, ds.PatientID, ds.StudyDate, ds.StudyTime = "1.2.3", "P1", "20260314", "101500"