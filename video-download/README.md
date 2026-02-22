# Video Download Skill

Download videos from 1000+ platforms including YouTube, TikTok, Twitter, Instagram, Facebook, Twitch, and more.

## Quick Start

### Download a video

```bash
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download as MP3

```bash
yt-dlp -x --audio-format mp3 "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download playlist

```bash
yt-dlp "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

### Download to specific folder

```bash
yt-dlp -o "/downloads/%(title)s.%(ext)s" "URL"
```

## Python Helper

```python
from skill import download_video, download_audio, get_video_info

# Download video
download_video(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    output_dir="/downloads",
    format="bestvideo[height<=1080]+bestaudio"
)

# Download as MP3
download_audio(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    output_dir="/downloads",
    audio_format="mp3"
)

# Get video metadata
info = get_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(f"Title: {info['title']}")
print(f"Duration: {info['duration']}s")
print(f"Views: {info['view_count']}")
```

## Command Line Tool

```bash
# Download video
python skill.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Download audio
python skill.py --audio "https://www.youtube.com/watch?v=VIDEO_ID"

# Get video info
python skill.py --info "https://www.youtube.com/watch?v=VIDEO_ID"

# List available formats
python skill.py --formats "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Supported Platforms

- YouTube (videos, playlists, channels, shorts, livestreams)
- TikTok
- Twitter/X
- Instagram
- Facebook
- Twitch
- Reddit
- Vimeo
- Dailymotion
- Bilibili
- SoundCloud
- And 1000+ more: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## Installation

yt-dlp is already installed at `/usr/local/bin/yt-dlp`.

To update:
```bash
yt-dlp -U
```

## Common Tasks

### Download best quality video

```bash
yt-dlp -f "bestvideo+bestaudio" "URL"
```

### Download 720p max

```bash
yt-dlp -f "bestvideo[height<=720]+bestaudio" "URL"
```

### Download with subtitles

```bash
yt-dlp --write-subs --sub-langs en "URL"
```

### Download Twitter video

```bash
yt-dlp "https://twitter.com/user/status/TWEET_ID"
```

### Download Instagram post

```bash
yt-dlp "https://www.instagram.com/p/POST_ID/"
```

### Download TikTok

```bash
yt-dlp "https://www.tiktok.com/@user/video/VIDEO_ID"
```

### Batch download from file

Create `urls.txt`:
```
https://www.youtube.com/watch?v=VIDEO1
https://www.youtube.com/watch?v=VIDEO2
```

Download all:
```bash
yt-dlp -a urls.txt
```

## Full Documentation

See [SKILL.md](SKILL.md) for complete documentation including:
- All supported platforms
- Advanced usage examples
- Quality selection
- Playlist filtering
- Authentication & cookies
- Proxy configuration
- Post-processing options
- Troubleshooting

## About VidBee

[VidBee](https://vidbee.org) is a GUI desktop application built on top of yt-dlp, offering:
- Modern UI with download queue management
- RSS auto-download for favorite creators
- One-click pause/resume/retry
- Cross-platform (Windows, Mac, Linux desktop)

This skill uses yt-dlp directly (CLI) which is perfect for:
- Headless servers
- Automation scripts
- OpenClaw integration
- Programmatic downloads

For desktop GUI usage, download VidBee from https://vidbee.org

## License

Part of the OpenClaw project.
