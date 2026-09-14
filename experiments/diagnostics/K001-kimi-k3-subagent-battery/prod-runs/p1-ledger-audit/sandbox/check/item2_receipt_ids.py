"""Item 2: distinct REC-\\d{8}-[A-Z]+ receipt ids in first-appearance order."""
import json

import common


def main():
    lines = common.load_lines()
    rows = common.receipt_ids(lines)
    payload = {
        "pattern": common.RECEIPT_PATTERN,
        "distinct_count": len(rows),
        "ids": rows,
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
