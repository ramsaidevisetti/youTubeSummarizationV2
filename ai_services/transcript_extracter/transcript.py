# ai_services/transcript_extracter/transcript.py
from typing import List, Dict, Optional
from youtube_transcript_api import YouTubeTranscriptApi
import os
import whisper
import yt_dlp
from typing import Optional
import re
from urllib.parse import urlparse, parse_qs

def get_video_id(url: str) -> Optional[str]:
    """Extract video ID from various YouTube URL formats"""
    parsed = urlparse(url)
    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed.query).get("v", [None])[0]
    if parsed.hostname in ["youtu.be"]:
        return parsed.path.lstrip("/")
    return None


def fetch_youtube_transcript(video_id: str, language: str = "en") -> Optional[List[Dict]]:
    """
    Fetch YouTube transcript using the latest youtube-transcript-api (v2+).
    Returns list of {'text': ..., 'start': ..., 'duration': ...} or None if unavailable.
    """
    api = YouTubeTranscriptApi()  # Required in new versions

    try:
        # First, try direct fetch with preferred language
        preferred_langs = [language]
        if '-' in language:  # e.g., 'en-US'
            preferred_langs.append(language.split('-')[0])

        for lang in preferred_langs:
            try:
                fetched = api.fetch(video_id, languages=[lang])
                return fetched.to_raw_data()  # Convert to classic list of dicts
            except:
                continue

        # Fallback: fetch any available (will pick best match)
        fetched = api.fetch(video_id)
        return fetched.to_raw_data()

    except Exception as e:
        print(f"Transcript unavailable for {video_id}: {e}")
        return None


def download_audio(youtube_url: str, output_file: str = "audio.mp3") -> str:
    """Download best audio using yt-dlp (requires ffmpeg installed)"""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_file.replace(".mp3", ""),
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    
    return output_file if os.path.exists(output_file) else output_file.replace(".mp3", ".mp3")


def transcribe_with_whisper(audio_file: str, model_size: str = "small") -> List[Dict]:
    """Transcribe audio using OpenAI Whisper (slow, fallback only)"""
    print(f"Loading Whisper model '{model_size}'...")
    model = whisper.load_model(model_size)
    print("Transcribing...")
    result = model.transcribe(audio_file)
    
    segments = []
    for seg in result["segments"]:
        segments.append({
            "text": seg["text"].strip(),
            "start": seg["start"],
            "duration": seg["end"] - seg["start"]
        })
    return segments

def extract_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from various YouTube URL formats.
    
    Args:
        url: YouTube URL in any format
        
    Returns:
        Video ID if found, None otherwise
    """
    # Handle various YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})',
        r'youtube\.com\/watch\?v=([^&]+)',
        r'youtu\.be\/([^?]+)',
        r'youtube\.com\/embed\/([^?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1) if len(match.groups()) > 0 else match.group(0)
    
    # If no match found, check if it's already a video ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
        
    return None


# ONLY FOR MANUAL TESTING — runs when you execute `python transcript.py` directly
if __name__ == "__main__":
    YOUTUBE_URL = "https://youtu.be/_hheZx7hxGQ?si=Qie5cyZ8HWKWeinm"
    OUTPUT_JSON = "transcript.json"
    AUDIO_FILE = "video_audio.mp3"

    video_id = get_video_id(YOUTUBE_URL)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    print("Trying official YouTube transcript...")
    transcript_data = fetch_youtube_transcript(video_id, language="en")

    if transcript_data:
        print("Official transcript fetched successfully!")
    else:
        print("No official transcript → falling back to Whisper")
        audio_path = download_audio(YOUTUBE_URL, AUDIO_FILE)
        transcript_data = transcribe_with_whisper(audio_path)
        print(transcript_data)
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print("Cleaned up audio file")

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(transcript_data, f, indent=4, ensure_ascii=False)

    print(f"Transcript saved to {OUTPUT_JSON}")