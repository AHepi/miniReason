"""Item 7: credential-pattern scan.

SECURITY: prints ONLY line numbers. Matched text is never printed.
"""
import json

import common


def main():
    lines = common.load_lines()
    print(json.dumps(common.credential_scan(lines), indent=2))


if __name__ == "__main__":
    main()
