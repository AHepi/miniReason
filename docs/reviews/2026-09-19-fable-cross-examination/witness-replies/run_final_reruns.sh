#!/bin/bash
# Final low-concurrency pass: after the first rerun ends, run every still-failed Atria item of both skills one at a time, into separate folders.
cd "$(dirname "$0")"
until [ "$(ls replies_htv_atria_retry | grep -c json)" -ge 5 ]; do sleep 30; done
echo "first rerun complete at $(date -u)"
set -a; . ../keys.env; set +a
export XEXAM_STREAM=1 XEXAM_ENDPOINT="https://api.atria-asi.ai/v1/chat/completions" XEXAM_MODEL="Atria-Dawn-Preview" XEXAM_KEY="$ATRIA_API_KEY" XEXAM_MAX_TOKENS=65536 XEXAM_TIMEOUT=2400
HTV=$(python3 -c "
import json,glob
ids=[json.load(open(p))['id'] for p in sorted(glob.glob('replies_htv_atria_retry/*.json')) if json.load(open(p)).get('error')]
print(','.join(i+':0' for i in ids))")
SC=$(python3 -c "
import json,glob
ids=[json.load(open(p))['id'] for p in sorted(glob.glob('replies_sc_atria/*.json')) if json.load(open(p)).get('error')]
print(','.join(i+':0' for i in ids))")
echo "hard-to-vary still failed: $HTV"; echo "story-critique still failed: $SC"
if [ -n "$HTV" ]; then XEXAM_ONLY="$HTV" XEXAM_SKILL_DIR=../skill_htv/hard-to-vary XEXAM_SKILL_FRAME=frame_htv.txt python3 cross_examine_skill.py battery_rev.json replies_htv_atria_retry2 --samples 1 --workers 1; fi
if [ -n "$SC" ]; then XEXAM_ONLY="$SC" XEXAM_SKILL_DIR=../skill_sc/story-critique XEXAM_SKILL_FRAME=frame_sc.txt python3 cross_examine_skill.py battery_rev.json replies_sc_atria_retry --samples 1 --workers 1; fi
echo "final reruns done at $(date -u)"
