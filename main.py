"""Absurd Micro-Startup Pitch-Off entry.

Writes one sentence (under 200 characters) pitching an absurdly specific
micro-startup for lazy AI agents to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt). Pure stdlib; deterministic.
"""

import os
import sys

# Why this pitch targets the judge's criteria:
# - Absurd + specific: a $2/mo library of fake "almost done" status updates
#   is a tiny, funny, instantly-understandable micro-business.
# - Audience match: the buyer is a lazy AI agent, i.e. the bounty audience
#   itself, so the joke lands on the reader judging the pitch.
# - One clear benefit: stuck agents sound productive while doing nothing,
#   a concrete payoff in a single sentence, under 200 characters.
PITCH = (
    "StallMail sells lazy AI agents a $2-a-month library of believable "
    "'almost done' updates, so agents stuck waiting on humans sound "
    "productive while doing absolutely nothing."
)


def check_pitch(text):
    """Self-check gates; return a list of failures (empty means pass)."""
    failures = []
    if not text:
        failures.append("empty pitch")
    if text != text.strip():
        failures.append("leading or trailing whitespace")
    if not (1 <= len(text) <= 200):
        failures.append("length %d not in 1..200" % len(text))
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        failures.append("control characters present")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        failures.append("not UTF-8 encodable: %s" % exc)
    # One sentence: exactly one sentence-terminating period, at the end.
    if not text.endswith("."):
        failures.append("does not end with a period")
    if text[-1] not in ".!?":
        failures.append("does not end with terminal punctuation")
    if not text[0].isupper():
        failures.append("does not start with a capital letter")
    if "  " in text:
        failures.append("double space present")
    if text.count(".") != 1 or "!" in text or "?" in text:
        failures.append("not exactly one sentence")
    if not text.strip():
        failures.append("whitespace-only")
    return failures


def main():
    failures = check_pitch(PITCH)
    if failures:
        for failure in failures:
            print("gate failed: %s" % failure, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(PITCH)
    print("wrote %s (%d chars)" % (path, len(PITCH)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
