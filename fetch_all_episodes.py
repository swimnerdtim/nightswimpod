#!/usr/bin/env python3
"""
Fetch ALL episodes from Night Swim YouTube channel using RSS + pagination fallback
"""
import json
import re
import xml.etree.ElementTree as ET
import requests
from datetime import datetime

# Night Swim YouTube channel ID
CHANNEL_ID = "UCxKskf92IDxYWM4advqsWMQ"
RSS_FEED = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

def fetch_rss():
    """Fetch RSS feed (gets latest 15 only)"""
    response = requests.get(RSS_FEED)
    response.raise_for_status()
    return response.text

def parse_rss(rss_xml):
    """Parse RSS XML and extract video data"""
    root = ET.fromstring(rss_xml)
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'media': 'http://search.yahoo.com/mrss/',
        'yt': 'http://www.youtube.com/xml/schemas/2015'
    }
    
    episodes = []
    
    for entry in root.findall('atom:entry', ns):
        video_id = entry.find('yt:videoId', ns).text
        title = entry.find('atom:title', ns).text
        published = entry.find('atom:published', ns).text[:10]
        
        media_group = entry.find('media:group', ns)
        description = ""
        if media_group is not None:
            desc_elem = media_group.find('media:description', ns)
            if desc_elem is not None:
                description = desc_elem.text or ""
        
        episodes.append({
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
        })
    
    return episodes

def fetch_from_channel_page():
    """Scrape channel page to get all video IDs"""
    url = f"https://www.youtube.com/@NightSwimPodcast/videos"
    
    # This is a backup approach - we'd need to use something like yt-dlp
    # For now, let's use a simpler approach
    print("Note: RSS only provides last 15 videos")
    print("For full archive, we need to:")
    print("1. Use yt-dlp to extract all video IDs")
    print("2. Or manually export from YouTube Studio")
    print("3. Or use YouTube Data API with proper credentials")
    return []

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
    id = re.sub(r'[^\w\s-]', '', title.lower())
    id = re.sub(r'[-\s]+', '-', id)
    return id[:70]

def main():
    print("🎬 Attempting to fetch ALL Night Swim episodes...")
    print(f"Channel: @NightSwimPodcast (ID: {CHANNEL_ID})")
    print()
    
    # Get latest from RSS
    print("Fetching from RSS (last 15)...")
    rss_xml = fetch_rss()
    rss_episodes = parse_rss(rss_xml)
    print(f"✅ Got {len(rss_episodes)} episodes from RSS")
    
    # Load existing archive
    try:
        with open('src/data/episodes.json', 'r') as f:
            existing = json.load(f)
        print(f"📁 Current archive has {len(existing)} episodes")
    except:
        existing = []
        print("📁 No existing archive found")
    
    # We need a better approach for all 291 videos
    print()
    print("⚠️  RSS only provides last 15 videos")
    print("To get all 291 videos, we need to:")
    print()
    print("Option 1: Use yt-dlp")
    print("  yt-dlp --flat-playlist --print-json 'https://www.youtube.com/@NightSwimPodcast/videos'")
    print()
    print("Option 2: YouTube Data API (if we have valid key)")
    print()
    print("Option 3: Manual export from YouTube Studio")
    print()
    print("Which approach should I use?")

if __name__ == '__main__':
    main()
