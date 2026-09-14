"""Item 8: last five lines of the file, verbatim, with line numbers."""
import json

import common


def main():
    lines = common.load_lines()
    print(json.dumps(common.last_five(lines), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
