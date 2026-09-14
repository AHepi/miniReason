"""Build F002's participant material from F001's, by adding nothing but a study id.

F001's own material is the owner's H005 material verbatim plus one key,
``study_id``.  F002's is F001's material with that one key's VALUE changed and
nothing else: same schema, same system text, same three instructions, same
problems, same templates, same ``source_pins``.  The runner refuses a material
whose ``study_id`` is neither null nor the study directory's own name
(``STUDY_ID_MISMATCH``), which is the only reason a separate file exists at all.

Run with --check to verify the staged file still is what this script builds.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

F001_MATERIAL_SHA256 = '8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff'
H005_MATERIAL_SHA256 = '24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927'
STUDY_ID = 'F002-fork5-raised-clock'


def build(f001_material: Path, h005_material: Path) -> bytes:
    raw = f001_material.read_bytes()
    if hashlib.sha256(raw).hexdigest() != F001_MATERIAL_SHA256:
        raise SystemExit('F001 material is not the published bytes')
    owner = h005_material.read_bytes()
    if hashlib.sha256(owner).hexdigest() != H005_MATERIAL_SHA256:
        raise SystemExit('H005 material is not the published bytes')
    document = json.loads(raw)
    if {k: v for k, v in document.items() if k != 'study_id'} != json.loads(owner):
        raise SystemExit('F001 material differs from H005 by more than study_id')
    document['study_id'] = STUDY_ID
    # The published F001 file's own encoding: sorted keys, two-space indent,
    # non-ASCII left as itself, one trailing newline.
    return (json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--f001', type=Path, required=True)
    parser.add_argument('--h005', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    built = build(args.f001, args.h005)
    if args.check:
        if args.out.read_bytes() != built:
            print('DIFFERS')
            return 1
        print('MATCHES sha256=%s' % hashlib.sha256(built).hexdigest())
        return 0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(built)
    print('wrote %s sha256=%s' % (args.out, hashlib.sha256(built).hexdigest()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
