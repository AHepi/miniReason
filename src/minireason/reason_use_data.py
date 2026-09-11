"""Generic candidate reason-use instructions; no selected experiment material."""
SYSTEM_MESSAGE = (
    "Respond in ordinary prose, with optional formal expressions or fenced source code. "
    "No JSON envelope is required. Preserve uncertainty and substantive criticism. "
    "No scalar score, creativity verdict or semantic status assignment is requested."
)
STAGE_INSTRUCTIONS = {
    "respond": (
        "Consider the fixed construction in relation to the complete supplied source and the "
        "supplemental criticism, if any. State which parts you retain, reject, qualify or leave "
        "unresolved, and why. A criticism is fallible: do not make a change merely because one "
        "was supplied. Return the account you would now use for the original question, while "
        "keeping the original construction and source as distinct historical occurrences. "
        "Explain disputed interpretations that affect your response. Return a self-contained "
        "proposed account for possible separate use without the original construction, source "
        "packet or supplemental criticism. Carry any distinctions needed by that proposed account "
        "in your response. This describes a text return route; it installs no executable "
        "program, language amendment or semantic standing."
    ),
    "use": (
        "Using the supplied material, address the supplied questions under the explicit "
        "use-domain data. This request does not provide the original construction, source "
        "packet or supplemental criticism. Identify the grounds of each answer and any "
        "needed distinction or unresolved issue. If an account is supplied, explain how it "
        "bears on each answer. You may criticize or depart from it, identifying the departure "
        "and its reason. Do not silently treat a new assumption as supplied material. "
        "Ordinary prose is sufficient. This is an observed use response, not an automatic "
        "certificate of repair, reason use, correctness or creativity."
    ),
}
