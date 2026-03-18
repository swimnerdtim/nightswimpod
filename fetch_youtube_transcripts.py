#!/usr/bin/env python3
"""
Fetch actual YouTube transcripts with timestamps using yt-dlp
"""

import json
import subprocess
import sys

def fetch_transcript_with_timestamps(video_id):
    """Fetch transcript using yt-dlp --write-auto-sub"""
    try:
        result = subprocess.run(
            [
                'yt-dlp',
                '--skip-download',
                '--write-auto-sub',
                '--sub-lang', 'en',
                '--sub-format', 'json3',
                '--output', f'/tmp/%(id)s',
                f'https://www.youtube.com/watch?v={video_id}'
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Read the generated subtitle file
            try:
                with open(f'/tmp/{video_id}.en.json3', 'r') as f:
                    captions = json.load(f)
                
                # Parse captions into readable transcript with timestamps
                transcript_lines = []
                for event in captions.get('events', []):
                    if 'segs' in event:
                        start_time = event.get('tStartMs', 0) / 1000
                        text = ''.join(seg.get('utf8', '') for seg in event['segs']).strip()
                        if text:
                            # Format timestamp as MM:SS
                            mins = int(start_time // 60)
                            secs = int(start_time % 60)
                            timestamp = f"[{mins:02d}:{secs:02d}]"
                            transcript_lines.append(f"{timestamp} {text}")
                
                return '\n'.join(transcript_lines)
            except Exception as e:
                print(f"  ⚠️ Error parsing captions: {e}")
                return None
        else:
            return None
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def update_episodes_with_transcripts():
    """Update episodes.json with real transcripts"""
    
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
        
        # Keep existing description in "transcript" field
        # Add new "fullTranscript" field with timestamps
        if episode.get('fullTranscript'):
            print(f"  [{i+1}/{len(episodes)}] ⏭️ Skip: {episode['title'][:50]}... (has fullTranscript)")
            continue
        
        print(f"  [{i+1}/{len(episodes)}] Fetching: {episode['title'][:60]}...")
        
        transcript = fetch_transcript_with_timestamps(video_id)
        
        if transcript and len(transcript) > 200:
            episode['fullTranscript'] = transcript
            updated_count += 1
            print(f"    ✅ Added full transcript ({len(transcript)} chars)")
        else:
            print(f"    ⚠️ No transcript available (auto-captions may be disabled)")
    
    # Save updated episodes
    with open('src/data/episodes.json', 'w') as f:
        json.dump(episodes, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Updated {updated_count} episodes with full transcripts")
    print(f"💾 Saved to src/data/episodes.json")

if __name__ == '__main__':
    try:
        update_episodes_with_transcripts()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
