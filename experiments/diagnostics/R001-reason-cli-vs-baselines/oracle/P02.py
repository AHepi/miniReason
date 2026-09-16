from itertools import combinations
import json


SIZE = 12


def rotate(text, amount):
    return text[amount:] + text[:amount]


def reflect(text, offset):
    return "".join(text[(offset - index) % SIZE] for index in range(SIZE))


def valid_indexed_strings():
    strings = []
    positions = range(SIZE)
    for a_positions_tuple in combinations(positions, 4):
        a_positions = frozenset(a_positions_tuple)
        remaining = tuple(index for index in positions if index not in a_positions)
        for b_positions_tuple in combinations(remaining, 4):
            b_positions = frozenset(b_positions_tuple)
            text = "".join(
                "A" if index in a_positions else "B" if index in b_positions else "C"
                for index in positions
            )
            if all(text[index] != text[(index + 1) % SIZE] for index in positions):
                strings.append(text)
    return tuple(strings)


def main():
    strings = valid_indexed_strings()
    rotation_fixed = [
        sum(rotate(text, amount) == text for text in strings)
        for amount in range(SIZE)
    ]
    reflection_fixed = [
        sum(reflect(text, offset) == text for text in strings)
        for offset in range(SIZE)
    ]

    representatives = set()
    orbit_sizes = {}
    for text in strings:
        images = {rotate(text, amount) for amount in range(SIZE)}
        images.update(
            rotate(reflect(text, 0), amount)
            for amount in range(SIZE)
        )
        representative = min(images)
        representatives.add(representative)
        orbit_sizes[representative] = len(images)

    assert sum(rotation_fixed) + sum(reflection_fixed) == 24 * len(representatives)
    assert sum(orbit_sizes.values()) == len(strings)

    result = {
        "problem_id": "P02",
        "answer": str(len(representatives)),
        "diagnostics": {
            "valid_indexed_strings": len(strings),
            "rotation_fixed_counts": rotation_fixed,
            "reflection_fixed_counts": reflection_fixed,
            "burnside_fixed_sum": sum(rotation_fixed) + sum(reflection_fixed),
            "orbit_size_counts": {
                str(size): sum(value == size for value in orbit_sizes.values())
                for size in sorted(set(orbit_sizes.values()))
            },
        },
    }
    print(json.dumps(result, separators=(",", ":"), sort_keys=True))


if __name__ == "__main__":
    main()
