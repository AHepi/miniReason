"""Item 1: line census of docs/DECISION_LEDGER.md."""
import json

import common


def main():
    lines = common.load_lines()
    print(json.dumps(common.line_census(lines), indent=2))


if __name__ == "__main__":
    main()
