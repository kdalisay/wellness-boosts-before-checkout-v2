#!/usr/bin/env python3
"""
Process a single feedback item and output instructions for Claude
Returns exit code 0 if no items, 1 if item needs processing
"""
import json
import time
import sys

STATE_FILE = '/Users/katreena.dalisay/Documents/spec-machine-prototypes/wellness-boosts-before-checkout-v2/state.json'

def main():
    # Read state
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)

    # Update heartbeat
    current_time = int(time.time() * 1000)
    state['last_agent_heartbeat'] = current_time
    state['last_agent_activity'] = current_time

    # Get pending items
    pending = [f for f in state['feedback'] if f.get('status') == 'pending']
    pending_sorted = sorted(pending, key=lambda x: x.get('seq', 0))

    # Save heartbeat
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

    if not pending_sorted:
        # No items to process
        done = len([f for f in state['feedback'] if f.get('status') == 'done'])
        print(f"✓ Heartbeat updated. No pending items. ({done} done)")
        return 0

    # We have a pending item
    item = pending_sorted[0]

    print(f"\n{'='*60}")
    print(f"🚨 PENDING ITEM FOUND")
    print(f"{'='*60}")
    print(f"ID: {item['id']}")
    print(f"Seq: {item.get('seq')}")
    print(f"Message: {item['message']}")
    print(f"Selector: {item.get('component', {}).get('selector', 'N/A')}")
    print(f"{'='*60}")

    # Output as JSON for Claude to parse
    output = {
        'has_pending': True,
        'item': item
    }

    print("\nJSON_OUTPUT_START")
    print(json.dumps(output, indent=2))
    print("JSON_OUTPUT_END")

    return 1  # Signal that processing is needed

if __name__ == '__main__':
    sys.exit(main())
