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