# dosetrail

A radiation dose registry for a radiology department, fed straight by the scanners.

CT scanners, angiography suites and DR rooms already write a **Radiation Dose Structured Report** (RDSR) after every exam. Most departments send it to the PACS and never read it. dosetrail is a DICOM node you add as one more destination: it reads each report, keeps the dose per exam and per irradiation event, follows each patient's cumulative dose under a pseudonym, and flags what a medical physicist should look at.

![the dose atlas](docs/atlas.png)

## What it flags
