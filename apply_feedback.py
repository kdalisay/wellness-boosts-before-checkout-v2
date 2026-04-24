#!/usr/bin/env python3
"""
Feedback Applier - Monitors and processes feedback items from state.json
This script continuously monitors for pending feedback and outputs commands
that the Claude agent can execute.
"""

import json
import time
import sys
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state.json"
INDEX_FILE = Path(__file__).parent / "index.html"
CHECK_INTERVAL = 5

def read_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        return None

def write_state(state):
    try:
        # Write atomically using temp file
        temp_file = STATE_FILE.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(state, f, indent=2)
        temp_file.replace(STATE_FILE)
        return True
    except Exception as e:
        print(f"ERROR_WRITE: {e}", file=sys.stderr)
        return False

def update_heartbeat(state):
    state['last_agent_heartbeat'] = int(time.time())
    return state

def get_pending_items(state):
    return [item for item in state.get('feedback_items', [])
            if item.get('status') == 'pending']

def classify_feedback(message):
    """
    Classify feedback as simple or complex.
    Returns: ('simple', confidence) or ('complex', reason)
    """
    msg_lower = message.lower()

    # Complex indicators
    complex_indicators = {
        'javascript': 'requires JS changes',
        'css': 'requires CSS changes',
        'style': 'requires styling changes',
        'component': 'requires component changes',
        'layout': 'requires layout changes',
        'add new': 'requires adding new elements',
        'create': 'requires creating new elements',
        'screenshot': 'references screenshot',
        'figma': 'references Figma',
        'function': 'requires function changes',
        'onclick': 'requires event handler',
        'conditional': 'requires conditional logic',
    }

    for indicator, reason in complex_indicators.items():
        if indicator in msg_lower:
            return ('complex', reason)

    # Simple indicators
    simple_indicators = [
        'change text', 'update text', 'change copy', 'update copy',
        'change label', 'change heading', 'change button text',
        'replace text', 'text should say', 'copy should say',
        'heading should', 'label should', 'button should say'
    ]

    for indicator in simple_indicators:
        if indicator in msg_lower:
            return ('simple', f'matches pattern: {indicator}')

    # Default to complex if unsure
    return ('complex', 'unclear classification - defaulting to manual review')

def main():
    iteration = 0

    while True:
        iteration += 1

        # Read state
        state = read_state()
        if state is None:
            time.sleep(CHECK_INTERVAL)
            continue

        # Update heartbeat
        state = update_heartbeat(state)

        # Get pending items
        pending = get_pending_items(state)

        # Output status
        print(f"ITERATION:{iteration}|PENDING:{len(pending)}")

        # Process first pending item
        if pending:
            item = pending[0]
            item_id = item['id']
            message = item['message']

            classification, info = classify_feedback(message)

            print(f"ITEM:{item_id}")
            print(f"MESSAGE:{message[:200]}")
            print(f"CLASSIFICATION:{classification}")
            print(f"INFO:{info}")

            # Mark as working
            for i in state['feedback_items']:
                if i['id'] == item_id:
                    i['status'] = 'working'
                    break

            # Output command for agent to execute
            if classification == 'simple':
                print(f"ACTION:APPLY_SIMPLE")
            else:
                print(f"ACTION:MANUAL_REVIEW")
                # Mark as needs manual review
                for i in state['feedback_items']:
                    if i['id'] == item_id:
                        i['status'] = 'needs_manual_review'
                        i['note'] = info
                        i['applied_at'] = int(time.time())
                        break

        # Write state
        write_state(state)

        # Wait
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
