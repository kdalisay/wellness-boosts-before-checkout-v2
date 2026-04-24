#!/usr/bin/env python3
"""Quick status check of the feedback system"""
import json
import time

STATE_FILE = '/Users/katreena.dalisay/Documents/spec-machine-prototypes/wellness-boosts-before-checkout-v2/state.json'

with open(STATE_FILE, 'r') as f:
    state = json.load(f)

current_time = int(time.time() * 1000)
last_heartbeat = state.get('last_agent_heartbeat', 0)
time_diff = (current_time - last_heartbeat) / 1000

# Count statuses
pending = [f for f in state['feedback'] if f.get('status') == 'pending']
working = [f for f in state['feedback'] if f.get('status') == 'working']
done = [f for f in state['feedback'] if f.get('status') == 'done']
review = [f for f in state['feedback'] if f.get('status') == 'needs_manual_review']
error = [f for f in state['feedback'] if f.get('status') == 'error']

print("📊 Feedback System Status")
print("=" * 60)
print(f"Total items: {len(state['feedback'])}")
print(f"  Pending: {len(pending)}")
print(f"  Working: {len(working)}")
print(f"  Done: {len(done)}")
print(f"  Needs Review: {len(review)}")
print(f"  Error: {len(error)}")
print()
print(f"Last heartbeat: {time_diff:.1f}s ago", end='')
if time_diff < 20:
    print(" ✅ ALIVE")
else:
    print(" ⚠️  STALE")
print()

if pending:
    print("Pending items:")
    for item in sorted(pending, key=lambda x: x.get('seq', 0))[:5]:
        print(f"  - seq {item.get('seq')}: {item['message'][:70]}")

if working:
    print("\nWorking items:")
    for item in working[:5]:
        print(f"  - seq {item.get('seq')}: {item['message'][:70]}")
