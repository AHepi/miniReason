# Local bridge provenance: miniReason P-A2 integration; not copied from an upstream module.
# DeepReason reference: https://github.com/AHepi/DeepReason @ 9607fba6f0a3066fbcab282c9ae0fad823e52e0c; original path: none (local bridge); upstream license: MIT, Copyright (c) 2026 Aaron Hepi; see LICENSE.
"""P-A2 text-only adapter boundary; no plugin discovery or execution."""
class AdapterError(ValueError):
    pass

def adapter_for(data: bytes, *, injected: tuple = ()):
    if injected:
        raise AdapterError("P-A2 does not authorize extraction plugins")
    return None

def run_adapter(manifest, data):
    raise AdapterError("P-A2 does not authorize extraction plugins")
