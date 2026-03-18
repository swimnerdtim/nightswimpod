#!/usr/bin/env python3
"""
Fetch episode transcripts from Spotify and add to episodes.json
"""

import json
import requests
from bs4 import BeautifulSoup
import time

def fetch_spotify_description(spotify_url):
    """Fetch the episode description from Spotify page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(spotify_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find description in meta tags
        og_description = soup.find('meta', property='og:description')
        if og_description:
            return og_description.get('content', '')
        
        # Try to find description in page content
        description_div = soup.find('div', {'data-testid': 'episode-description'})
        if description_div:
            return description_div.get_text(strip=True)
            
        return None
        
    except Exception as e:
        print(f"Error fetching {spotify_url}: {e}")
        return None

def update_episodes_with_transcripts():
    """Update episodes.json with transcripts from Spotify"""
    
    # Load current episodes
    with open('src/data/episodes.json', 'r') as f:
        episodes = json.load(f)
    
    print(f"Processing {len(episodes)} episodes...")
    
    updated_count = 0
    
    for i, episode in enumerate(episodes):
        spotify_url = episode.get('platforms', {}).get('spotify')
        
        if not spotify_url:
            print(f"  [{i+1}/{len(episodes)}] Skipping {episode['title']}: No Spotify URL")
            continue
        
        if episode.get('transcript'):
            print(f"  [{i+1}/{len(episodes)}] Skipping {episode['title']}: Already has transcript")
            continue
        
        print(f"  [{i+1}/{len(episodes)}] Fetching: {episode['title']}")
        
        transcript = fetch_spotify_description(spotify_url)
        
        if transcript and len(transcript) > 100:  # Only add if substantial
            episode['transcript'] = transcript
            updated_count += 1
            print(f"    ✅ Added transcript ({len(transcript)} chars)")
        else:
            print(f"    ⚠️ No transcript found")
        
        # Rate limiting
        time.sleep(1)
    
    # Save updated episodes
    with open('src/data/episodes.json', 'w') as f:
        json.dump(episodes, f, indent=2)
    
    print(f"\n✅ Updated {updated_count} episodes with transcripts")
    print(f"💾 Saved to src/data/episodes.json")

if __name__ == '__main__':
    try:
        update_episodes_with_transcripts()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
