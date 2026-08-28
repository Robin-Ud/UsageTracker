#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$(mktemp -d /tmp/usage_tracker_test.XXXXXX)"
LOG_DIR="$TEST_DIR/logs"
mkdir -p "$LOG_DIR"

cp "$SCRIPT_DIR/usage_tracker.py" "$TEST_DIR/"
python -c "
import json
with open('$TEST_DIR/configs.json', 'w') as f:
    json.dump({'log_dir': '$LOG_DIR', 'top_n': 5, 'stale_days': 30}, f)
"

now=$(date +%s)
old=$((now - 40 * 86400))

printf '%s\tls\n%s\tls\n%s\tcd\n%s\tclaude\n' "$now" "$now" "$now" "$now" > "$LOG_DIR/cmd_log.tsv"
printf '%s\tSUPER+1\n%s\tSUPER+1\n%s\tSUPER+q\n' "$now" "$now" "$old" > "$LOG_DIR/bind_log.tsv"
printf '%s' "$old" > "$LOG_DIR/tracking_started"

echo "🧪 Teste — dados reais não serão tocados"
echo "   ($TEST_DIR)"
echo ""

python "$TEST_DIR/usage_tracker.py"
status=$?

echo ""
if [ $status -eq 0 ]; then
    echo "✅ Relatório gerado sem erro."
else
    echo "❌ Falhou com status $status."
fi

rm -rf "$TEST_DIR"
echo "🗑️  Limpo."

exit $status
