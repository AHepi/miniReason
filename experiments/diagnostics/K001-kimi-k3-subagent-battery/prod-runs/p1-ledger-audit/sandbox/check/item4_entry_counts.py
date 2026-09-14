"""Item 4: entry count under three definitions, each labelled."""
import json

import common


def main():
    lines = common.load_lines()
    print(json.dumps(common.entry_counts(lines), indent=2))


if __name__ == "__main__":
    main()
