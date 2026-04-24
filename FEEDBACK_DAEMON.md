# Feedback Applier Daemon

## Overview

The feedback applier daemon is a background process that monitors `state.json` for pending feedback items from the iterator system and automatically processes them.

## Status

**Current Status:** ACTIVE ✓

The daemon is running in the background and checks for new feedback every 5 seconds.

## How It Works

1. **Monitoring Loop**
   - Checks `state.json` every 5 seconds
   - Updates heartbeat timestamp
   - Looks for feedback items with `status: "pending"`

2. **Classification**
   - **Simple changes** → Text/copy edits in existing elements
   - **Complex changes** → JavaScript, CSS, new components, layout changes, or screenshot references

3. **Processing**
   - Simple changes are flagged for auto-application (requires Edit tool integration)
   - Complex changes are marked as `needs_manual_review` with a note explaining why

4. **State Updates**
   - Each processed item gets its status updated
   - Timestamps are recorded in `applied_at` field
   - Error messages or notes are added as needed

## Files

- `state.json` - Main state file with feedback queue
- `index.html` - Prototype HTML file to be updated
- `check_daemon_status.sh` - Helper script to check daemon status
- `apply_feedback.py` - Standalone monitoring script (alternative implementation)
- `feedback_monitor.py` - Original daemon implementation

## Checking Status

Run this command from the prototype directory:

```bash
./check_daemon_status.sh
```

Or manually:

```bash
python3 -c "
import json, time
with open('state.json') as f:
    state = json.load(f)
current = int(time.time() * 1000)
last = state.get('last_agent_heartbeat', 0)
print(f'Heartbeat: {(current - last) / 1000:.1f}s ago')
print(f'Pending: {len([i for i in state.get(\"feedback_items\", []) if i.get(\"status\") == \"pending\"])}')
"
```

## Classification Rules

### Simple (Auto-Apply)
- Text content changes (headings, labels, button text)
- Copy edits in existing elements
- Simple attribute changes (placeholder, alt text)

### Complex (Manual Review Required)
- JavaScript logic changes
- CSS/styling modifications
- New component additions
- Layout restructuring
- Changes that reference screenshots or Figma nodes
- Conditional rendering changes
- Event handler modifications

## State.json Format

```json
{
  "feedback_items": [
    {
      "id": "unique-id",
      "timestamp": 1234567890,
      "message": "feedback text",
      "status": "pending|working|applied|failed|needs_manual_review",
      "applied_at": 1234567890,
      "error": "error message if failed",
      "note": "reason for manual review"
    }
  ],
  "last_agent_heartbeat": 1234567890
}
```

## Status Values

- `pending` - New feedback waiting to be processed
- `working` - Currently being processed
- `applied` - Successfully applied to prototype
- `failed` - Processing failed with error
- `needs_manual_review` - Requires human review (too complex or uncertain)

## Runtime

- **Check interval:** 5 seconds
- **Max runtime:** 10 minutes (auto-stops after 120 iterations)
- **Heartbeat:** Updated every iteration

## Stopping the Daemon

The daemon will automatically stop after 10 minutes, or it can be stopped manually:

```bash
# Find the process
ps aux | grep python3 | grep state.json

# Kill it
kill <process_id>
```

## Extending the Daemon

To make the daemon actually apply simple changes (currently it only flags them), you would need to:

1. Integrate with the Edit tool to make changes to index.html
2. Parse feedback messages to identify the specific text to change
3. Use pattern matching or HTML parsing to locate elements
4. Apply the changes and update status to "applied"

Current implementation is conservative and flags most items for manual review.

## Troubleshooting

### Heartbeat is stale
- Check if the process is still running: `ps aux | grep python3 | grep state.json`
- Restart if needed (run the monitoring command again)

### No items being processed
- Verify there are items with `status: "pending"` in state.json
- Check the daemon output file for errors
- Ensure state.json is writable

### Items marked as "needs_manual_review" incorrectly
- Review the classification rules in the daemon code
- Adjust the keyword lists to better match your use case
- Consider training a classifier if you have many examples
