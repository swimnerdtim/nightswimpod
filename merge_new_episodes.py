#!/usr/bin/env python3
"""
Merge NEW Night Swim YouTube episodes into src/data/episodes.json.
- Pulls the recent uploads (flat) to get video IDs + titles
- For any video ID not already in episodes.json, fetch exact upload date + full description
- Insert, dedupe, sort newest-first, save
"""
import json
import re
import subprocess
import sys

YTDLP = "/opt/homebrew/bin/yt-dlp"
CHANNEL = "https://www.youtube.com/channel/UCxKskf92IDxYWM4advqsWMQ/videos"
EPISODES_PATH = "src/data/episodes.json"
FETCH_COUNT = 60  # how many recent uploads to scan

def create_episode_id(title):
    i = re.sub(r'[^\w\s-]', '', title.lower())
    i = re.sub(r'[-\s]+', '-', i)
    return i[:70]

def categorize_episode(title, description=""):
    text = (title + " " + description).lower()
    if any(w in text for w in ["hot take", "rant", "controversial", "exposes", "pissed", "goes off"]):
        return "hot-takes"
    if any(w in text for w in ["interview", "joins", "talks", "conversation", "reveals", "full interview"]):
        return "interviews"
    if any(w in text for w in ["workout", "training", "drill", "technique", "speed", "dryland", "muscle", "kick"]):
        return "training"
    if any(w in text for w in ["meet", "championship", "olympics", "world record", "trials", "recap", "national"]):
        return "events"
    return "news"

def run_json_lines(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = []
    for line in res.stdout.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out

def main():
    with open(EPISODES_PATH) as f:
        episodes = json.load(f)
    existing_ids = {ep['youtubeId'] for ep in episodes}
    print(f"Existing episodes: {len(episodes)}")

    print(f"Fetching {FETCH_COUNT} recent uploads (flat)...")
    flat = run_json_lines([
        YTDLP, "--flat-playlist", "--dump-json", "--no-warnings",
        "--playlist-end", str(FETCH_COUNT), CHANNEL
    ])
    candidates = [(v.get('id'), v.get('title', '')) for v in flat if v.get('id')]
    new_ids = [(vid, title) for vid, title in candidates if vid not in existing_ids]
    print(f"Found {len(new_ids)} new videos not yet on site")
    for vid, title in new_ids:
        print(f"  NEW: {vid} - {title[:65]}")

    if not new_ids:
        print("Nothing to add. Site is up to date.")
        return 0

    added = 0
    for vid, _title in new_ids:
        detail = run_json_lines([
            YTDLP, "--dump-json", "--no-warnings", "--skip-download",
            f"https://www.youtube.com/watch?v={vid}"
        ])
        if not detail:
            print(f"  ! Could not fetch details for {vid}, skipping")
            continue
        v = detail[0]
        title = v.get('title', '')
        description = v.get('description', '') or ''
        upload = v.get('upload_date', '')  # YYYYMMDD
        if upload and len(upload) == 8:
            publish_date = f"{upload[:4]}-{upload[4:6]}-{upload[6:8]}"
        else:
            publish_date = "2026-01-01"
        episodes.append({
            "id": create_episode_id(title),
            "title": title,
            "description": description[:500],
            "youtubeId": vid,
            "thumbnail": f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg",
            "publishDate": publish_date,
            "category": categorize_episode(title, description),
            "platforms": {
                "youtube": f"https://youtube.com/watch?v={vid}",
                "spotify": "https://open.spotify.com/show/5jeYpru0iqfbtmhDg56IoI",
                "apple": "https://podcasts.apple.com/us/podcast/night-swim-podcast/id1853013593"
            }
        })
        added += 1
        print(f"  + {publish_date} - {title[:60]}")

    # dedupe by youtubeId (keep first)
    seen = set()
    deduped = []
    for ep in episodes:
        if ep['youtubeId'] in seen:
            continue
        seen.add(ep['youtubeId'])
        deduped.append(ep)
    deduped.sort(key=lambda x: x['publishDate'], reverse=True)

    with open(EPISODES_PATH, 'w') as f:
        json.dump(deduped, f, indent=2)

    print(f"\nAdded {added} new episodes. Total now: {len(deduped)}")
    print(f"Newest: {deduped[0]['publishDate']} - {deduped[0]['title'][:60]}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
