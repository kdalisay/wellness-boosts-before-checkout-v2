#!/bin/bash
# Check the status of the feedback applier daemon

cd "$(dirname "$0")"

python3 << 'EOF'
import json
import time

with open('state.json', 'r') as f:
    state = json.load(f)

current_ms = int(time.time() * 1000)
last_heartbeat = state.get('last_agent_heartbeat', 0)
seconds_ago = (current_ms - last_heartbeat) / 1000

print('=== FEEDBACK APPLIER DAEMON STATUS ===')
print()

if seconds_ago < 10:
    print(f'✓ Status: ACTIVE (heartbeat {seconds_ago:.1f}s ago)')
elif seconds_ago < 60:
    print(f'⚠ Status: POSSIBLY STALE (heartbeat {seconds_ago:.1f}s ago)')
else:
    print(f'✗ Status: INACTIVE (last heartbeat {seconds_ago:.0f}s ago)')

print()
print('=== FEEDBACK QUEUE ===')

feedback_items = state.get('feedback_items', [])
print(f'Total items: {len(feedback_items)}')

statuses = {}
for item in feedback_items:
    status = item.get('status', 'unknown')
    statuses[status] = statuses.get(status, 0) + 1

if statuses:
    for status, count in sorted(statuses.items()):
        print(f'  {status}: {count}')
else:
    print('  (no items in queue)')

# Show first pending item if exists
pending = [i for i in feedback_items if i.get('status') == 'pending']
if pending:
    print()
    print('=== NEXT PENDING ITEM ===')
    item = pending[0]
    print(f'ID: {item["id"]}')
    print(f'Message: {item["message"][:150]}...')
    print(f'Timestamp: {item.get("timestamp")}')

EOF

echo ""
echo "To view full state.json: cat state.json | python3 -m json.tool | less"
