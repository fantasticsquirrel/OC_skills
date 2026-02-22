# Video Download Skill

Download videos from YouTube, TikTok, Twitter, Instagram, Facebook, Twitch, Bilibili, and 1000+ other platforms using yt-dlp.

## Installation

yt-dlp is installed at `/usr/local/bin/yt-dlp` (version 2026.02.21).

To update:
```bash
yt-dlp -U
```

## Supported Platforms

1000+ sites including:
- YouTube (videos, playlists, channels, shorts)
- TikTok
- Twitter/X
- Instagram
- Facebook
- Twitch
- Reddit
- Vimeo
- Dailymotion
- Bilibili
- And many more: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## Basic Usage

### Download a video

```bash
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download to specific directory

```bash
yt-dlp -o "/path/to/downloads/%(title)s.%(ext)s" "URL"
```

### Download best quality

```bash
yt-dlp -f "bestvideo+bestaudio" "URL"
```

### Extract audio only

```bash
yt-dlp -x --audio-format mp3 "URL"
```

### Download playlist

```bash
yt-dlp "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

### Download with specific format (e.g., 1080p)

```bash
yt-dlp -f "bestvideo[height<=1080]+bestaudio" "URL"
```

## Common Options

### Output Template

The `-o` flag controls the output filename. Common template variables:

- `%(title)s` — Video title
- `%(id)s` — Video ID
- `%(ext)s` — File extension
- `%(uploader)s` — Uploader name
- `%(upload_date)s` — Upload date (YYYYMMDD)
- `%(duration)s` — Duration in seconds
- `%(resolution)s` — Resolution (e.g., 1920x1080)

Example:
```bash
yt-dlp -o "%(uploader)s - %(title)s [%(id)s].%(ext)s" "URL"
```

### Quality Selection

```bash
# Best quality (video + audio)
yt-dlp -f "bestvideo+bestaudio" "URL"

# Specific height (e.g., 720p max)
yt-dlp -f "bestvideo[height<=720]+bestaudio" "URL"

# Specific format code (use -F to list)
yt-dlp -F "URL"  # List available formats
yt-dlp -f 137+140 "URL"  # Download format 137 (video) + 140 (audio)

# Best mp4 format
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" "URL"
```

### Audio Extraction

```bash
# Extract as mp3
yt-dlp -x --audio-format mp3 "URL"

# Extract with specific quality
yt-dlp -x --audio-format mp3 --audio-quality 0 "URL"  # 0 = best

# Keep video file after audio extraction
yt-dlp -x --audio-format mp3 --keep-video "URL"
```

### Playlists

```bash
# Download entire playlist
yt-dlp "PLAYLIST_URL"

# Download playlist items 1-10
yt-dlp --playlist-items 1-10 "PLAYLIST_URL"

# Download specific items (1, 3, 5)
yt-dlp --playlist-items 1,3,5 "PLAYLIST_URL"

# Download playlist starting from item 10
yt-dlp --playlist-start 10 "PLAYLIST_URL"

# Skip first 5 items
yt-dlp --playlist-start 6 "PLAYLIST_URL"
```

### Subtitles

```bash
# Download all subtitles
yt-dlp --write-subs --all-subs "URL"

# Download auto-generated subtitles
yt-dlp --write-auto-subs "URL"

# Download English subtitles only
yt-dlp --write-subs --sub-langs "en" "URL"

# Embed subtitles in video
yt-dlp --embed-subs "URL"
```

### Metadata

```bash
# Write metadata to file
yt-dlp --write-info-json "URL"

# Write thumbnail
yt-dlp --write-thumbnail "URL"

# Embed thumbnail in audio file
yt-dlp -x --audio-format mp3 --embed-thumbnail "URL"

# Write description
yt-dlp --write-description "URL"
```

### Download Restrictions

```bash
# Rate limit (e.g., 1M per second)
yt-dlp --limit-rate 1M "URL"

# Maximum file size (e.g., 100M)
yt-dlp --max-filesize 100M "URL"

# Minimum file size
yt-dlp --min-filesize 10M "URL"

# Date filter (YYYYMMDD)
yt-dlp --dateafter 20231201 "URL"
yt-dlp --datebefore 20231231 "URL"
```

