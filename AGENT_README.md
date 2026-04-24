# Continuous Feedback Processor

This system provides automatic, continuous processing of feedback items for the wellness-boosts-before-checkout-v2 prototype.

## System Architecture

The system consists of several components working together:

1. **continuous_agent.sh** - Main loop that runs forever
2. **process_one_item.py** - Checks for pending items and updates heartbeat
3. **helper_process_item.py** - Helper to mark items as done/error/review
4. **status_check.py** - Quick status check utility

## Current Status

- **Agent Status**: RUNNING ✅
- **Background Process ID**: See output of `ps aux | grep continuous_agent`
- **Log File**: `/private/tmp/claude-503/.../tasks/bdy7d7f8r.output`
- **Heartbeat Interval**: 15 seconds
- **State File**: `state.json`

## How It Works

### 1. Continuous Loop
The agent runs in the background, checking for pending feedback items every 15 seconds:
- Updates `last_agent_heartbeat` timestamp
- Checks for items with `status: "pending"`
- Processes oldest item first (sorted by `seq`)

### 2. Item Processing Flow
When a pending item is found:
1. Agent detects the item and marks it as "working"
2. Item is analyzed based on the message content
3. Claude agent uses Grep/Edit tools to make changes
4. Item is marked as "done", "error", or "needs_manual_review"

### 3. Processing Rules

**Remove requests** (`"remove this"` or `"remove [element]"`):
- Use Grep to find the component selector
- Use Edit to remove the HTML block
- Mark as `done`

**Figma URL references**:
- Mark as `needs_manual_review` with note "Requires Figma design implementation"

**Simple text changes**:
- Use Grep to find text
- Use Edit to replace
- Mark as `done`

**Complex style/layout changes**:
- Mark as `needs_manual_review` with descriptive note

## Commands

### Check Status
```bash
python3 status_check.py
```

### View Agent Log (live)
```bash
tail -f /private/tmp/claude-503/-Users-katreena-dalisay/1cb69a5c-3eca-4d95-8947-cf44760a2e93/tasks/bdy7d7f8r.output
```

### Manually Mark Item
```bash
python3 helper_process_item.py <item_id> <status> [message]
# Example:
python3 helper_process_item.py 1776955289417 done
python3 helper_process_item.py 1776955476907 needs_manual_review "Requires design system update"
```

### Stop Agent
```bash
ps aux | grep continuous_agent | grep -v grep | awk '{print $2}' | xargs kill
```

### Restart Agent
```bash
./continuous_agent.sh &
```

## Files

- `state.json` - Main state file with all feedback items
- `index.html` - Prototype HTML file
- `continuous_agent.sh` - Main agent loop script
- `process_one_item.py` - Item detection and heartbeat script
- `helper_process_item.py` - Helper to update item status
- `status_check.py` - Status checker utility
- `AGENT_README.md` - This file

## Monitoring

The agent maintains a heartbeat in `state.json`:
- `last_agent_heartbeat` - Updated every 15 seconds
- `last_agent_activity` - Updated when processing items

If the heartbeat is stale (>20 seconds old), the agent may have stopped.

## Current Statistics

Run `python3 status_check.py` to see:
- Total feedback items
- Pending/Working/Done/Review/Error counts
- Heartbeat status
- List of pending/working items

## Notes

- The agent runs indefinitely in the background
- All changes are written to `state.json` atomically
- The agent never stops unless manually killed
- Each feedback item is processed exactly once
- Items are processed in sequential order (by `seq` field)
