#!/usr/bin/env python3
"""
Fetch YouTube video descriptions and add as transcripts to episodes.json
YouTube descriptions often contain detailed episode notes/transcripts
"""

import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

YOUTUBE_TOKENS = '/Users/tim/.openclaw/credentials/youtube-tokens-nightswim.json'

def get_youtube_service():
    """Get authenticated YouTube API service"""
    with open(YOUTUBE_TOKENS, 'r') as f:
        creds_data = json.load(f)
    
    creds = Credentials.from_authorized_user_info(creds_data)
    
    # Refresh if expired
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save refreshed token
        with open(YOUTUBE_TOKENS, 'w') as f:
            f.write(creds.to_json())
    
    return build('youtube', 'v3', credentials=creds)

def fetch_video_description(youtube_service, video_id):
    """Fetch full description for a YouTube video"""
    try:
        request = youtube_service.videos().list(
            part='snippet',
            id=video_id
        )
        response = request.execute()
        
        if response.get('items'):
            description = response['items'][0]['snippet']['description']
            return description
        
        return None
        
    except Exception as e:
        print(f"  ❌ Error fetching {video_id}: {e}")
        return None

def update_episodes_with_descriptions():
    """Update episodes.json with YouTube descriptions"""
    
    # Load current episodes
    with open('src/data/episodes.json', 'r') as f:
        episodes = json.load(f)
    
    print(f"📺 Processing {len(episodes)} episodes...")
    
    youtube = get_youtube_service()
    updated_count = 0
    
    for i, episode in enumerate(episodes):
        video_id = episode.get('youtubeId')
        
        if not video_id:
            print(f"  [{i+1}/{len(episodes)}] ⚠️ Skipping {episode['title']}: No YouTube ID")
            continue
        
        if episode.get('transcript'):
            print(f"  [{i+1}/{len(episodes)}] ⏭️ Skipping {episode['title']}: Already has transcript")
            continue
        
        print(f"  [{i+1}/{len(episodes)}] Fetching: {episode['title']}")
        
        description = fetch_video_description(youtube, video_id)
        
        if description and len(description) > 100:  # Only add if substantial
            episode['transcript'] = description
            updated_count += 1
            print(f"    ✅ Added description ({len(description)} chars)")
        else:
            print(f"    ⚠️ Description too short or missing")
    
    # Save updated episodes
    with open('src/data/episodes.json', 'w') as f:
        json.dump(episodes, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Updated {updated_count} episodes with descriptions")
    print(f"💾 Saved to src/data/episodes.json")

if __name__ == '__main__':
    try:
        update_episodes_with_descriptions()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
