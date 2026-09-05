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

print("📥 Fetching 50 most recent videos...")

# Fetch just the 50 most recent videos with full metadata
cmd = [
    "/opt/homebrew/bin/yt-dlp",
    "--skip-download",
    "--dump-json",
    "--no-warnings",
    "--playlist-end", "50",
    "https://www.youtube.com/@NightSwimPod/videos"
]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
lines = result.stdout.strip().split('\n')

episodes = []
seen_ids = set()

for line in lines:
    if not line:
        continue
    
    try:
        video = json.loads(line)
        video_id = video.get('id')
        
        if not video_id or video_id in seen_ids:
            continue
        seen_ids.add(video_id)
        
        title = video.get('title', '')
        description = video.get('description', '')
        
        # Get upload date
        upload_date_str = video.get('upload_date')
        if upload_date_str and len(upload_date_str) == 8:
            publish_date = f"{upload_date_str[:4]}-{upload_date_str[4:6]}-{upload_date_str[6:8]}"
        else:
            timestamp = video.get('timestamp')
            if timestamp:
                publish_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            else:
                publish_date = "2024-01-01"
        
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

print(f"✅ Fetched {len(episodes)} videos")

# Sort by date (newest first)
episodes.sort(key=lambda x: x['publishDate'], reverse=True)

# Save
with open('src/data/episodes.json', 'w') as f:
    json.dump(episodes, f, indent=2)

print(f"💾 Saved to src/data/episodes.json")
print(f"\nDate range: {episodes[-1]['publishDate']} to {episodes[0]['publishDate']}")
print("\nNewest 10 episodes:")
for ep in episodes[:10]:
    print(f"  • {ep['publishDate']} - {ep['title']}")
