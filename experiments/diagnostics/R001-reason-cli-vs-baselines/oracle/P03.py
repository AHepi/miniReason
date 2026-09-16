import json


TRANSITIONS = {
    ("A", "L"): ("B", lambda x, y: ((x + y) % 10, (x + 3) % 10)),
    ("A", "R"): ("C", lambda x, y: ((2 * x + y) % 10, (y + 4) % 10)),
    ("B", "L"): ("C", lambda x, y: ((x + 2 * y) % 10, (x + y) % 10)),
    ("B", "R"): ("A", lambda x, y: ((x + 5) % 10, (x + 2 * y) % 10)),
    ("C", "L"): ("A", lambda x, y: ((3 * x + y) % 10, (y + 6) % 10)),
    ("C", "R"): ("B", lambda x, y: ((x + y + 1) % 10, (2 * x + y) % 10)),
}

SEQUENTIAL_MISREAD = {
    ("A", "L"): ("B", lambda x, y: ((x + y) % 10, ((x + y) % 10 + 3) % 10)),
    ("A", "R"): ("C", lambda x, y: ((2 * x + y) % 10, (y + 4) % 10)),
    ("B", "L"): (
        "C",
        lambda x, y: ((x + 2 * y) % 10, ((x + 2 * y) % 10 + y) % 10),
    ),
    ("B", "R"): (
        "A",
        lambda x, y: ((x + 5) % 10, ((x + 5) % 10 + 2 * y) % 10),
    ),
    ("C", "L"): ("A", lambda x, y: ((3 * x + y) % 10, (y + 6) % 10)),
    ("C", "R"): (
        "B",
        lambda x, y: (
            (x + y + 1) % 10,
            (2 * ((x + y + 1) % 10) + y) % 10,
        ),
    ),
}


def emit(x, y):
    if x < y:
        return "E"
    if x == y:
        return "T"
    return "G"


def run_machine(transitions):
    state = "A"
    x = 2
    y = 5
    emitted = []
    trace = []
    input_text = "LRRLLRLRRLLRRL"

    for step, symbol in enumerate(input_text, 1):
        old_state, old_x, old_y = state, x, y
        next_state, update = transitions[(old_state, symbol)]
        new_x, new_y = update(old_x, old_y)
        emitted_symbol = emit(new_x, new_y)
        trace.append(
            {
                "step": step,
                "input": symbol,
                "pre": [old_state, old_x, old_y],
                "post": [next_state, new_x, new_y],
                "emit": emitted_symbol,
            }
        )
        state, x, y = next_state, new_x, new_y
        emitted.append(emitted_symbol)

    return state, x, y, "".join(emitted), trace


def main():
    state, x, y, output, trace = run_machine(TRANSITIONS)
    wrong_state, wrong_x, wrong_y, wrong_output, _ = run_machine(SEQUENTIAL_MISREAD)
    result = {
        "problem_id": "P03",
        "answer": f"state={state}; x={x}; y={y}; output={output}",
        "diagnostics": {
            "steps": len(trace),
            "trace": trace,
            "sequential_misread": {
                "state": wrong_state,
                "x": wrong_x,
                "y": wrong_y,
                "output": wrong_output,
            },
        },
    }
    print(json.dumps(result, separators=(",", ":"), sort_keys=True))


if __name__ == "__main__":
    main()
