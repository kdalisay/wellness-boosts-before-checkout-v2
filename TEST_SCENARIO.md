# Test Scenario: Processing a Pending Item

## What Happens When a New Feedback Item Arrives

### Step 1: User Submits Feedback
A user clicks feedback in the UI, creating a new item in `state.json`:
```json
{
  "id": "1776960000000",
  "seq": 86,
  "message": "remove the wellness tips section",
  "status": "pending",
  "timestamp": "2026-04-23T14:00:00.000Z"
}
```

### Step 2: Agent Detects Item (within 15 seconds)
The continuous agent's next iteration finds the pending item:
```
[N] 13:15:03 
============================================================
🚨 PENDING ITEM FOUND
============================================================
ID: 1776960000000
Seq: 86
Message: remove the wellness tips section
Selector: section.wellness-tips
============================================================

JSON_OUTPUT_START
{
  "has_pending": true,
  "item": {
    "id": "1776960000000",
    "seq": 86,
    "message": "remove the wellness tips section",
    ...
  }
}
JSON_OUTPUT_END

⚠️  ITEM REQUIRES PROCESSING
    Waiting for Claude agent to handle this item...
```

### Step 3: Claude Agent Processes Item

#### For "remove" requests:
```bash
# 1. Find the element
grep -n "wellness-tips" index.html

# 2. Remove the section using Edit tool
# (Remove the entire <section class="wellness-tips">...</section> block)

# 3. Mark as done
python3 helper_process_item.py 1776960000000 done
```

#### For Figma URL requests:
```bash
python3 helper_process_item.py 1776960000000 needs_manual_review "Requires Figma design implementation"
```

#### For text changes:
```bash
# 1. Find the text
grep -n "old text" index.html

# 2. Replace using Edit tool
# (Replace "old text" with "new text")

# 3. Mark as done
python3 helper_process_item.py 1776960000000 done
```

### Step 4: Agent Continues
After processing, the item status changes from "pending" → "done", and the agent continues its normal loop:
```
[N+1] 13:15:33 ✓ Heartbeat updated. No pending items. (69 done)
```

## Manual Testing

To manually test the system:

### 1. Add a test item to state.json:
```python
python3 << 'EOF'
import json
import time

with open('state.json', 'r') as f:
    state = json.load(f)

test_item = {
    "id": str(int(time.time() * 1000)),
    "seq": len(state['feedback']) + 1,
    "message": "TEST: remove the test section",
    "status": "pending",
    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
}

state['feedback'].append(test_item)

with open('state.json', 'w') as f:
    json.dump(state, f, indent=2)

print(f"Added test item: {test_item['id']}")
EOF
```

### 2. Watch the agent log:
```bash
tail -f /private/tmp/claude-503/.../tasks/bdy7d7f8r.output
```

### 3. Process the item manually:
```bash
# After agent detects it, mark as done
python3 helper_process_item.py <item_id> done
```

### 4. Verify:
```bash
python3 status_check.py
```

## Processing Patterns

### Pattern 1: Simple Removal
**Message**: "remove this", "remove [element]"
**Action**: Grep → Edit → Mark done

### Pattern 2: Figma Reference
**Message**: Contains "figma.com" URL
**Action**: Mark as needs_manual_review immediately

### Pattern 3: Text Replacement
**Message**: "change X to Y", "update text"
**Action**: Grep → Edit → Mark done

### Pattern 4: Complex Changes
**Message**: Layout changes, style modifications
**Action**: Mark as needs_manual_review with description

## Error Handling

If processing fails:
```bash
python3 helper_process_item.py <item_id> error "Description of what went wrong"
```

The item will be marked with status "error" and the error message will be stored.
