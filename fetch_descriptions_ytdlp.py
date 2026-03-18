#!/usr/bin/env python3
"""
Fetch YouTube video descriptions using yt-dlp (no auth needed)
"""

import json
import subprocess
import sys

def fetch_video_description(video_id):
    """Fetch description using yt-dlp"""
    try:
        result = subprocess.run(
            ['yt-dlp', '--skip-download', '--print', 'description', f'https://www.youtube.com/watch?v={video_id}'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        return None
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def update_episodes_with_descriptions():
    """Update episodes.json with YouTube descriptions"""
    
    # Load current episodes
    with open('src/data/episodes.json', 'r') as f:
        episodes = json.load(f)
    
    print(f"📺 Processing {len(episodes)} episodes...")
    
    updated_count = 0
    
    for i, episode in enumerate(episodes):
        video_id = episode.get('youtubeId')
        
        if not video_id:
            print(f"  [{i+1}/{len(episodes)}] ⚠️ Skip: No YouTube ID")
            continue
        
        if episode.get('transcript'):
            print(f"  [{i+1}/{len(episodes)}] ⏭️ Skip: {episode['title'][:50]}... (has transcript)")
            continue
        
        print(f"  [{i+1}/{len(episodes)}] Fetching: {episode['title'][:60]}...")
        
        description = fetch_video_description(video_id)
        
        if description and len(description) > 100:
            episode['transcript'] = description
            updated_count += 1
            print(f"    ✅ Added ({len(description)} chars)")
        else:
            print(f"    ⚠️ Too short or missing")
    
    # Save updated episodes
    with open('src/data/episodes.json', 'w') as f:
        json.dump(episodes, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Updated {updated_count} episodes")
    print(f"💾 Saved to src/data/episodes.json")

if __name__ == '__main__':
    try:
        # Check if yt-dlp is installed
        try:
            subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ yt-dlp not found. Install with: brew install yt-dlp")
            sys.exit(1)
        
        update_episodes_with_descriptions()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
