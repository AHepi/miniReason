"""Secret-in-receipt refusal, done correctly: a credential env name must be
declared (fixed set, endpoint key_env, or register_secret_envs) for the scanner
to see it. Then a secret-bearing body must be refused with SECRET_IN_RECEIPT,
never written, and the refusal must name the env var, never the value."""
import sys, tempfile, os
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, "src")
from minireason.loop import receipts
from minireason.loop.types import LoopError
from minireason.provider_openai_compat import register_secret_envs, _reset_registered_secret_envs

tmp = Path(tempfile.mkdtemp())
ledger = tmp / "LEDGER.md"
ledger.write_bytes(b"# ledger\n")
moment = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)

os.environ["PROBE_REG_CRED"] = "ak-1234567890abcdef"
register_secret_envs(["PROBE_REG_CRED"])
size_before = ledger.stat().st_size
try:
    receipts.open_receipt(body="token is ak-1234567890abcdef in the log",
                          ledger_path=ledger, moment=moment, set_current=False)
    print("attack SUCCEEDED: secret written")
except LoopError as e:
    value_leaked = "ak-1234567890abcdef" in str(e)
    print("refused:", e.code, "| names:", getattr(e, "names", None),
          "| value leaked into exception:", value_leaked)
print("ledger unchanged:", ledger.stat().st_size == size_before)
_reset_registered_secret_envs()
del os.environ["PROBE_REG_CRED"]

# control: DEEPSEEK_API_KEY is in the always-secret set, value-length >= 8
os.environ["DEEPSEEK_API_KEY"] = "dsk-testvalue123"
size_before = ledger.stat().st_size
try:
    receipts.ledger_append("key dsk-testvalue123 here", ledger_path=ledger)
    print("attack SUCCEEDED: secret written")
except LoopError as e:
    print("refused:", e.code, "| ledger unchanged:",
          ledger.stat().st_size == size_before)
del os.environ["DEEPSEEK_API_KEY"]
