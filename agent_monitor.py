#!/usr/bin/env python3
"""
Continuous Feedback Processor Monitor
Runs forever, checking for pending items every 15 seconds
"""
import json
import time
import sys
import os

STATE_FILE = '/Users/katreena.dalisay/Documents/spec-machine-prototypes/wellness-boosts-before-checkout-v2/state.json'
SIGNAL_FILE = '/Users/katreena.dalisay/Documents/spec-machine-prototypes/wellness-boosts-before-checkout-v2/processing_needed.json'

print("🤖 Continuous Feedback Processor Monitor Started")
print("=" * 60)
print(f"State file: {STATE_FILE}")
print(f"Signal file: {SIGNAL_FILE}")
print(f"Loop interval: 15 seconds")
print("=" * 60)
print()

iteration = 0

while True:
    iteration += 1
    current_time = int(time.time() * 1000)
    
    print(f"[{iteration}] {time.strftime('%H:%M:%S')} ", end='')
    sys.stdout.flush()
    
    try:
        # Read current state
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
        
        # Update heartbeat
        state['last_agent_heartbeat'] = current_time
        state['last_agent_activity'] = current_time
        
        # Get pending items
        pending = [f for f in state['feedback'] if f.get('status') == 'pending']
        pending_sorted = sorted(pending, key=lambda x: x.get('seq', 0))
        
        working_count = len([f for f in state['feedback'] if f.get('status') == 'working'])
        done_count = len([f for f in state['feedback'] if f.get('status') == 'done'])
        
        print(f"P:{len(pending)} W:{working_count} D:{done_count} ", end='')
        
        # Process pending item if exists
        if pending_sorted:
            item = pending_sorted[0]
            print(f"🔧 FOUND seq={item.get('seq')}")
            
            # Mark as working
            for f in state['feedback']:
                if f['id'] == item['id']:
                    f['status'] = 'working'
                    f['updated_at'] = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
                    break
            
            # Save state
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f, indent=2)
            
            # Create signal file for Claude agent
            with open(SIGNAL_FILE, 'w') as f:
                json.dump({
                    'item': item,
                    'timestamp': current_time,
                    'action': 'process_now'
                }, f, indent=2)
            
            print(f"      📝 Item details: {item['message'][:60]}...")
            print(f"      🚨 Signal file created for Claude agent")
            
        else:
            # Just save heartbeat
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f, indent=2)
            print("✓")
        
        sys.stdout.flush()
        
    except Exception as e:
        print(f"❌ {e}")
        sys.stdout.flush()
    
    # Wait 15 seconds
    time.sleep(15)

