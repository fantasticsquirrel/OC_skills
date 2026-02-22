#!/usr/bin/env python3
"""Video download helper using yt-dlp."""

import subprocess
import json
from pathlib import Path
from typing import Optional, List, Dict, Any


YT_DLP = "/usr/local/bin/yt-dlp"


def download_video(
    url: str,
    output_dir: str = ".",
    output_template: str = "%(title)s.%(ext)s",
    format: str = "bestvideo+bestaudio",
    **kwargs
) -> subprocess.CompletedProcess:
    """Download a video with yt-dlp.
    
    Args:
        url: Video URL
        output_dir: Download directory
        output_template: Output filename template
        format: Quality format string
        **kwargs: Additional yt-dlp options
        
    Returns:
        subprocess.CompletedProcess
        
    Example:
        download_video(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            output_dir="/downloads",
            format="bestvideo[height<=1080]+bestaudio"
        )
    """
    output_path = str(Path(output_dir) / output_template)
    
    cmd = [
        YT_DLP,
        "-f", format,
        "-o", output_path,
        url
    ]
    
    # Add extra options
    for key, value in kwargs.items():
        key_arg = f"--{key.replace('_', '-')}"
        if isinstance(value, bool):
            if value:
                cmd.append(key_arg)
        elif isinstance(value, list):
            for item in value:
                cmd.extend([key_arg, str(item)])
        else:
            cmd.extend([key_arg, str(value)])
    
    return subprocess.run(cmd, capture_output=True, text=True)


def download_audio(
    url: str,
    output_dir: str = ".",
    audio_format: str = "mp3",
    audio_quality: int = 0,
    embed_thumbnail: bool = True
) -> subprocess.CompletedProcess:
    """Download and extract audio from a video.
    
    Args:
        url: Video URL
        output_dir: Download directory
        audio_format: Output format (mp3, m4a, opus, etc.)
        audio_quality: Quality (0=best, 9=worst)
        embed_thumbnail: Embed thumbnail in audio file
        
    Returns:
        subprocess.CompletedProcess
    """
    output_path = str(Path(output_dir) / f"%(title)s.{audio_format}")
    
    cmd = [
        YT_DLP,
        "-x",
        "--audio-format", audio_format,
        "--audio-quality", str(audio_quality),
        "-o", output_path,
        url
    ]
    
    if embed_thumbnail:
        cmd.append("--embed-thumbnail")
    
    return subprocess.run(cmd, capture_output=True, text=True)


def download_playlist(
    url: str,
    output_dir: str = ".",
    playlist_items: Optional[str] = None,
    format: str = "bestvideo+bestaudio",
    archive_file: Optional[str] = None
) -> subprocess.CompletedProcess:
    """Download playlist with optional filtering.
    
    Args:
        url: Playlist URL
        output_dir: Download directory
        playlist_items: Item range (e.g., "1-10", "1,3,5")
        format: Quality format string
        archive_file: Archive file to skip already downloaded videos
        
    Returns:
        subprocess.CompletedProcess
    """
    output_path = str(Path(output_dir) / "%(playlist_index)s - %(title)s.%(ext)s")
    
    cmd = [
        YT_DLP,
        "-f", format,
        "-o", output_path,
        url
    ]
    
    if playlist_items:
        cmd.extend(["--playlist-items", playlist_items])
    
    if archive_file:
        cmd.extend(["--download-archive", archive_file])
    
    return subprocess.run(cmd, capture_output=True, text=True)


def get_video_info(url: str) -> Dict[str, Any]:
    """Get video metadata without downloading.
    
    Args:
        url: Video URL
        
    Returns:
        Dict with video metadata
        
    Example:
        info = get_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print(f"Title: {info['title']}")
        print(f"Duration: {info['duration']}s")
        print(f"Uploader: {info['uploader']}")
    """
    cmd = [YT_DLP, "--dump-json", "--no-download", url]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def list_formats(url: str) -> str:
    """List available formats for a video.
    
    Args:
        url: Video URL
        
    Returns:
        Formatted list of available formats
    """
    cmd = [YT_DLP, "-F", url]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout


def download_batch(
    urls: List[str],
    output_dir: str = ".",
    format: str = "bestvideo+bestaudio"
) -> List[subprocess.CompletedProcess]:
    """Download multiple videos.
    
    Args:
        urls: List of video URLs
        output_dir: Download directory
        format: Quality format string
        
    Returns:
        List of subprocess results
    """
    results = []
    for url in urls:
        result = download_video(url, output_dir=output_dir, format=format)
        results.append(result)
    return results


def download_with_subtitles(
    url: str,
    output_dir: str = ".",
    sub_langs: str = "en",
    embed_subs: bool = True
) -> subprocess.CompletedProcess:
    """Download video with subtitles.
    
    Args:
        url: Video URL
        output_dir: Download directory
        sub_langs: Subtitle languages (comma-separated)
        embed_subs: Embed subtitles in video file
        
    Returns:
        subprocess.CompletedProcess
    """
    output_path = str(Path(output_dir) / "%(title)s.%(ext)s")
    
    cmd = [
        YT_DLP,
        "--write-subs",
        "--sub-langs", sub_langs,
        "-o", output_path,
        url
    ]
    
    if embed_subs:
        cmd.append("--embed-subs")
    
    return subprocess.run(cmd, capture_output=True, text=True)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python skill.py <url>                    # Download video")
        print("  python skill.py --audio <url>            # Download audio")
        print("  python skill.py --info <url>             # Get video info")
        print("  python skill.py --formats <url>          # List formats")
        sys.exit(1)
    
    if sys.argv[1] == "--audio":
        url = sys.argv[2]
        print(f"Downloading audio from: {url}")
        result = download_audio(url)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error: {result.stderr}", file=sys.stderr)
            sys.exit(1)
            
    elif sys.argv[1] == "--info":
        url = sys.argv[2]
        info = get_video_info(url)
        print(json.dumps(info, indent=2))
        
    elif sys.argv[1] == "--formats":
        url = sys.argv[2]
        print(list_formats(url))
        
    else:
        url = sys.argv[1]
        print(f"Downloading video from: {url}")
        result = download_video(url)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error: {result.stderr}", file=sys.stderr)
            sys.exit(1)
