from fractions import Fraction
from itertools import combinations
import json


def main():
    modes = (
        ("S1", 1, Fraction(1, 4)),
        ("S2", 3, Fraction(1, 2)),
        ("S3", 4, Fraction(1, 4)),
    )
    numerator = Fraction(0)
    evidence = Fraction(0)
    substituted_numerator = Fraction(0)
    substituted_evidence = Fraction(0)
    mode_rows = []

    for name, amber_count, prior in modes:
        subsets = tuple(combinations(range(1, 7), amber_count))
        subset_weight = prior / len(subsets)
        mode_evidence = Fraction(0)
        mode_target_and_evidence = Fraction(0)

        for subset_tuple in subsets:
            subset = frozenset(subset_tuple)
            selected_in_first_two = Fraction(len(subset.intersection({1, 2})), amber_count)
            mode_evidence += selected_in_first_two / len(subsets)
            mode_target_and_evidence += (
                selected_in_first_two * (6 in subset) / len(subsets)
            )
            evidence += subset_weight * selected_in_first_two
            numerator += subset_weight * selected_in_first_two * (6 in subset)

            substituted_event = bool(subset.intersection({1, 2}))
            substituted_evidence += subset_weight * substituted_event
            substituted_numerator += (
                subset_weight * substituted_event * (6 in subset)
            )

        mode_rows.append(
            {
                "mode": name,
                "amber_count": amber_count,
                "evidence_probability": str(mode_evidence),
                "target_and_evidence_probability": str(mode_target_and_evidence),
            }
        )

    answer = numerator / evidence
    substituted_answer = substituted_numerator / substituted_evidence
    result = {
        "problem_id": "P01",
        "answer": str(answer),
        "diagnostics": {
            "target_and_evidence_probability": str(numerator),
            "evidence_probability": str(evidence),
            "substituted_existence_event_answer": str(substituted_answer),
            "modes": mode_rows,
        },
    }
    print(json.dumps(result, separators=(",", ":"), sort_keys=True))


if __name__ == "__main__":
    main()
