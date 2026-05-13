#!/usr/bin/env python3
"""
Update Night Swim website with latest YouTube episodes
Uses YouTube RSS feed (no API key needed)
"""
import json
import re
import xml.etree.ElementTree as ET
import requests
from datetime import datetime

# Night Swim YouTube RSS feed
# Channel ID: UCxKskf92IDxYWM4advqsWMQ
RSS_FEED = "https://www.youtube.com/feeds/videos.xml?channel_id=UCxKskf92IDxYWM4advqsWMQ"

def fetch_rss():
    """Fetch RSS feed"""
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
        published = entry.find('atom:published', ns).text[:10]  # YYYY-MM-DD
        
        # Get description from media:group
        media_group = entry.find('media:group', ns)
        description = ""
        if media_group is not None:
            desc_elem = media_group.find('media:description', ns)
            if desc_elem is not None:
                description = desc_elem.text or ""
        
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
    
    return episodes

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
    # Remove special chars, lowercase, replace spaces with hyphens
    id = re.sub(r'[^\w\s-]', '', title.lower())
    id = re.sub(r'[-\s]+', '-', id)
    return id[:70]  # Truncate to reasonable length

def main():
    print("🎬 Fetching latest Night Swim episodes from RSS...")
    
    # Fetch RSS
    rss_xml = fetch_rss()
    print("✅ RSS fetched")
    
    # Parse episodes
    episodes = parse_rss(rss_xml)
    print(f"Found {len(episodes)} videos")
    
    for ep in episodes:
        print(f"  • {ep['publishDate']} - {ep['title'][:60]}...")
    
    # Save to episodes.json
    output_path = "src/data/episodes.json"
    with open(output_path, 'w') as f:
        json.dump(episodes, f, indent=2)
    
    print(f"\n✅ Updated {output_path} with {len(episodes)} episodes")
    print("\nNext steps:")
    print("  1. git add src/data/episodes.json")
    print("  2. git commit -m 'Update episodes from YouTube RSS'")
    print("  3. git push")
    print("  4. Site auto-deploys in ~2 minutes")

if __name__ == '__main__':
    main()
