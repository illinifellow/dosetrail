# dosetrail

A radiation dose registry for a radiology department, fed straight by the scanners.

CT scanners, angiography suites and DR rooms already write a **Radiation Dose Structured Report** (RDSR) after every exam. Most departments send it to the PACS and never read it. dosetrail is a DICOM node you add as one more destination: it reads each report, keeps the dose per exam and per irradiation event, follows each patient's cumulative dose under a pseudonym, and flags what a medical physicist should look at.

![the dose atlas](docs/atlas.png)

## What it flags

- **Above a diagnostic reference level** — CTDIvol or DLP for CT, DAP for fluoroscopy, against the levels in `drl.yaml`. A DRL is not a limit; the alert asks for a reason, which is recorded when the alert is closed.
- **Cumulative dose** — 100 mSv effective dose within five years for one patient.
- **Repeat scans** — the same protocol on the same patient within 24 hours.

Alerts can be posted to a webhook (Teams, Slack, a ticketing system) as they happen.

## What it shows

- DLP distribution per CT protocol as box plots, with the DRL drawn across. Protocols whose median sits near the line are the first place to optimise.
- The same protocol on different scanners, side by side.
- A pseudonymous patient's history with the running five-year effective dose.

## Setup

```sh
docker compose up -d
# on the scanner or the PACS: add a DICOM destination
#   AE title DOSETRAIL, host <this machine>, port 11112, send SR dose reports only
cd web && npm install && npm run dev
```

Test with dcmtk: `storescu localhost 11112 -aec DOSETRAIL rdsr.dcm`.

## Privacy

Patient ids are replaced by an HMAC of issuer and id with a key only the server holds (`DOSETRAIL_PSEUDONYM_KEY`). Names and birth dates are not stored; the birth year and sex are, because dose risk depends on them.

## How it reads a report

An RDSR is a tree of SR content items (TID 10011 for CT, TID 10001 for projection X-ray). Vendors nest and order it differently, so `rdsr.py` walks the whole tree and reads concepts by their DCM codes — Mean CTDIvol 113830, DLP 113838, DAP 122130 and so on — never by position. Effective dose for CT is estimated from DLP per event with the ICRP 102 conversion factors for the scanned region; where the region is not recognised, dosetrail stores no effective dose rather than a guessed one.

## Layout

```
server/dosetrail/scp.py    DICOM Storage SCP (pynetdicom)
server/dosetrail/rdsr.py   RDSR parsing
server/dosetrail/drl.py    reference levels and checks
server/dosetrail/store.py  one transaction per report
server/dosetrail/api.py    FastAPI for the dashboard
server/sql/                schema
web/                       React, Mantine, ECharts
deploy/helm/               chart for a hospital Kubernetes
```


## Credits

- [pynetdicom](https://github.com/pydicom/pynetdicom) and [pydicom](https://github.com/pydicom/pydicom) — the whole DICOM side stands on them.