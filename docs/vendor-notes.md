# Vendor dose report notes

DoseTrail reads DICOM Radiation Dose Structured Reports.

The standard fixes the concepts.

Vendors still differ in shape.

The parser reads by concept code.

The parser does not depend on item order.

The parser keeps working when optional sections are missing.

Siemens CT reports usually keep the CT acquisition container clear.

CTDIvol and DLP sit inside the acquisition event.

Target region is often present.

Protocol name is usually near the top.

Total DLP is often present.

Scan length is often present.

Series descriptions can be more useful than protocol names.

Siemens reports may include localizer events.

Localizers stay as events.

Localizers should not drive protocol DRL matching.

Device identity comes from manufacturer, model and station.

GE CT reports are often flatter.

GE can repeat concept names in different containers.

The parser keeps the nearest event container.

GE may omit target region.

When target region is missing, protocol text is the fallback.

GE protocol names can include scanner abbreviations.

The DRL matcher must normalise those names.

GE sometimes reports total DLP only.

If events lack DLP, event-level alerting skips them.

Study-level totals are still stored.

GE can put acquisition type in a coded item.

The parser reads CodeMeaning and TextValue.

Philips CT reports often carry rich protocol text.

Philips may group events under irradiation event containers.

The parser descends recursively.

Philips reports may include phantom type.

Phantom type is useful for QA.

Phantom type is not patient dose.

Philips can include planned but unexposed series.

Only events with dose values count.

Philips can report DLP as decimal strings.

Numeric parsing must accept strings.

Philips device names may include software version.

Charts should group by scanner identity.

Canon CT reports can be sparse.

Canon may put protocol names in study description.

Canon events can have acquisition UID but no scan length.

Scan length is optional.

Canon may report total DLP with no per-event DLP.

The store allows study totals without event totals.

Canon target region text may differ from the DRL vocabulary.

The normaliser maps common region variants.

Projection X-ray reports use a separate path.

Fluoro and XA use DAP more than DLP.

Effective dose from DAP depends on geometry.

DoseTrail stores DAP and avoids a fake effective dose.

Mammography reports are projection X-ray reports.

Mammography uses average glandular dose.

Average glandular dose is per view.

Compressed breast thickness is per view.

Totals are per breast.

Per-breast totals must not mix with CT DLP.

All vendors can omit patient issuer.

Patient pseudonymisation must handle an empty issuer.

All vendors can send repeated studies.

Study UID is the idempotency key.

Events use event UID when present.

When event UID is absent, event order is a weak fallback.

Units must be checked at the measured value.

Do not assume every NUM in an event is mGy.

Do not assume every total belongs to CT.

Reject reports without ContentSequence.

Store raw manufacturer and model strings.

Normalise for grouping later.
