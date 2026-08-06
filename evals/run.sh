#!/usr/bin/env bash
# End-to-end routing eval. Builds a catalog per condition, routes every eval
# query through `claude -p`, and scores the results.
#
#   ./run.sh                    # both conditions, one run each
#   REPEAT=5 ./run.sh           # 5 runs per query, to surface flaky routing
#   PAR=4 ./run.sh              # limit concurrency
#   CONDITIONS="current" ./run.sh
#   WORK=./out ./run.sh         # keep artifacts instead of using a temp dir
#
# Costs one model call per query per condition per repeat (40 by default).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="${WORK:-$(mktemp -d)}"
REPEAT="${REPEAT:-1}"
PAR="${PAR:-8}"
read -ra CONDS <<< "${CONDITIONS:-current ablated}"

command -v claude >/dev/null || { echo "claude CLI not found on PATH" >&2; exit 1; }

mkdir -p "$WORK/run" "$WORK/out" "$WORK/clean"

for cond in "${CONDS[@]}"; do
  python3 "$HERE/harness.py" prompts "$cond" "$WORK/run"
done

: > "$WORK/jobs.txt"
for prompt in "$WORK"/run/*.prompt; do
  base="$(basename "$prompt" .prompt)"
  for r in $(seq 1 "$REPEAT"); do
    if [ "$REPEAT" -eq 1 ]; then echo "$base"; else echo "$base.rep$r"; fi
  done >> "$WORK/jobs.txt"
done

# $WORK/clean is an empty scratch dir. Run from there so the model sees only the
# catalog in the prompt -- a run from the repo would pick up CLAUDE.md and score
# the project instructions rather than the skill descriptions under test.
run_one() {
  local job="$1" prompt="${1%%.rep*}"
  cd "$WORK/clean"
  claude -p < "$WORK/run/$prompt.prompt" > "$WORK/out/$job.json" 2>"$WORK/out/$job.err" || true
}
export -f run_one
export WORK

echo "running $(wc -l < "$WORK/jobs.txt") calls (concurrency $PAR)..."
xargs -a "$WORK/jobs.txt" -P "$PAR" -I{} bash -c 'run_one "$@"' _ {} || true

echo
python3 "$HERE/harness.py" score "$WORK/out" "${CONDS[@]}"
echo
echo "artifacts: $WORK"
