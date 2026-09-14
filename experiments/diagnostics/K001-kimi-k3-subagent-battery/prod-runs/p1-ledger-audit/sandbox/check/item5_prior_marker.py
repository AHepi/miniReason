"""Item 5: lines containing the exact substring 'Prior verified commit/tree:'."""
import json

import common


def main():
    lines = common.load_lines()
    print(json.dumps(common.prior_marker(lines), indent=2))


if __name__ == "__main__":
    main()
