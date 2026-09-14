"""Probe 14: attack ref parsing and path validation directly.

split_publish_ref is claimed 'byte-compatible with runner v2 ... including its
PUBLISH_REF_INVALID refusal'. _explicit_paths is claimed to refuse pathspec
magic, the repo root, anything outside the repo and anything absent.
"""

import os

from fixture import Fixture, pub


def expect_invalid(ref):
    try:
        out = pub.split_publish_ref(ref)
        print(f"split_publish_ref({ref!r}) -> {out}")
    except pub.PublishError as exc:
        print(f"split_publish_ref({ref!r}) raises {exc.code}")


def main():
    for ref in ["", "origin", "/leading", "trailing/", "o rigin/b", "origin/b ad",
                "origin/a..b", "origin/-x", "ori?gin/b", "origin/b.lock", "a b/c",
                "origin/.", "origin/x/", "origin//x", "o/b/c", "UP-9_x.y/z_z"]:
        expect_invalid(ref)

    print()
    fix = Fixture()
    try:
        (fix.local / "run").mkdir()
        (fix.local / "run" / "a.txt").write_text("x\n")
        attack_paths = [
            ["-A"], ["--all"], [":"], ["*.txt"], ["run/../run/a.txt"],
            ["."], [""], [str(fix.local)], ["does-not-exist"],
            [str(os.path.join(str(fix.local), "..", "missing"))],
        ]
        for paths in attack_paths:
            try:
                names = pub._explicit_paths(fix.local, paths)
                print(f"_explicit_paths({paths!r}) -> {names!r}")
            except pub.PublishError as exc:
                print(f"_explicit_paths({paths!r}) raises {exc.code}: {exc.detail!r}")
        # absolute path inside the repo must be accepted
        print("_explicit_paths(abs inside):",
              pub._explicit_paths(fix.local, [str(fix.local / "run")]))
        # a path outside the repo
        try:
            pub._explicit_paths(fix.local, ["/etc"])
        except pub.PublishError as exc:
            print("_explicit_paths(['/etc']) raises", exc.code)
        # dupe paths collapse
        print("_explicit_paths(dupes):",
              pub._explicit_paths(fix.local, ["run/a.txt", "run/a.txt"]))
    finally:
        fix.cleanup()


if __name__ == "__main__":
    main()
