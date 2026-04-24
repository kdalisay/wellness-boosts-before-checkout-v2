#!/usr/bin/env python3
"""
Feedback Monitor Daemon
Continuously monitors state.json for pending feedback items and processes them.
"""

import json
import time
import sys
import re
from pathlib import Path

# Configuration
STATE_FILE = Path(__file__).parent / "state.json"
INDEX_FILE = Path(__file__).parent / "index.html"
CHECK_INTERVAL = 5  # seconds

def read_state():
    """Read the current state from state.json."""
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading state.json: {e}", file=sys.stderr)
        return None

def write_state(state):
    """Write updated state to state.json."""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        return True
    except Exception as e:
        print(f"Error writing state.json: {e}", file=sys.stderr)
        return False

def update_heartbeat(state):
    """Update the last_agent_heartbeat timestamp."""
    state['last_agent_heartbeat'] = int(time.time())
    return state

def update_item_status(state, item_id, status, **kwargs):
    """Update the status of a feedback item."""
    for item in state.get('feedback_items', []):
        if item.get('id') == item_id:
            item['status'] = status
            if status in ['applied', 'failed', 'needs_manual_review']:
                item['applied_at'] = int(time.time())
            for key, value in kwargs.items():
                item[key] = value
            break
    return state

def is_simple_text_change(feedback):
    """
    Determine if feedback is a simple text/copy change.

    Simple changes are things like:
    - Changing button text
    - Updating headings
    - Modifying labels
    - Editing placeholder text
    """
    # Keywords that indicate complex changes
    complex_keywords = [
        'javascript', 'js', 'function', 'event', 'onclick', 'handler',
        'css', 'style', 'color', 'layout', 'position', 'flex', 'grid',
        'component', 'add', 'create', 'new', 'implement',
        'screenshot', 'figma', 'design',
        'conditional', 'if', 'logic', 'render'
    ]

    feedback_lower = feedback.lower()

    # Check for complex keywords
    for keyword in complex_keywords:
        if keyword in feedback_lower:
            return False

    # Keywords that indicate simple text changes
    simple_keywords = [
        'change text', 'update text', 'change copy', 'update copy',
        'change label', 'change heading', 'change button',
        'text should', 'copy should', 'label should',
        'replace text', 'update heading'
    ]

    for keyword in simple_keywords:
        if keyword in feedback_lower:
            return True

    # If unsure, be conservative and flag for manual review
    return False

def get_pending_items(state):
    """Get all pending feedback items."""
    return [item for item in state.get('feedback_items', [])
            if item.get('status') == 'pending']

def process_feedback_item(state, item):
    """
    Process a single feedback item.
    Returns updated state.
    """
    item_id = item.get('id')
    message = item.get('message', '')

    print(f"\nProcessing item {item_id}")
    print(f"Message: {message[:100]}...")

    # Mark as working
    state = update_item_status(state, item_id, 'working')
    write_state(state)

    # Determine if simple or complex
    if is_simple_text_change(message):
        print(f"  -> Classified as SIMPLE text change")
        # For now, mark as needs_manual_review since we can't directly apply edits
        # In a real implementation, this would call the Edit tool
        state = update_item_status(
            state,
            item_id,
            'needs_manual_review',
            note='Simple text change - requires Edit tool integration'
        )
    else:
        print(f"  -> Classified as COMPLEX change")
        state = update_item_status(
            state,
            item_id,
            'needs_manual_review',
            note='Complex change requiring manual review'
        )

    return state

def main():
    """Main monitoring loop."""
    print("=" * 60)
    print("Feedback Monitor Daemon Started")
    print(f"Monitoring: {STATE_FILE}")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    print("=" * 60)

    iteration = 0

    while True:
        iteration += 1
        print(f"\n[Iteration {iteration}] Checking for pending items...")

        # Read current state
        state = read_state()
        if state is None:
            print("  -> Failed to read state, waiting before retry...")
            time.sleep(CHECK_INTERVAL)
            continue

        # Update heartbeat
        state = update_heartbeat(state)

        # Get pending items
        pending_items = get_pending_items(state)
        print(f"  -> Found {len(pending_items)} pending item(s)")

        # Process each pending item
        for item in pending_items:
            state = process_feedback_item(state, item)
            write_state(state)

        # Write final state with updated heartbeat
        write_state(state)

        # Wait before next check
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDaemon stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nFatal error: {e}", file=sys.stderr)
        sys.exit(1)
