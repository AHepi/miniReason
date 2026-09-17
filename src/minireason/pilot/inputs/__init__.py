# Local bridge provenance: miniReason P-A2 integration; not copied from an upstream module.
# DeepReason reference: https://github.com/AHepi/DeepReason @ 9607fba6f0a3066fbcab282c9ae0fad823e52e0c; original path: none (local bridge); upstream license: MIT, Copyright (c) 2026 Aaron Hepi; see LICENSE.
"""P-A2 content-addressed inputs, ported from DeepReason and scoped for the pilot."""
from .service import TaskInputs, INPUT_REF_SCHEMA
from .preflight import InputError, preflight_prepared, preflight_for_endpoint
from .parse import AdmissionInput, admit_sources, PARSER_VERSION
