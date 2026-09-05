#!/usr/bin/env python3
import json
import subprocess
import sys
from datetime import datetime

print("🎯 Fetching EXACT dates for all 290 videos...")
print("This will take ~10 minutes (fetching full metadata for each video)")
print()

# Load all video IDs
video_ids = []
with open('/tmp/all_uploads.jsonl', 'r') as f:
    for line in f:
        v = json.loads(line)
        video_ids.append(v['id'])

total = len(video_ids)
print(f"📊 Processing {total} videos...")
print()

results = []
errors = 0

for idx, vid_id in enumerate(video_ids):
    if (idx + 1) % 10 == 0 or idx == 0:
        progress = (idx + 1) / total * 100
        print(f"Progress: {idx + 1}/{total} ({progress:.1f}%) - Latest: {results[-1]['title'][:50] if results else '...'}")
    
    try:
        # Fetch full metadata
        cmd = [
            '/opt/homebrew/bin/yt-dlp',
            '--dump-json',
            '--no-warnings',
            f'https://www.youtube.com/watch?v={vid_id}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            results.append({
                'id': vid_id,
                'title': data.get('title', ''),
                'description': data.get('description', ''),
                'upload_date': data.get('upload_date', ''),
                'timestamp': data.get('timestamp', 0)
            })
        else:
            errors += 1
            print(f"  ⚠️  Failed to fetch {vid_id}")
            
    except Exception as e:
        errors += 1
        print(f"  ⚠️  Error on {vid_id}: {e}")
        continue

print()
print(f"✅ Successfully fetched {len(results)}/{total} videos")
if errors:
    print(f"⚠️  {errors} errors")

# Save results
with open('/tmp/videos_with_exact_dates.json', 'w') as f:
    json.dump(results, f, indent=2)

print()
print("💾 Saved to /tmp/videos_with_exact_dates.json")
