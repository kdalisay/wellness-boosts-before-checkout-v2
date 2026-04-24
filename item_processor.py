#!/usr/bin/env python3
"""
Item Processor - Checks for signal file and outputs processing instructions
This runs alongside the monitor and tells Claude what to do
"""
import json
import time
import os

STATE_FILE = '/Users/katreena.dalisay/Documents/spec-machine-prototypes/wellness-boosts-before-checkout-v2/state.json'
SIGNAL_FILE = '/Users/katreena.dalisay/Documents/spec-machine-prototypes/wellness-boosts-before-checkout-v2/processing_needed.json'
HTML_FILE = '/Users/katreena.dalisay/Documents/spec-machine-prototypes/wellness-boosts-before-checkout-v2/index.html'

print("🔧 Item Processor Started - Watching for signal file")
print("=" * 60)
print()

iteration = 0

while True:
    iteration += 1
    
    if os.path.exists(SIGNAL_FILE):
        try:
            # Read signal
            with open(SIGNAL_FILE, 'r') as f:
                signal = json.load(f)
            
            item = signal['item']
            
            print(f"\n{'='*60}")
            print(f"🚨 PROCESSING REQUIRED - Iteration {iteration}")
            print(f"{'='*60}")
            print(f"Item ID: {item['id']}")
            print(f"Sequence: {item.get('seq')}")
            print(f"Message: {item['message']}")
            print()
            
            # Analyze the request type
            msg = item['message'].lower()
            
            if 'figma' in msg and 'http' in msg:
                print("📋 TYPE: Figma URL reference")
                print("ACTION: Mark as 'needs_manual_review'")
                print("REASON: Requires Figma design implementation")
                
            elif 'remove' in msg:
                print("📋 TYPE: Remove element")
                print("ACTION: Use Grep to find, Edit to remove")
                selector = item.get('component', {}).get('selector', 'unknown')
                print(f"TARGET: {selector}")
                
            elif 'update' in msg or 'replace' in msg or 'change' in msg:
                print("📋 TYPE: Update/Replace content")
                print("ACTION: Use Grep to find, Edit to replace")
                
            else:
                print("📋 TYPE: Unknown/Complex")
                print("ACTION: Mark as 'needs_manual_review'")
            
            print()
            print("⏸️  Processor paused - waiting for Claude agent to handle this item")
            print("    Claude should now use Grep/Edit tools to process the item")
            print("    and mark it as 'done' or 'needs_manual_review'")
            print(f"{'='*60}\n")
            
            # Don't delete signal - let Claude delete it after processing
            # Just wait for it to be removed
            while os.path.exists(SIGNAL_FILE):
                time.sleep(2)
            
            print("✅ Signal file removed - item processed, resuming watch")
            
        except Exception as e:
            print(f"❌ Error processing signal: {e}")
            # Remove bad signal file
            if os.path.exists(SIGNAL_FILE):
                os.remove(SIGNAL_FILE)
    
    else:
        # No signal, just wait
        if iteration % 10 == 1:  # Print every 10 iterations (20 seconds)
            print(f"[{iteration}] {time.strftime('%H:%M:%S')} Waiting for signal file...")
    
    time.sleep(2)

