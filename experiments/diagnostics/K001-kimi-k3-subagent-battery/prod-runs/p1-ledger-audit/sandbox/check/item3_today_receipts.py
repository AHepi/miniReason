"""Item 3: receipts dated 20260914, letter sequence, A..Z coverage."""
import json

import common


def main():
    lines = common.load_lines()
    rows = common.receipt_ids(lines)
    print(json.dumps(common.today_receipts(rows), indent=2))


if __name__ == "__main__":
    main()
