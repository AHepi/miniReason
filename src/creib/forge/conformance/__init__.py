"""Compatibility support retained for Mini; the outer conformance runner is absent.

Imports stay narrow so importing Mini does not initialize an unrelated harness.
The legacy namespace preserves source identities and existing kernel references.
"""
from .executor import response_from_content
