#!/usr/bin/env python3
import json
import subprocess
import re
from datetime import datetime

def create_episode_id(title):
    """Generate URL-safe ID from title"""
    id = re.sub(r'[^\w\s-]', '', title.lower())
    id = re.sub(r'[-\s]+', '-', id)
    return id[:70]

def categorize_episode(title, description=""):
    """Guess episode category from title/description"""
    text = (title + " " + description).lower()
    
    if any(word in text for word in ["hot take", "rant", "controversial", "exposes", "pissed", "goes off"]):
        return "hot-takes"
    elif any(word in text for word in ["interview", "joins", "talks", "conversation", "with"]):
        return "interviews"
    elif any(word in text for word in ["workout", "training", "drill", "technique", "speed"]):
        return "training"
    elif any(word in text for word in ["meet", "championship", "olympics", "world record", "trials", "games"]):
        return "events"
    else:
        return "news"

print("📥 Fetching ALL videos from YouTube channel WITH DATES...")
print("This will download full metadata for all 152 videos (slower but accurate)...")

# Fetch videos with FULL metadata (not flat-playlist)
cmd = [
    "/opt/homebrew/bin/yt-dlp",
    "--skip-download",
    "--dump-json",
    "--no-warnings",
    "--playlist-end", "200",  # Safety limit
    "https://www.youtube.com/@NightSwimPod/videos"
]

print("Running yt-dlp (this will take 2-3 minutes)...")
result = subprocess.run(cmd, capture_output=True, text=True)
lines = result.stdout.strip().split('\n')

episodes = []
seen_ids = set()

for i, line in enumerate(lines):
    if not line:
        continue
    
    if (i + 1) % 10 == 0:
        print(f"  Processing video {i+1}/{len(lines)}...")
    
    try:
        video = json.loads(line)
        video_id = video.get('id')
        
        if not video_id or video_id in seen_ids:
            continue
        seen_ids.add(video_id)
        
        title = video.get('title', '')
        description = video.get('description', '')
        
        # Get upload date from proper metadata
        upload_date_str = video.get('upload_date')
        if upload_date_str and len(upload_date_str) == 8:  # YYYYMMDD format
            publish_date = f"{upload_date_str[:4]}-{upload_date_str[4:6]}-{upload_date_str[6:8]}"
        else:
            # Fallback to timestamp if available
            timestamp = video.get('timestamp')
            if timestamp:
                publish_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            else:
                publish_date = "2024-01-01"  # ultimate fallback
        
        episode = {
            "id": create_episode_id(title),
            "title": title,
            "description": description[:500] if description else "",
            "youtubeId": video_id,
            "thumbnail": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            "publishDate": publish_date,
            "category": categorize_episode(title, description),
            "platforms": {
                "youtube": f"https://youtube.com/watch?v={video_id}",
                "spotify": "https://open.spotify.com/show/5jeYpru0iqfbtmhDg56IoI",
                "apple": "https://podcasts.apple.com/us/podcast/night-swim-podcast/id1853013593"
            }
        }
        
        episodes.append(episode)
        
    except json.JSONDecodeError:
        continue

print(f"✅ Fetched {len(episodes)} unique videos with dates")

# Sort by date (newest first)
episodes.sort(key=lambda x: x['publishDate'], reverse=True)

# Save
with open('src/data/episodes.json', 'w') as f:
    json.dump(episodes, f, indent=2)

print(f"💾 Saved to src/data/episodes.json")
print(f"\nDate range: {episodes[-1]['publishDate']} to {episodes[0]['publishDate']}")
print("\nNewest 5 episodes:")
for ep in episodes[:5]:
    print(f"  • {ep['publishDate']} - {ep['title'][:60]}")
print("\nOldest 5 episodes:")
for ep in episodes[-5:]:
    print(f"  • {ep['publishDate']} - {ep['title'][:60]}")
