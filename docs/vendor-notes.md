# Vendor dose report notes

DoseTrail reads DICOM Radiation Dose Structured Reports.

The standard fixes the concepts.

Vendors still differ in shape.

The parser reads by concept code.

The parser does not depend on item order.

The parser keeps working when optional sections are missing.

Siemens CT reports usually keep the CT acquisition container clear.
