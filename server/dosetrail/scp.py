"""The DICOM side: a Storage SCP that modalities and the PACS send dose reports to.

pynetdicom is the reason this server is Python. It is the complete, maintained implementation of
the DICOM network protocol (association negotiation, presentation contexts, C-STORE, C-ECHO) — the
part that every scanner speaks and that nothing in the JavaScript ecosystem implements reliably.