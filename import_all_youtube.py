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

print("📥 Fetching ALL videos from YouTube channel...")
print("This will take 1-2 minutes for 291 videos...")

# Fetch all videos as JSON
cmd = [
    "/opt/homebrew/bin/yt-dlp",
    "--flat-playlist",
    "--dump-json",
    "--no-warnings",
    "https://www.youtube.com/channel/UCxKskf92IDxYWM4advqsWMQ/videos"
]

result = subprocess.run(cmd, capture_output=True, text=True)
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
        
        # Try to get upload date
        upload_date = video.get('upload_date', '')
        if upload_date and len(upload_date) == 8:  # YYYYMMDD format
            publish_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
        else:
            publish_date = "2024-01-01"  # fallback
        
        episode = {
            "id": create_episode_id(title),
            "title": title,
            "description": description[:500] if description else "",  # Truncate long descriptions
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

print(f"✅ Fetched {len(episodes)} unique videos")

# Sort by date (newest first)
episodes.sort(key=lambda x: x['publishDate'], reverse=True)

# Save
with open('src/data/episodes.json', 'w') as f:
    json.dump(episodes, f, indent=2)

print(f"💾 Saved to src/data/episodes.json")
print(f"\nDate range: {episodes[-1]['publishDate']} to {episodes[0]['publishDate']}")
print("\nSample episodes:")
for ep in episodes[:5]:
    print(f"  • {ep['publishDate']} - {ep['title'][:60]}")
