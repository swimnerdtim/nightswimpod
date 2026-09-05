# Night Swim Website Update Log

## Update: July 13, 2026 (07:55 AM EDT)

**Status:** ✅ DEPLOYED

**What changed:**
- Updated episodes data from YouTube channel `@NightSwimPod`
- Fetched 50 most recent episodes (Mar 16 - Jul 12, 2026)
- Replaced old data with fresh content

**Episode summary:**
- **50 episodes** now live on site
- **Date range:** March 16, 2026 → July 12, 2026
- **Latest episode:** "Is the IOC's New Athlete Grant Actually a Pay Cut?" (Jul 12, 2026)

**Top 10 newest episodes:**
1. **Jul 12** - Is the IOC's New Athlete Grant Actually a Pay Cut?
2. **Jul 11** - Jordan Crooks Is BACK! Can the World's Fastest Swimmer Dominate Again?
3. **Jul 11** - Jessica Hardy Is This Really a Comeback... or Just Publicity?
4. **Jul 10** - Should Swimming Add a 25 Freestyle? The Debate That Could Change the Sport
5. **Jul 9** - Did Léon Marchand Push Too Hard? The Injury Explained
6. **Jul 7** - Why Are Women's Swimming World Records Falling So Fast?
7. **Jun 30** - Race Pace Training For Distance Swimmers in the after math of the Australian Championships
8. **Jun 29** - The Longhorn "Elite" Invite isn't Elite
9. **Jun 29** - Sam Short The World's Fastest Distance Swimmer Reveals His Secrets
10. **Jun 23** - Heart Rate Monitors in Swimming: Complete Waste of Time or Game-Changer? Dax vs Elvis Debate

**Technical details:**
- Git commit: `499211c`
- GitHub Actions workflow: Run #29247915603
- Build time: 17s
- Deploy time: 9s
- Total deployment: ~26 seconds

**URLs:**
- Live site: https://nightswimpod.com/
- Episodes page: https://nightswimpod.com/episodes
- GitHub repo: https://github.com/swimnerdtim/nightswimpod

**Files updated:**
- `src/data/episodes.json` (701 lines, 50 episodes)

**Method used:**
- Script: `quick_update.py`
- Tool: `yt-dlp` with `--playlist-end 50`
- Full metadata extraction (proper dates, descriptions, thumbnails)

**Note:** This update only includes the 50 most recent episodes. To add ALL 152 episodes from the channel history, run the full `import_with_dates.py` script (takes 3-5 minutes).

---

## Previous Updates

### Update: June 23, 2026
- Added 8 new episodes (Jun 9-23, 2026)
- Workflow run: 28024283880

### Update: June 8, 2026
- Added episode: "Enhanced Games Was NOT a Failure 🔥"
- Workflow run: 27143531228
