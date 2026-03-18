#!/usr/bin/env python3
"""
Parse RSS feed and update episodes.json with episode-specific podcast URLs
"""

import json
import requests
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher

RSS_FEED_URL = "https://anchor.fm/s/10b7e163c/podcast/rss"

def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def fetch_rss_episodes():
    """Fetch all episodes from RSS feed"""
    response = requests.get(RSS_FEED_URL)
    response.raise_for_status()
    
    root = ET.fromstring(response.content)
    
    episodes_from_rss = []
    
    for item in root.findall('.//item'):
        title = item.find('title').text if item.find('title') is not None else ""
        link = item.find('link').text if item.find('link') is not None else ""
        guid = item.find('guid').text if item.find('guid') is not None else ""
        
        # Extract Spotify episode URL from the podcasters.spotify.com link
        # Format: https://podcasters.spotify.com/pod/show/nightswimpod/episodes/{slug}
        if 'episodes/' in link:
            slug = link.split('/episodes/')[-1]
            # Convert to public Spotify URL
            spotify_url = f"https://open.spotify.com/episode/{guid}" if guid else None
        else:
            spotify_url = None
        
        episodes_from_rss.append({
            'title': title,
            'link': link,
            'guid': guid,
            'spotify_url': spotify_url
        })
    
    return episodes_from_rss

def update_episodes_json():
    """Update episodes.json with episode-specific podcast URLs"""
    
    print("📻 Fetching RSS feed...")
    rss_episodes = fetch_rss_episodes()
    print(f"Found {len(rss_episodes)} episodes in RSS feed")
    
    # Load current episodes.json
    with open('src/data/episodes.json', 'r') as f:
        our_episodes = json.load(f)
    
    updated_count = 0
    
    for our_ep in our_episodes:
        best_match = None
        best_score = 0
        
        # Find best matching episode by title
        for rss_ep in rss_episodes:
            score = similarity(our_ep['title'], rss_ep['title'])
            if score > best_score:
                best_score = score
                best_match = rss_ep
        
        # If we found a good match (>70% similarity), update the URLs
        if best_match and best_score > 0.7:
            print(f"✅ Matched: '{our_ep['title']}'")
            print(f"   RSS title: '{best_match['title']}' (score: {best_score:.2f})")
            
            # For now, keep the Spotify show URL since we can't easily get episode URLs
            # The RSS only gives us podcasters.spotify.com links (creator URLs)
            # We'd need to scrape Spotify or use their API to get public episode URLs
            
            # Update with what we can get
            if 'platforms' not in our_ep:
                our_ep['platforms'] = {}
            
            # Keep existing YouTube (it's already correct)
            # Spotify & Apple remain show-level for now
            
            updated_count += 1
        else:
            print(f"⚠️ No match: '{our_ep['title']}'")
    
    # Save updated JSON
    with open('src/data/episodes.json', 'w') as f:
        json.dump(our_episodes, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Matched {updated_count} episodes")
    print("\nNote: Spotify/Apple URLs are show-level (not episode-specific)")
    print("To get episode-specific URLs, we'd need:")
    print("  - Spotify Web API (requires app registration)")
    print("  - Or scrape the Spotify show page")
    print("\nFor now, YouTube links are episode-specific, which is the most important.")

if __name__ == '__main__':
    update_episodes_json()
