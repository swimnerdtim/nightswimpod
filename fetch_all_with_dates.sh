#!/bin/bash
echo "📥 Fetching all 290 videos with dates..."
echo "This will take 5-10 minutes (need full metadata for dates)"

# Extract all video IDs
jq -r '.id' /tmp/all_uploads.jsonl > /tmp/video_ids.txt
TOTAL=$(wc -l < /tmp/video_ids.txt | tr -d ' ')
echo "Found $TOTAL video IDs"

# Fetch in batches of 50 (YouTube API limit)
rm -f /tmp/all_videos_with_dates.jsonl
count=0

while read video_id; do
  count=$((count+1))
  if [ $((count % 10)) -eq 0 ]; then
    echo "Progress: $count/$TOTAL..."
  fi
  
  # Fetch full metadata for this video
  /opt/homebrew/bin/yt-dlp --dump-json --no-warnings "https://www.youtube.com/watch?v=$video_id" 2>/dev/null >> /tmp/all_videos_with_dates.jsonl
  
  # Small delay to avoid rate limits
  sleep 0.1
done < /tmp/video_ids.txt

echo "✅ Done! Saved to /tmp/all_videos_with_dates.jsonl"
wc -l /tmp/all_videos_with_dates.jsonl
