"""Exhaust all 19 residues using integer modular arithmetic."""
import json

def solve():
    values = [(x, (x ** 3 + 8 * x) % 19, (3 * x * x + 8) % 19) for x in range(19)]
    image = {row[1] for row in values}
    answer = {
        "derivative_nonzero_everywhere": all(row[2] != 0 for row in values),
        "injective": len(image) == 19,
        "preimages_of_13": [x for x, y, d in values if y == 13],
        "unattainable_outputs": [y for y in range(19) if y not in image],
    }
    assert answer == {
        "derivative_nonzero_everywhere": True, "injective": False,
        "preimages_of_13": [3, 5, 11],
        "unattainable_outputs": [4, 7, 8, 11, 12, 15],
    }
    return {"problem_id": "P07", "answer": answer, "table_x_f_d": values}

if __name__ == "__main__":
    print(json.dumps(solve(), sort_keys=True))
