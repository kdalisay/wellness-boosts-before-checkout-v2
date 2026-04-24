# Quick Reference Card

## One-Line Commands

### Status Check
```bash
python3 status_check.py
```

### Monitor Dashboard
```bash
./monitor.sh
```

### Watch Live
```bash
tail -f /private/tmp/claude-503/-Users-katreena-dalisay/1cb69a5c-3eca-4d95-8947-cf44760a2e93/tasks/bdy7d7f8r.output
```

### Mark Item Done
```bash
python3 helper_process_item.py <item_id> done
```

### Mark Item for Review
```bash
python3 helper_process_item.py <item_id> needs_manual_review "Reason"
```

### Stop Agent
```bash
ps aux | grep continuous_agent | grep -v grep | awk '{print $2}' | xargs kill
```

### Start Agent
```bash
./continuous_agent.sh &
```

## Files

| File | Purpose |
|------|---------|
| `state.json` | Feedback items and system state |
| `index.html` | Prototype HTML file |
| `continuous_agent.sh` | Main agent loop ⭐ |
| `process_one_item.py` | Item detector |
| `helper_process_item.py` | Status updater |
| `status_check.py` | Quick status |
| `monitor.sh` | Interactive monitor |

## Key Concepts

**Heartbeat**: Updated every 15 seconds in `state.json`  
**Pending**: New items waiting to be processed  
**Working**: Item currently being processed  
**Done**: Successfully processed items  
**Needs Review**: Items requiring manual attention  

## Processing Pattern

1. Item arrives → `status: "pending"`
2. Agent detects → Logs details
3. Process with tools → Grep, Edit
4. Mark complete → `status: "done"`
5. Continue loop → Next iteration

## Current Status

```
✅ RUNNING
Process ID: 28890
Iterations: 15+
Heartbeat: Every 15s
```
