#!/bin/bash
# Interactive monitor for the continuous feedback processor

LOG_FILE="/private/tmp/claude-503/-Users-katreena-dalisay/1cb69a5c-3eca-4d95-8947-cf44760a2e93/tasks/bdy7d7f8r.output"

echo "🔍 Continuous Feedback Processor Monitor"
echo "========================================"
echo ""

# Check if agent is running
if ps aux | grep -v grep | grep continuous_agent.sh > /dev/null; then
    echo "✅ Agent is RUNNING"
    ps aux | grep -v grep | grep continuous_agent.sh | head -1
else
    echo "❌ Agent is NOT RUNNING"
    echo ""
    echo "To start: ./continuous_agent.sh &"
    exit 1
fi

echo ""

# Show current status
python3 status_check.py

echo ""
echo "========================================"
echo "Recent Activity (last 10 lines):"
echo "========================================"
tail -10 "$LOG_FILE"

echo ""
echo "========================================"
echo "Options:"
echo "  1. Watch live log:     tail -f $LOG_FILE"
echo "  2. Check status:       python3 status_check.py"
echo "  3. Stop agent:         ps aux | grep continuous_agent | grep -v grep | awk '{print \$2}' | xargs kill"
echo "========================================"
