"""Reads what matters out of a Radiation Dose Structured Report.

An RDSR is a tree of SR content items (TID 10001 for projection X-ray, TID 10011 for CT). We walk
it by concept codes rather than by position, because every vendor orders and nests the tree
differently; the codes are what the standard fixes.
"""
