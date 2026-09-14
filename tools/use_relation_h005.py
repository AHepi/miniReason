"""Write the use-relation table for one H005 occurrence. Offline; no provider.

Reads only the occurrence directory and writes only a NEW output directory
(``USE_TABLE.md`` and ``use_table.json``). The occurrence is custody-checked
first, with the importer's own ``verify_custody``; on failure nothing is
written and the exit code is 2. No credential is read, no network call is
made, no graph is built, no adjudicator is called, and every interpretive cell
in the output is left empty for root.

Exit codes (the table is repeated in docs/workflows/use-relation-h005.md):

    0  the table was written.
    2  CUSTODY_REFUSED - the occurrence failed a custody check (including a
       missing or malformed occurrence file); nothing was written.
    3  BUILD_FAILED - the occurrence is well-custodied but the table could not
       be built. EMPTY_SCOPE (the occurrence holds no coordinate at all) is one
       of these.
    4  OUT_DIR_REFUSED - the destination is inside the occurrence, or already
       exists, or could not be written (an OSError: permissions, ENOSPC). The
       occurrence is fine; name a different directory. Nothing under the
       occurrence is ever written, and a failed write leaves no partial
       output directory behind.
    5  SELECTOR_MATCHED_NOTHING - the occurrence holds coordinates but
       --problem/--arm/--cycle matched none of them; stderr lists what the
       occurrence actually holds.

argparse keeps its own usage-error behaviour and this tool does not remap it.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

REPOSITORY = Path(__file__).resolve().parents[1]
if str(REPOSITORY / "src") not in sys.path:
    sys.path.insert(0, str(REPOSITORY / "src"))

from minireason.use_relation_h005 import (  # noqa: E402
    USE_RELATION_BANNER,
    CustodyError,
    MappingError,
    OutDirRefused,
    SelectorMatchedNothing,
    build_use_table,
    write_use_table,
)

EXIT_OK = 0
EXIT_CUSTODY = 2
EXIT_BUILD = 3
EXIT_OUT_DIR = 4
EXIT_SELECTOR = 5


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("occurrence", type=Path, help="H005 occurrence directory (read-only)")
    parser.add_argument("out_dir", type=Path, help="new output directory; must not exist")
    parser.add_argument("--problem", action="append", default=None,
                        help="restrict to this problem id (repeatable)")
    parser.add_argument("--arm", action="append", default=None,
                        help="restrict to this arm (repeatable)")
    parser.add_argument("--cycle", action="append", type=int, default=None,
                        help="restrict to this cycle (repeatable)")
    args = parser.parse_args(argv)

    # The destination is checked before the occurrence is opened, so an
    # operator who names a refused directory is told that and not made to wait
    # for a full custody pass first. Both refusals are checked here and again
    # in write_use_table, which is the library-level guarantee.
    try:
        occurrence_root = args.occurrence.resolve()
        destination = args.out_dir.resolve()
    except OSError as exc:
        print("OUT_DIR_REFUSED: " + str(exc), file=sys.stderr)
        return EXIT_OUT_DIR
    if destination == occurrence_root or occurrence_root in destination.parents:
        print("OUT_DIR_REFUSED: OUT_DIR_INSIDE_OCCURRENCE:" + str(args.out_dir),
              file=sys.stderr)
        return EXIT_OUT_DIR
    if args.out_dir.exists():
        print("OUT_DIR_REFUSED: OUT_DIR_EXISTS:" + str(args.out_dir), file=sys.stderr)
        return EXIT_OUT_DIR
    try:
        table = build_use_table(
            args.occurrence,
            problems=args.problem,
            arms=args.arm,
            cycles=args.cycle,
        )
    except CustodyError as exc:
        print("CUSTODY_REFUSED: " + str(exc), file=sys.stderr)
        return EXIT_CUSTODY
    except SelectorMatchedNothing as exc:
        # Before MappingError: SelectorMatchedNothing is one, and an operator
        # mistake in a selector is not the same failure as an occurrence that
        # cannot be read. The message already carries its own code.
        print(str(exc), file=sys.stderr)
        return EXIT_SELECTOR
    except MappingError as exc:
        print("BUILD_FAILED: " + str(exc), file=sys.stderr)
        return EXIT_BUILD

    try:
        markdown, document = write_use_table(table, args.out_dir)
    except OutDirRefused as exc:
        print("OUT_DIR_REFUSED: " + str(exc), file=sys.stderr)
        return EXIT_OUT_DIR
    except OSError as exc:
        # A permission error or a full disk is not a traceback and not exit 1:
        # it is a destination this run cannot use. write_use_table has already
        # removed whatever it managed to create.
        print("OUT_DIR_REFUSED: OUT_DIR_UNWRITABLE:%s: %s" % (args.out_dir, exc),
              file=sys.stderr)
        return EXIT_OUT_DIR

    print("occurrence : " + table.occurrence)
    print("plan_id    : " + table.custody["plan_id"])
    print("out_dir    : " + str(args.out_dir))
    print("scope      : " + ", ".join(
        "%s/%s/cycle%02d/%s" % (c["problem"], c["arm"], c["cycle"], c["node"])
        for c in table.scope))
    totals = table.reference_totals
    print("refs       : %d walked, %d cross-document rows, %d intra-document, "
          "%d to the exposed task artifact, %d unresolved"
          % (totals["refs_walked"], totals["cross_document_rows"],
             totals["intra_document"], totals["refs_to_exposed_task_artifact"],
             totals["unresolved"]))
    print("wrote      : %s, %s" % (markdown, document))
    if table.nodes_not_read:
        print()
        print("NODES WHOSE COMMITMENT SURFACE WAS NOT READ")
        for node in table.nodes_not_read:
            print("  %s - %s" % (node.coordinate_key, node.note))
    if table.unresolved_refs:
        print()
        print("REFS THAT RESOLVE TO NOTHING (residue, never dropped)")
        for residue in table.unresolved_refs:
            print("  %s %s.%s -> %s [%s]" % (
                residue.referring_coordinate_key, residue.referring_record_id or "-",
                residue.ref_field, residue.ref_verbatim, residue.code))
    print()
    print(USE_RELATION_BANNER.replace("**", ""))
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
