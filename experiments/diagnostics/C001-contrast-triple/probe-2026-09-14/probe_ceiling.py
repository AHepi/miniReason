"""ONE probe call: deepseek-flash at a declared max_tokens ceiling.

Uses tools/provider_smoke.py's own `load_env_file` and `probe`, so the call goes
through exactly the transport, record discipline and credential redaction the study
uses. Exactly one `complete()` is sent; no /models call, no retry, no second attempt.

  python3 probe_ceiling.py <records_dir> <max_tokens>

Prints the probe row only. No credential value, fragment or header ever reaches
stdout or any file: `load_env_file` never returns a value and registers every name
it set with the transport's redaction set.
"""
import json
import sys
from pathlib import Path

REPO = Path('/home/user/miniReason')
sys.path.insert(0, str(REPO / 'tools'))
sys.path.insert(0, str(REPO / 'src'))

import provider_smoke as smoke                       # noqa: E402
from minireason.provider_openai_compat import ENDPOINTS  # noqa: E402

records = Path(sys.argv[1])
ceiling = int(sys.argv[2])
if records.exists() and any(records.iterdir()):
    raise SystemExit('RECORDS_DIR_NOT_EMPTY')
records.mkdir(parents=True, exist_ok=True)

names = smoke.load_env_file(REPO / '.env')
print(json.dumps({'env_names_loaded': sorted(names), 'ceiling': ceiling,
                  'records_dir': str(records)}, sort_keys=True))

row = smoke.probe(records, ENDPOINTS['deepseek-flash'],
                  max_tokens=ceiling, label=f'ceiling-{ceiling}')
print(json.dumps(row, ensure_ascii=False, indent=1, sort_keys=True))
