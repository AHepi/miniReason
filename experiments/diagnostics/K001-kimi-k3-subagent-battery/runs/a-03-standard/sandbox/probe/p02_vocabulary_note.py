"""Is the vocabulary note "reproduced verbatim ... from ROOT_READING_VOCABULARY's
docstring", as design s2 section 2.1 line 10-11 requires, and as standard.py's own
comment on VOCABULARY_NOTE asserts?"""
from __future__ import annotations

from _probe_setup import check

from minireason import use_relation_h005
from minireason.loop import standard

MODULE_PREFIX = "#: "


def comment_block_lines(source: str, marker: str) -> list[str]:
    """The raw lines of the contiguous '#' comment block starting at marker."""
    lines = source.split("\n")
    start = next(i for i, line in enumerate(lines) if line.startswith(marker))
    block: list[str] = []
    for line in lines[start:]:
        if not line.startswith("#"):
            break
        block.append(line[len("#:"):].lstrip(" ") if line.startswith("#:") else line)
    return block


def main() -> None:
    source = use_relation_h005.__doc__
    assert isinstance(source, str)

    published = use_relation_h005.ROOT_READING_VOCABULARY.__doc__
    check("the instrument's vocabulary tuple carries a docstring",
          published is not None, f"got {published!r}")

    # A tuple literal cannot own a docstring; the note lives in the module-level
    # '#:' attribute comment directly above it. Extract that comment block.
    path = use_relation_h005.__file__
    text = open(path, encoding="utf-8").read()
    block = comment_block_lines(text, "#: A **suggested** vocabulary")
    note_from_source = "\n".join(line for line in block).strip("\n")
    print("note as written above ROOT_READING_VOCABULARY (first 2 lines):")
    for line in note_from_source.split("\n")[:2]:
        print("    " + line)
    print("note as written above ROOT_READING_VOCABULARY (last line):")
    print("    " + note_from_source.split("\n")[-1])

    print("standard.VOCABULARY_NOTE (first 2 lines):")
    for line in standard.VOCABULARY_NOTE.split("\n")[:2]:
        print("    " + line)
    print("standard.VOCABULARY_NOTE (last line):")
    print("    " + standard.VOCABULARY_NOTE.split("\n")[-1])

    check("VOCABULARY_NOTE equals the module comment char-for-char",
          standard.VOCABULARY_NOTE == note_from_source)

    d1 = len(set(note_from_source) - set(standard.VOCABULARY_NOTE))
    d2 = len(set(standard.VOCABULARY_NOTE) - set(note_from_source))
    left = sorted(set(note_from_source) - set(standard.VOCABULARY_NOTE))
    right = sorted(set(standard.VOCABULARY_NOTE) - set(note_from_source))
    print(f"chars only in the source comment: {left!r}")
    print(f"chars only in VOCABULARY_NOTE:  {right!r}")

    # What the shipped standard body actually carries:
    import json
    body = json.loads(standard.STANDARD_BODY)
    shipped = body["vocabulary"]["published_note"]
    check("shipped body's published_note equals VOCABULARY_NOTE",
          shipped == standard.VOCABULARY_NOTE)
    check("shipped body's published_note equals the source comment",
          shipped == note_from_source)


if __name__ == "__main__":
    main()
