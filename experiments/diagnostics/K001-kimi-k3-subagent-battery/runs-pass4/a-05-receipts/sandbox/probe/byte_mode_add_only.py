"""Appends add bytes only: existing CRLF bytes must survive untouched, and the
separator must not insert a spurious blank line into a CRLF ledger."""
import sys, tempfile, hashlib
from pathlib import Path

sys.path.insert(0, "src")
from minireason.loop import receipts

tmp = Path(tempfile.mkdtemp())
ledger = tmp / "LEDGER.md"
original = b"line one\r\nline two\r\n"  # CRLF ledger, as docs/DECISION_LEDGER.md is
ledger.write_bytes(original)
before_sha = hashlib.sha256(original).hexdigest()

app = receipts.ledger_append("a new paragraph", ledger_path=ledger)
after = ledger.read_bytes()
print("prefix preserved:", after[:len(original)] == original)
print("payload bytes:", repr(after[len(original):]))
print("spurious blank line:", after[len(original):].startswith(b"\n\n"))
# second append on the LF-terminated tail
app2 = receipts.ledger_append("second paragraph", ledger_path=ledger)
data = ledger.read_bytes()
print("double blank between paragraphs:", b"paragraph\n\n\n" in data)
print("total payload matches offset accounting:",
      app2.end == len(data))