### Authentication

```bash
# YouTube login (for private/age-restricted videos)
yt-dlp --username "USERNAME" --password "PASSWORD" "URL"

# Use cookies from browser
yt-dlp --cookies-from-browser chrome "URL"

# Use cookies file
yt-dlp --cookies /path/to/cookies.txt "URL"
```

### Proxy

```bash
# Use HTTP proxy
yt-dlp --proxy "http://proxy.example.com:8080" "URL"

# Use SOCKS5 proxy
yt-dlp --proxy "socks5://proxy.example.com:1080" "URL"
```

### Archive

```bash
# Keep track of downloaded videos (skip already downloaded)
yt-dlp --download-archive downloaded.txt "PLAYLIST_URL"
```

## Advanced Examples

### Download YouTube channel's latest 10 videos

```bash
yt-dlp --playlist-items 1-10 "https://www.youtube.com/@CHANNEL_NAME/videos"
```

### Download all videos from a channel uploaded after a date

```bash
yt-dlp --dateafter 20240101 "https://www.youtube.com/@CHANNEL_NAME/videos"
```

### Download Twitter video

```bash
yt-dlp "https://twitter.com/USER/status/TWEET_ID"
```

### Download Instagram post

```bash
yt-dlp "https://www.instagram.com/p/POST_ID/"
```

### Download TikTok video

```bash
yt-dlp "https://www.tiktok.com/@user/video/VIDEO_ID"
```

### Download Facebook video

```bash
yt-dlp "https://www.facebook.com/user/videos/VIDEO_ID"
```

### Download Twitch VOD

```bash
yt-dlp "https://www.twitch.tv/videos/VOD_ID"
```

### Download livestream

```bash
# Download ongoing livestream
yt-dlp "LIVESTREAM_URL"

# Wait for livestream to start, then download
yt-dlp --wait-for-video 30 "LIVESTREAM_URL"
```

### Batch download from file

Create a file with URLs (one per line):

```
https://www.youtube.com/watch?v=VIDEO1
https://www.youtube.com/watch?v=VIDEO2
https://www.youtube.com/watch?v=VIDEO3
```

Download all:

```bash
yt-dlp -a urls.txt
```

### Post-processing

```bash
# Convert to mp4
yt-dlp --recode-video mp4 "URL"

# Merge video + audio into mkv
yt-dlp --merge-output-format mkv "URL"

# Remove original files after merging
yt-dlp --no-keep-video "URL"
```

## Python Helper

See `skill.py` for a Python wrapper with common download patterns.

## Configuration File

Create `~/.config/yt-dlp/config` for default options:

```
# Default output template
-o ~/Downloads/%(uploader)s/%(title)s.%(ext)s

# Best quality by default
-f bestvideo+bestaudio

# Embed metadata
--embed-metadata
--embed-thumbnail

# Write subtitle files
--write-subs
--sub-langs en

# Archive to avoid re-downloads
--download-archive ~/Downloads/.yt-dlp-archive.txt
```

## Troubleshooting

### Video unavailable or access denied

Try using cookies from your browser:

```bash
yt-dlp --cookies-from-browser firefox "URL"
```

### Download stuck or slow

Use a different CDN or limit rate:

```bash
yt-dlp --limit-rate 500K "URL"
```

### Age-restricted content

Use cookies or login:

```bash
yt-dlp --cookies-from-browser chrome "URL"
```

### Geo-restricted content

Use a proxy:

```bash
yt-dlp --proxy "socks5://proxy.example.com:1080" "URL"
```

## References

- Official docs: https://github.com/yt-dlp/yt-dlp
- Supported sites: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
- Format selection: https://github.com/yt-dlp/yt-dlp#format-selection

## Notes

- VidBee (https://vidbee.org) is a GUI frontend for yt-dlp with RSS auto-download features
- This skill uses yt-dlp directly (CLI) which works on headless servers
- For desktop GUI, download VidBee from vidbee.org (Electron app, not suitable for servers)
