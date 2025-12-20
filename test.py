
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import yt_dlp
import whisper
from urllib.parse import urlparse, parse_qs

# -----------------------------
# CONFIG
# -----------------------------
youtube_url = "https://youtu.be/B0p5SdkBydU?si=7G2RmoV7EZCoVtoA"
audio_file = "video_audio.mp3"

# -----------------------------
# Extract YouTube video ID
# -----------------------------
def get_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed.query).get("v", [None])[0]
    elif parsed.hostname == "youtu.be":
        return parsed.path[1:]
    return None

video_id = get_video_id(youtube_url)
if not video_id:
    raise ValueError("Invalid YouTube URL")

# -----------------------------
# 1️⃣ Try fetching transcript (updated for latest youtube-transcript-api)
# -----------------------------
try:
    ytt_api = YouTubeTranscriptApi()  # Create instance
    transcript_list = ytt_api.list(video_id)  # Use .list() on instance
    transcript = transcript_list.find_transcript(['en'])  # Find English transcript
    transcript_data = transcript.fetch()  # Fetch the data
    transcript_text = " ".join([snippet.text for snippet in transcript.fetch()])
    
    print("✅ Transcript fetched from YouTube:\n")
    print(transcript_text)

except (TranscriptsDisabled, NoTranscriptFound):
    print("⚠ YouTube transcript not found, downloading audio and transcribing...")

    # -----------------------------
    # 2️⃣ Download YouTube audio
    # -----------------------------
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': audio_file,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    print(f"✅ Audio downloaded: {audio_file}")

    # -----------------------------
    # 3️⃣ Transcribe audio with Whisper
    # -----------------------------
    model = whisper.load_model("small")
    result = model.transcribe(audio_file)
    transcript_text = result["text"]

    print("✅ Transcript generated from audio:\n")
    print(transcript_text)

# -----------------------------
# 4️⃣ Save transcript
# -----------------------------
with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write(transcript_text)

print("✅ Transcript saved to transcript.txt")