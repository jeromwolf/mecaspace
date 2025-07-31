import os
import requests
from typing import Optional
from pydub import AudioSegment
from src.core.config import config


class MusicService:
    def __init__(self):
        self.music_dir = os.path.join(config.output_dir, "music")
        os.makedirs(self.music_dir, exist_ok=True)
        
    def get_background_music(self, duration: int, style: str = "calm") -> Optional[str]:
        """
        Get background music for the video.
        
        Args:
            duration: Required duration in seconds
            style: Music style (calm, upbeat, etc.)
            
        Returns:
            Path to the music file
        """
        # For now, we'll use royalty-free music from a local collection
        # In production, you might want to use APIs like Epidemic Sound, AudioJungle, etc.
        
        music_path = os.path.join(self.music_dir, f"{style}_background.mp3")
        
        # Check if we have pre-downloaded music
        if os.path.exists(music_path):
            return self._adjust_music_duration(music_path, duration)
        
        # Otherwise, try to download from free sources
        music_urls = {
            "calm": "https://www.bensound.com/bensound-music/bensound-memories.mp3",
            "upbeat": "https://www.bensound.com/bensound-music/bensound-sunny.mp3",
            "inspiring": "https://www.bensound.com/bensound-music/bensound-inspire.mp3"
        }
        
        if style in music_urls:
            try:
                self._download_music(music_urls[style], music_path)
                return self._adjust_music_duration(music_path, duration)
            except Exception as e:
                print(f"Error downloading music: {e}")
        
        # If all else fails, generate silence
        return self._generate_silence(duration)
    
    def _download_music(self, url: str, save_path: str):
        """Download music from URL."""
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    
    def _adjust_music_duration(self, music_path: str, target_duration: int) -> str:
        """
        Adjust music duration to match video length.
        
        Args:
            music_path: Path to the original music file
            target_duration: Target duration in seconds
            
        Returns:
            Path to the adjusted music file
        """
        audio = AudioSegment.from_file(music_path)
        current_duration = len(audio) / 1000  # Convert to seconds
        
        output_path = os.path.join(
            self.music_dir, 
            f"adjusted_{os.path.basename(music_path)}"
        )
        
        if current_duration < target_duration:
            # Loop the music if it's shorter than needed
            loops_needed = int(target_duration / current_duration) + 1
            audio = audio * loops_needed
        
        # Trim to exact duration
        audio = audio[:target_duration * 1000]
        
        # Apply fade in/out
        fade_duration = config.music_fade_duration * 1000
        audio = audio.fade_in(fade_duration).fade_out(fade_duration)
        
        # Adjust volume
        audio = audio - (20 * (1 - config.music_volume))  # Convert to dB
        
        audio.export(output_path, format="mp3")
        return output_path
    
    def _generate_silence(self, duration: int) -> str:
        """Generate a silent audio track."""
        silence = AudioSegment.silent(duration=duration * 1000)
        output_path = os.path.join(self.music_dir, "silence.mp3")
        silence.export(output_path, format="mp3")
        return output_path
    
    def create_music_library(self):
        """
        Create a library of background music options.
        This would be called during setup to prepare music files.
        """
        # In a real implementation, you would:
        # 1. Connect to a music API or service
        # 2. Download various styles of royalty-free music
        # 3. Organize them by mood/style
        # 4. Store metadata about each track
        
        music_library = {
            "calm": {
                "description": "Peaceful, relaxing music for study",
                "tracks": ["memories.mp3", "relaxing.mp3", "meditation.mp3"]
            },
            "upbeat": {
                "description": "Energetic, positive music",
                "tracks": ["sunny.mp3", "happy.mp3", "ukulele.mp3"]
            },
            "inspiring": {
                "description": "Motivational, uplifting music",
                "tracks": ["inspire.mp3", "epic.mp3", "cinematic.mp3"]
            }
        }
        
        # Save library metadata
        import json
        library_path = os.path.join(self.music_dir, "library.json")
        with open(library_path, 'w') as f:
            json.dump(music_library, f, indent=2)