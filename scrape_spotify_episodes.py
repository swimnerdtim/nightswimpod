#!/usr/bin/env python3
"""
Scrape Spotify show page to get episode-specific URLs
"""

import json
import requests
from bs4 import BeautifulSoup
import time
import re

SHOW_URL = "https://open.spotify.com/show/5jeYpru0iqfbtmhDg56IoI"

def scrape_spotify_episodes():
    """Scrape Spotify for all episode URLs"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        print(f"🎵 Fetching Spotify show page...")
        response = requests.get(SHOW_URL, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for episode links in the page
        episode_links = []
        
        # Spotify uses React, so we need to look in the embedded JSON
        scripts = soup.find_all('script', type='application/ld+json')
        
        for script in scripts:
            try:
                data = json.loads(script.string)
                if 'episode' in str(data).lower():
                    print("Found episode data in JSON-LD")
                    print(json.dumps(data, indent=2)[:500])
            except:
                pass
        
        # Alternative: look for episode URLs in meta tags or links
        links = soup.find_all('a', href=re.compile(r'/episode/'))
        
        for link in links[:10]:
            href = link.get('href', '')
            if '/episode/' in href:
                episode_links.append(href)
                print(f"Found episode link: {href}")
        
        return episode_links
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == '__main__':
    scrape_spotify_episodes()
