"""Import one H005 occurrence into a spec-v1.3 graph root. Offline; no provider.

Reads only the occurrence directory, writes only a new graph root. Refuses to
run unless the occurrence's plan identity, material pin, manifest pins and
per-node artifact, request, trace and provider-byte custody verify. No
credential is read and no network call is made.

Exit codes (the table is repeated in docs/workflows/graph-import-h005.md):

    0  the import succeeded. An unresolvable --why is still 0: the import
       succeeded and only the display selector was wrong.
    2  CUSTODY_REFUSED - the occurrence failed a custody check (including a
       missing or malformed occurrence file); nothing was written.
    3  IMPORT_FAILED - the occurrence is well-custodied but could not be
       mapped as specified. EMPTY_SCOPE (the occurrence holds no coordinate
       at all) is one of these.
    4  OUT_ROOT_REFUSED - the destination is not usable (inside the
       occurrence, or already exists). The occurrence is fine.
    5  SELECTOR_MATCHED_NOTHING - the occurrence holds coordinates but
       --problem/--arm/--cycle matched none of them. The occurrence and the
       destination are both fine; the selector is wrong, and stderr lists
       what the occurrence actually holds.

argparse keeps its own usage-error behaviour and this tool does not remap it;
a usage error is told apart from a custody refusal by the ``usage:`` line
argparse prints, and by the absence of ``CUSTODY_REFUSED:``.
"""
from __future__ import annotations

import argparse
import difflib
from pathlib import Path
import sys

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / 'src'))
from minireason.graph_import_h005 import (  # noqa: E402
    I7_BANNER,
    CustodyError,
    MappingError,
    OutRootRefused,
    SelectorMatchedNothing,
    import_occurrence,
)

EXIT_OK = 0
EXIT_CUSTODY = 2
EXIT_MAPPING = 3
EXIT_OUT_ROOT = 4
EXIT_SELECTOR = 5


def _print_why(report, wanted: str) -> None:
    """Print one why chain, or say what could not be resolved and carry on.

    A bad ``--why`` is a bad *display selector*, not a bad import: the root is
    already written and re-running to fix a typo would hit the write-once
    guard. So it is reported on stderr and the exit code stays 0.
    """
    try:
        print()
        print(report.why(wanted))
    except KeyError:
        candidates = sorted(set(report.names.values()))
        close = difflib.get_close_matches(wanted, candidates, n=5, cutoff=0.3)
        if not close:
            close = [name for name in candidates if wanted.lower() in name.lower()][:5]
        print('WHY_UNRESOLVED: ' + wanted, file=sys.stderr)
        if close:
            print('  closest candidates: ' + ', '.join(close), file=sys.stderr)
        else:
            print('  no artifact name resembles it; try one of: '
                  + ', '.join(candidates[:5]), file=sys.stderr)
        print('  the import itself succeeded; only this selector did not resolve.',
              file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('occurrence', type=Path, help='H005 occurrence directory (read-only)')
    parser.add_argument('out_root', type=Path, help='new graph root; must not exist')
    parser.add_argument('--problem', action='append', default=None,
                        help='restrict to this problem id (repeatable)')
    parser.add_argument('--arm', action='append', default=None,
                        help='restrict to this arm (repeatable)')
    parser.add_argument('--cycle', action='append', type=int, default=None,
                        help='restrict to this cycle (repeatable)')
    parser.add_argument('--dry-run', action='store_true',
                        help='compute and print the import without writing anything')
    parser.add_argument('--why', default=None,
                        help='print the attack/defence chain for one artifact '
                             '(id, unique id prefix, or coordinate key)')
    args = parser.parse_args()
    try:
        report = import_occurrence(args.occurrence, args.out_root, problems=args.problem,
                                   arms=args.arm, cycles=args.cycle, dry_run=args.dry_run)
    except CustodyError as exc:
        print('CUSTODY_REFUSED: ' + str(exc), file=sys.stderr)
        return EXIT_CUSTODY
    except OutRootRefused as exc:
        print('OUT_ROOT_REFUSED: ' + str(exc), file=sys.stderr)
        return EXIT_OUT_ROOT
    except SelectorMatchedNothing as exc:
        # Before MappingError: SelectorMatchedNothing is one, and an operator
        # mistake in a selector is not the same failure as an occurrence that
        # cannot be mapped. The message already carries its own code.
        print(str(exc), file=sys.stderr)
        return EXIT_SELECTOR
    except MappingError as exc:
        print('IMPORT_FAILED: ' + str(exc), file=sys.stderr)
        return EXIT_MAPPING
    print('occurrence : ' + report.occurrence)
    print('plan_id    : ' + report.custody['plan_id'])
    print('out_root   : ' + (report.out_root or '(dry run: nothing written)'))
    print('scope      : ' + ', '.join(
        '%s/%s/cycle%02d/%s' % (c['problem'], c['arm'], c['cycle'], c['node'])
        for c in report.scope))
    print('events     : %d  artifacts: %d  warrants: %d  att: %d  dep: %d'
          % (report.events_count, len(report.labels), len(report.warrants),
             len(report.att_edges), len(report.dep_edges)))
    print()
    print('I7: ' + I7_BANNER.replace('**', ''))
    errors = report.error_severity_totals
    if errors:
        print('ERROR-SEVERITY RESIDUE FIRED: ' + ', '.join(
            '%s (%d)' % (code, count) for code, count in errors.items())
            + ' -- read the residue before reading any label.')
    if report.multi_arm_framing:
        print()
        print(report.multi_arm_framing)
    print()
    print('LABELS')
    print(report.labels_table())
    print()
    print('RESIDUE')
    print(report.residue_summary())
    if args.why:
        _print_why(report, args.why)
    return EXIT_OK


if __name__ == '__main__':
    raise SystemExit(main())
