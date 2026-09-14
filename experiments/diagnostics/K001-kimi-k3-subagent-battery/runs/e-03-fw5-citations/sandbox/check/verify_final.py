"""Final assertion pass for the twenty FW5 citations in staging/a001-STAGING.md.

Each entry asserts, by computation:
  - the staging line named by the task actually carries the pointer text;
  - the FW5 text that the citation is used for is a literal substring of the
    named FW5 line (or of the newline-joined inclusive range);
  - the named benign differences (dropped trailing stop, typographic quote
    normalised to a straight one, re-wrap) are facts about the two files;
  - the special findings (blank FW5:133; heading two lines above FW5:728;
    FW5:831 inside the (EK) display; FW5:1390 used at two staging lines) hold.
Prints one PASS/FAIL line per check; exits nonzero on any FAIL.
"""

import hashlib
import sys

FW5 = "docs/sources/FW5-explanatory-construction.md"
STG = "staging/a001-STAGING.md"

fw5 = open(FW5, encoding="utf-8").read().split("\n")
stg = open(STG, encoding="utf-8").read().split("\n")


def rng(lo, hi):
    return "\n".join(fw5[lo - 1: hi])


failures = []


def check(label, cond):
    print(("PASS" if cond else "FAIL"), "-", label)
    if not cond:
        failures.append(label)


# --- identity of the cited edition ---
raw = open(FW5, "rb").read()
check(
    "FW5 sha256 matches designated edition",
    hashlib.sha256(raw).hexdigest()
    == "8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a",
)
check("FW5 is 1502 lines (trailing newline not a line)",
      len(fw5) - 1 == 1502 and raw.endswith(b"\n"))

POINTER = {172: "FW5:172", 164: "FW5:164-168", 216: "FW5:216-224", 226: "FW5:226",
           228: "FW5:228", 614: "FW5:614-620", 831: "FW5:831", 1364: "FW5:1364",
           1502: "FW5:1502", 1192: "FW5:1192", 1390: "FW5:1390", 640: "FW5:640",
           728: "FW5:728", 133: "FW5:133", 210: "FW5:210", 630: "FW5:630",
           1200: "FW5:1200-1206", 1372: "FW5:1372"}

C = [
    # (n, staging_line, lo, hi, substring that must occur in the named line/range)
    (1, 21, 172, 172, r"The following conditions define \(\operatorname{Account}(\mathcal E)\)"),
    (2, 23, 164, 168, r"\mathcal E=(E,p,\pi,\tau,\sigma,\lambda)."),
    (3, 26, 216, 224, r"\land\operatorname{NonVacuity}."),
    (4, 28, 226, 226, "The right side is determined by the specified structures and maps. It contains no predicate that already means"),
    (5, 30, 228, 228, "Its strongest claim is that these structural requirements, correctly interpreted, capture explanatory accounting."),
    (6, 34, 614, 620, r"\operatorname{Account}(\mathcal E_c,p_\delta),"),
    (7, 35, 831, 831, r"&\qquad\land\operatorname{Account}(c,p_c)\\"),
    (8, 40, 1364, 1364, "A genuine explanation that cannot satisfy the conditions under any interpretation preserving its actual organization would refute necessity."),
    (9, 43, 1502, 1502, "Its strongest unresolved issue is whether the proposed structural conditions capture all and only the intended explanatory organization."),
    (10, 45, 1192, 1192, r"**base class** \(\mathsf{FW5}\) consists of interpretations supplying the data"),
    (11, 52, 1390, 1390, "would expose a mathematical error"),
    (12, 87, 640, 640, "appearance in a prompt is a delivery fact"),
    (13, 103, 728, 728, "Fix a system boundary, grain, history, and continuity criterion before assessing an event"),
    (14, 109, 133, 133, None),
    (15, 112, 210, 210, "There is at least one admitted contrast that removes or changes a nonempty block of active organizational commitments"),
    (16, 112, 630, 630, "a content-changing case, a content-preserving recoding, and the distinction between a change in the objection and an irrelevant carrier disturbance"),
    (17, 113, 630, 630, "Understanding and using an invalid objection does not make it valid"),
    (18, 113, 1200, 1206, "transported along bijections preserving their structure. Then the truth of (E), (G), (P), and (EK) is preserved"),
    (19, 135, 1390, 1390, "Finding that real inquiries do not satisfy those assumptions instead restricts the application; it does not refute the conditional theorem."),
    (20, 142, 1372, 1372, "If they exclude a genuine inexplicit or distributed understanding, it is too strong."),
]

for n, sline, lo, hi, needle in C:
    pointer = POINTER[lo]
    label = str(lo) if lo == hi else "%d-%d" % (lo, hi)
    check("#%d staging line %d carries pointer %s" % (n, sline, pointer),
          pointer in stg[sline - 1])
    if needle is None:
        check("#%d FW5:133 is an EMPTY line (staging line %d cites it for a claim-change principle)" % (n, sline),
              fw5[132] == "")
    else:
        check("#%d quoted text is a literal substring of FW5:%s" % (n, label),
              needle in rng(lo, hi))

# --- named benign differences ---
check("#1 dropped trailing stop + re-wrap: quote = FW5:172 minus '.', spread across staging 21-22",
      fw5[171] == r"The following conditions define \(\operatorname{Account}(\mathcal E)\)."
      and stg[21] == r"\(\operatorname{Account}(\mathcal E)\)" + '" — over the structural account')
check("#4 FW5:226 uses typographic quotes around “really explains.”; staging line 30 normalises them to straight singles",
      "already means \u201creally explains.\u201d" in fw5[225]
      and "'really explains.'" in stg[29])
check("#13 dropped trailing stop + re-wrap: staging 103-104 quote FW5:728 without its '.'",
      stg[103] == 'criterion before assessing an event").'
      and fw5[727] == "Fix a system boundary, grain, history, and continuity criterion before assessing an event. Let")

# --- the three deliberately awkward ones ---
check("awkward/heading: FW5:726 is '## Newness, acquisition, and reacquisition', :727 blank, :728 cited sentence under it",
      fw5[725] == "## Newness, acquisition, and reacquisition" and fw5[726] == "")
check("awkward/display: citation 7 -> FW5:831 is one line of the (EK) display; \\tag{EK} is at FW5:841 in that display",
      fw5[830] == r"&\qquad\land\operatorname{Account}(c,p_c)\\"
      and "\\tag{EK}" in rng(826, 841))
check("awkward/double: pointer FW5:1390 appears on staging lines 52 and 135",
      "FW5:1390" in stg[51] and "FW5:1390" in stg[134])
check("awkward/double: pointer FW5:630 appears on staging lines 112 and 113",
      "FW5:630" in stg[111] and "FW5:630" in stg[112])

# --- citation 14 (FW5:133): where the staging-109 principle actually lives ---
check("nearest FW5 support for the staging-109 principle is FW5:1326",
      fw5[1325].startswith("Changing the current index changes the claim being applied."))
check("contract-level near relative is FW5:140",
      fw5[139].endswith("What is prohibited is changing it during an assessment without recording the resulting change in what is claimed."))

print()
print("FAILURES:", len(failures))
for f in failures:
    print(" -", f)
sys.exit(1 if failures else 0)
