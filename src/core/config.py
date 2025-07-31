import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    # API Keys
    unsplash_access_key: Optional[str] = os.getenv("UNSPLASH_ACCESS_KEY")
    azure_speech_key: Optional[str] = os.getenv("AZURE_SPEECH_KEY")
    azure_speech_region: Optional[str] = os.getenv("AZURE_SPEECH_REGION")
    youtube_api_key: Optional[str] = os.getenv("YOUTUBE_API_KEY")
    
    # Directories
    output_dir: str = os.getenv("OUTPUT_DIR", "output")
    video_output_dir: str = os.path.join(output_dir, "videos")
    audio_output_dir: str = os.path.join(output_dir, "audio")
    image_output_dir: str = os.path.join(output_dir, "images")
    
    # Video Settings
    video_width: int = int(os.getenv("VIDEO_WIDTH", "1920"))
    video_height: int = int(os.getenv("VIDEO_HEIGHT", "1080"))
    video_fps: int = int(os.getenv("VIDEO_FPS", "24"))
    sentence_display_time: int = int(os.getenv("SENTENCE_DISPLAY_TIME", "8"))
    transition_time: int = int(os.getenv("TRANSITION_TIME", "1"))
    
    # TTS Settings
    tts_engine: str = os.getenv("TTS_ENGINE", "azure")
    tts_voice_en: str = os.getenv("TTS_VOICE_EN", "en-US-JennyNeural")
    tts_voice_ko: str = os.getenv("TTS_VOICE_KO", "ko-KR-SunHiNeural")
    tts_speed: float = float(os.getenv("TTS_SPEED", "1.0"))
    
    # Background Music
    music_volume: float = float(os.getenv("MUSIC_VOLUME", "0.1"))
    music_fade_duration: int = int(os.getenv("MUSIC_FADE_DURATION", "2"))
    
    def __post_init__(self):
        # Create directories if they don't exist
        for dir_path in [self.output_dir, self.video_output_dir, 
                         self.audio_output_dir, self.image_output_dir]:
            os.makedirs(dir_path, exist_ok=True)


config = Config()