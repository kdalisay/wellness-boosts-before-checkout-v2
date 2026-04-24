#!/usr/bin/env python3
"""
Helper script to mark an item with a specific status and message
Usage: python3 helper_process_item.py <item_id> <status> [error_message]
"""
import json
import sys
import time

STATE_FILE = '/Users/katreena.dalisay/Documents/spec-machine-prototypes/wellness-boosts-before-checkout-v2/state.json'

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 helper_process_item.py <item_id> <status> [error_message]")
        print("Status can be: done, error, needs_manual_review, working")
        return 1

    item_id = sys.argv[1]
    status = sys.argv[2]
    error_msg = sys.argv[3] if len(sys.argv) > 3 else None

    # Read state
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)

    # Find and update item
    found = False
    for item in state['feedback']:
        if item['id'] == item_id:
            item['status'] = status
            item['updated_at'] = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
            if error_msg:
                item['error_message'] = error_msg
            found = True
            print(f"✓ Updated item {item_id} to status '{status}'")
            if error_msg:
                print(f"  Message: {error_msg}")
            break

    if not found:
        print(f"❌ Item {item_id} not found")
        return 1

    # Save state
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

    return 0

if __name__ == '__main__':
    sys.exit(main())
