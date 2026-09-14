"""Item 6: VERIFIED <40 hex> TREE <40 hex> lines with nearest receipt above."""
import json

import common


def main():
    lines = common.load_lines()
    print(json.dumps(common.verified_tree(lines), indent=2))


if __name__ == "__main__":
    main()
