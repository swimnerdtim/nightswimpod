#!/usr/bin/env python3
"""
Update Night Swim website with latest YouTube episodes
Uses public YouTube Data API v3 (no OAuth needed)
"""
import json
import requests
from datetime import datetime

# YouTube Data API v3 - public access
API_KEY = "AIzaSyDGpAj-VpP4-6K7u6SzTfuXaZ2KJRWq_TE"  # Public API key
CHANNEL_HANDLE = "@NightSwimPodcast"  # Night Swim channel handle

def get_channel_id():
    """Get channel ID from handle"""
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": API_KEY,
        "q": CHANNEL_HANDLE,
        "part": "snippet",
        "type": "channel",
        "maxResults": 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    items = response.json().get('items', [])
    if items:
        return items[0]['snippet']['channelId']
    return None

def get_latest_videos(channel_id, max_results=20):
    """Fetch latest videos from Night Swim channel"""
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": API_KEY,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "maxResults": max_results,
        "type": "video"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_video_details(video_ids):
    """Get full details for video IDs (description, etc)"""
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "key": API_KEY,
        "id": ",".join(video_ids),
        "part": "snippet,contentDetails"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def categorize_episode(title, description):
    """Guess episode category from title/description"""
    text = (title + " " + description).lower()
    
    if any(word in text for word in ["hot take", "rant", "controversial", "exposes", "pissed"]):
        return "hot-takes"
    elif any(word in text for word in ["interview", "joins", "talks", "conversation"]):
        return "interviews"
    elif any(word in text for word in ["workout", "training", "drill", "technique", "speed"]):
        return "training"
    elif any(word in text for word in ["meet", "championship", "olympics", "world record", "trials"]):
        return "events"
    else:
        return "news"

def create_episode_id(title):
    """Generate URL-safe ID from title"""
    import re
    # Remove special chars, lowercase, replace spaces with hyphens
    id = re.sub(r'[^\w\s-]', '', title.lower())
    id = re.sub(r'[-\s]+', '-', id)
    return id[:70]  # Truncate to reasonable length

def main():
    print("🎬 Fetching latest Night Swim episodes...")
    
    # Get channel ID
    print("Looking up channel ID...")
    channel_id = get_channel_id()
    if not channel_id:
        print("❌ Could not find channel")
        return 1
    print(f"Channel ID: {channel_id}")
    
    # Get latest videos
    search_results = get_latest_videos(channel_id, 20)
    video_ids = [item['id']['videoId'] for item in search_results['items']]
    
    print(f"Found {len(video_ids)} videos")
    
    # Get full details
    video_details = get_video_details(video_ids)
    
    episodes = []
    for video in video_details['items']:
        snippet = video['snippet']
        video_id = video['id']
        
        title = snippet['title']
        description = snippet['description']
        published = snippet['publishedAt'][:10]  # YYYY-MM-DD
        
        episode = {
            "id": create_episode_id(title),
            "title": title,
            "description": description,
            "youtubeId": video_id,
            "thumbnail": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            "publishDate": published,
            "category": categorize_episode(title, description),
            "platforms": {
                "youtube": f"https://youtube.com/watch?v={video_id}",
                "spotify": "https://open.spotify.com/show/5jeYpru0iqfbtmhDg56IoI",
                "apple": "https://podcasts.apple.com/us/podcast/night-swim-podcast/id1853013593"
            }
        }
        
        episodes.append(episode)
        print(f"  • {published} - {title[:60]}...")
    
    # Save to episodes.json
    output_path = "src/data/episodes.json"
    with open(output_path, 'w') as f:
        json.dump(episodes, f, indent=2)
    
    print(f"\n✅ Updated {output_path} with {len(episodes)} episodes")
    print("\nNext steps:")
    print("  1. git add src/data/episodes.json")
    print("  2. git commit -m 'Update episodes'")
    print("  3. git push")
    print("  4. Site auto-deploys in ~2 minutes")

if __name__ == '__main__':
    main()
