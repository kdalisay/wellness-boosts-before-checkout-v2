#!/bin/bash
# Continuous Feedback Processor
# Runs forever, checking for pending items every 15 seconds

echo "🤖 Continuous Feedback Processor Started"
echo "========================================"
echo "Working directory: $(pwd)"
echo "Interval: 15 seconds"
echo "========================================"
echo ""

iteration=0

while true; do
    ((iteration++))
    timestamp=$(date +"%H:%M:%S")

    echo -n "[$iteration] $timestamp "

    # Run the Python script to check for pending items
    python3 process_one_item.py
    exit_code=$?

    if [ $exit_code -eq 1 ]; then
        echo ""
        echo "⚠️  ITEM REQUIRES PROCESSING"
        echo "    Waiting for Claude agent to handle this item..."
        echo "    (Claude should use Grep/Edit tools to process the feedback)"
        echo ""
        # Wait longer when item needs processing
        sleep 30
    else
        # Normal heartbeat, wait 15 seconds
        sleep 15
    fi
done
