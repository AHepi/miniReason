#!/bin/bash
# Waits for the first Atria hard-to-vary batch to end, then reruns every item whose record carries an error, into a separate folder.
cd "$(dirname "$0")"
until [ "$(ls replies_htv_atria | grep -c json)" -ge 9 ]; do sleep 30; done
echo "htv batch complete at $(date -u)"
ONLY=$(python3 -c "
import json,glob
ids=[json.load(open(p))['id'] for p in sorted(glob.glob('replies_htv_atria/*.json')) if json.load(open(p)).get('error')]
print(','.join(i+':0' for i in ids))")
echo "failed items: $ONLY"
set -a; . ../keys.env; set +a
XEXAM_ONLY="$ONLY" XEXAM_STREAM=1 XEXAM_SKILL_DIR=../skill_htv/hard-to-vary XEXAM_SKILL_FRAME=frame_htv.txt XEXAM_ENDPOINT="https://api.atria-asi.ai/v1/chat/completions" XEXAM_MODEL="Atria-Dawn-Preview" XEXAM_KEY="$ATRIA_API_KEY" XEXAM_MAX_TOKENS=65536 XEXAM_TIMEOUT=2400 python3 cross_examine_skill.py battery_rev.json replies_htv_atria_retry --samples 1 --workers 2
echo "retry batch done at $(date -u): $(ls replies_htv_atria_retry | grep -c json)"
