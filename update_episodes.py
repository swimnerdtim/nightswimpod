#!/usr/bin/env python3
"""
Automatically fetch latest Night Swim videos from YouTube and update episodes.json
"""

import json
import requests
from datetime import datetime
import sys

# Configuration
API_KEY = "AIzaSyAkKB-g06QLBRoKU3I1BFD45evUNe8iYjQ"
CHANNEL_HANDLE = "@NightSwimPod"
EPISODES_FILE = "src/data/episodes.json"

def get_channel_id():
    """Get channel ID from handle"""
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': 'Night Swim Podcast Dax Hill Elvis Burrows',
        'type': 'channel',
        'maxResults': 1,
        'key': API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'items' in data and len(data['items']) > 0:
        return data['items'][0]['snippet']['channelId']
    return None

def get_channel_videos(channel_id, max_results=50):
    """Fetch latest videos from the channel"""
    # First get the uploads playlist ID
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        'part': 'contentDetails',
        'id': channel_id,
        'key': API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'items' not in data or len(data['items']) == 0:
        print("❌ Could not find channel uploads playlist")
        return []
    
    uploads_playlist = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    # Now get videos from uploads playlist
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        'part': 'snippet',
        'playlistId': uploads_playlist,
        'maxResults': max_results,
        'key': API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'items' not in data:
        print("❌ No videos found")
        return []
    
    return data['items']

def categorize_video(title, description):
    """Auto-categorize video based on title/description"""
    title_lower = title.lower()
    desc_lower = description.lower()
    
    if any(word in title_lower for word in ['interview', 'joins', 'with', 'ft.']):
        return 'interviews'
    elif any(word in title_lower for word in ['ncaa', 'olympics', 'championship', 'meet', 'sec', 'acc', 'big ten']):
        return 'events'
    elif any(word in title_lower for word in ['hot take', 'controversial', 'debate', 'opinion']):
        return 'hot-takes'
    elif any(word in title_lower for word in ['training', 'practice', 'technique', 'workout']):
        return 'training'
    elif any(word in title_lower for word in ['news', 'breaking', 'announcement']):
        return 'news'
    else:
        return 'interviews'  # Default

def create_episode_id(title):
    """Create URL-friendly ID from title"""
    import re
    # Remove special characters, lowercase, replace spaces with hyphens
    id_str = title.lower()
    id_str = re.sub(r'[^\w\s-]', '', id_str)
    id_str = re.sub(r'[-\s]+', '-', id_str)
    return id_str[:60]  # Limit length

def video_to_episode(video_item):
    """Convert YouTube video to episode format"""
    snippet = video_item['snippet']
    video_id = snippet['resourceId']['videoId']
    
    # Parse publish date
    published = snippet['publishedAt']
    date_obj = datetime.strptime(published, '%Y-%m-%dT%H:%M:%SZ')
    publish_date = date_obj.strftime('%Y-%m-%d')
    
    title = snippet['title']
    description = snippet['description']
    
    # Truncate description if too long
    if len(description) > 200:
        description = description[:197] + "..."
    
    return {
        "id": create_episode_id(title),
        "title": title,
        "description": description,
        "youtubeId": video_id,
        "thumbnail": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        "publishDate": publish_date,
        "category": categorize_video(title, description),
        "platforms": {
            "youtube": f"https://www.youtube.com/watch?v={video_id}",
            "spotify": "https://open.spotify.com/show/5jeYpru0iqfbtmhDg56IoI",
            "apple": "https://podcasts.apple.com/us/podcast/night-swim-podcast/id1853013593"
        }
    }

def update_episodes():
    """Main function to update episodes.json"""
    print("🏊 Fetching Night Swim videos from YouTube...")
    
    # Get channel ID
    print("   Finding channel...")
    channel_id = get_channel_id()
    if not channel_id:
        print("❌ Could not find Night Swim channel")
        return False
    
    print(f"   ✅ Channel ID: {channel_id}")
    
    # Get videos
    print("   Fetching videos...")
    videos = get_channel_videos(channel_id, max_results=50)
    print(f"   ✅ Found {len(videos)} videos")
    
    # Convert to episodes
    new_episodes = [video_to_episode(v) for v in videos]
    
    # Load existing episodes
    try:
        with open(EPISODES_FILE, 'r') as f:
            existing_episodes = json.load(f)
        print(f"   📝 Loaded {len(existing_episodes)} existing episodes")
    except FileNotFoundError:
        existing_episodes = []
        print("   📝 No existing episodes file")
    
    # Merge (keep existing if ID matches, add new ones)
    existing_ids = {ep['id'] for ep in existing_episodes}
    episodes_dict = {ep['id']: ep for ep in existing_episodes}
    
    added_count = 0
    for new_ep in new_episodes:
        if new_ep['id'] not in existing_ids:
            episodes_dict[new_ep['id']] = new_ep
            added_count += 1
    
    # Sort by publish date (newest first)
    all_episodes = sorted(
        episodes_dict.values(),
        key=lambda x: x['publishDate'],
        reverse=True
    )
    
    # Write back to file
    with open(EPISODES_FILE, 'w') as f:
        json.dump(all_episodes, f, indent=2)
    
    print(f"\n✅ Updated episodes.json!")
    print(f"   Total episodes: {len(all_episodes)}")
    print(f"   New episodes added: {added_count}")
    
    if added_count > 0:
        print(f"\n📺 New episodes:")
        for ep in sorted(all_episodes, key=lambda x: x['publishDate'], reverse=True)[:added_count]:
            print(f"   • {ep['publishDate']}: {ep['title']}")
    
    return True

if __name__ == '__main__':
    success = update_episodes()
    sys.exit(0 if success else 1)
