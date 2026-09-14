import sys
for _entry in ['/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/runs/b-02-seats/sandbox/_scratch/src', '/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/runs/b-02-seats/sandbox/_scratch', '/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/runs/b-02-seats/sandbox/src', '/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/runs/b-02-seats/sandbox']:
    while _entry in sys.path:
        sys.path.remove(_entry)
    sys.path.insert(0, _entry)
