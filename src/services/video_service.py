import os
from typing import List, Tuple
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from src.core.config import config


class VideoService:
    def __init__(self):
        self.width = config.video_width
        self.height = config.video_height
        self.fps = config.video_fps
        self.sentence_duration = config.sentence_display_time
        self.transition_duration = config.transition_time
        
    def create_text_overlay(self, text: str, position: str = "center", 
                           font_size: int = 60, color: str = "white",
                           stroke_color: str = "black", stroke_width: int = 3) -> ImageClip:
        """
        Create a text overlay with stroke effect for better readability.
        """
        # Create text with stroke using PIL for better quality
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fallback to default if not available
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Calculate position
        if position == "center":
            x = (self.width - text_width) // 2
            y = (self.height - text_height) // 2
        elif position == "top":
            x = (self.width - text_width) // 2
            y = self.height // 6
        else:  # bottom
            x = (self.width - text_width) // 2
            y = self.height - (self.height // 4)
        
        # Draw text with stroke
        for adj_x in range(-stroke_width, stroke_width + 1):
            for adj_y in range(-stroke_width, stroke_width + 1):
                draw.text((x + adj_x, y + adj_y), text, font=font, fill=stroke_color)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=color)
        
        # Convert to numpy array and create ImageClip
        img_array = np.array(img)
        return ImageClip(img_array, duration=self.sentence_duration)
    
    def create_sentence_clip(self, background_path: str, 
                           en_audio_path: str, ko_audio_path: str,
                           en_text: str, ko_text: str, 
                           sentence_number: int) -> VideoClip:
        """
        Create a video clip for one sentence pair.
        """
        # Load background image
        background = ImageClip(background_path).set_duration(self.sentence_duration)
        background = background.resize((self.width, self.height))
        
        # Add subtle zoom effect
        background = background.resize(lambda t: 1 + 0.02 * t)
        
        # Create header with sentence number
        header_text = f"#{sentence_number}"
        header = self.create_text_overlay(header_text, "top", 40, "#FFD700")
        
        # Create text overlays
        en_text_overlay = self.create_text_overlay(en_text, "center", 50, "white")
        ko_text_overlay = self.create_text_overlay(ko_text, "bottom", 45, "#87CEEB")
        
        # Load audio
        en_audio = AudioFileClip(en_audio_path)
        ko_audio = AudioFileClip(ko_audio_path)
        
        # Calculate timings
        en_duration = en_audio.duration
        ko_duration = ko_audio.duration
        pause_duration = 0.5
        
        total_duration = en_duration + pause_duration + ko_duration + pause_duration
        
        # Set timings for text and audio
        en_text_timed = en_text_overlay.set_start(0).set_duration(en_duration + pause_duration)
        ko_text_timed = ko_text_overlay.set_start(en_duration + pause_duration).set_duration(ko_duration + pause_duration)
        
        en_audio_timed = en_audio.set_start(0)
        ko_audio_timed = ko_audio.set_start(en_duration + pause_duration)
        
        # Combine audio
        audio = CompositeAudioClip([en_audio_timed, ko_audio_timed])
        
        # Update background duration
        background = background.set_duration(total_duration)
        header = header.set_duration(total_duration)
        
        # Composite video
        video = CompositeVideoClip([
            background,
            header.set_opacity(0.9),
            en_text_timed.crossfadein(0.5).crossfadeout(0.5),
            ko_text_timed.crossfadein(0.5).crossfadeout(0.5)
        ])
        
        # Set audio
        video = video.set_audio(audio)
        
        return video
    
    def create_intro_clip(self, title: str, subtitle: str) -> VideoClip:
        """Create an intro clip for the video."""
        # Create gradient background using numpy
        import numpy as np
        gradient = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        for y in range(self.height):
            ratio = y / self.height
            gradient[y, :] = [
                int(50 + (150 - 50) * ratio),  # R
                50,  # G
                int(150 + (50 - 150) * ratio)   # B
            ]
        background = ImageClip(gradient).set_duration(3)
        
        # Create title and subtitle
        title_clip = self.create_text_overlay(title, "center", 80, "white")
        subtitle_clip = self.create_text_overlay(subtitle, "bottom", 40, "#FFD700")
        
        # Composite
        intro = CompositeVideoClip([
            background,
            title_clip.set_duration(3).crossfadein(1),
            subtitle_clip.set_duration(3).set_start(0.5).crossfadein(1)
        ])
        
        return intro
    
    def create_outro_clip(self) -> VideoClip:
        """Create an outro clip."""
        # Similar to intro but with different text
        import numpy as np
        gradient = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        for y in range(self.height):
            ratio = y / self.height
            gradient[y, :] = [
                int(50 + (150 - 50) * ratio),  # R
                50,  # G
                int(150 + (50 - 150) * ratio)   # B
            ]
        background = ImageClip(gradient).set_duration(3)
        
        text1 = self.create_text_overlay("Thank you for watching!", "center", 60, "white")
        text2 = self.create_text_overlay("Subscribe for more!", "bottom", 40, "#FFD700")
        
        outro = CompositeVideoClip([
            background,
            text1.set_duration(3).crossfadein(0.5),
            text2.set_duration(3).set_start(0.5).crossfadein(0.5)
        ])
        
        return outro
    
    def create_full_video(self, sentences: List[Tuple[str, str]], 
                         audio_files: List[Tuple[str, str]],
                         image_paths: List[str],
                         background_music_path: str,
                         output_path: str,
                         title: str = "Daily English Study",
                         subtitle: str = "Learn with Us"):
        """
        Create the complete video from all components.
        """
        clips = []
        
        # Add intro
        intro = self.create_intro_clip(title, subtitle)
        clips.append(intro)
        
        # Create clips for each sentence
        for i, ((en_text, ko_text), (en_audio, ko_audio), img_path) in enumerate(
            zip(sentences, audio_files, image_paths)):
            
            clip = self.create_sentence_clip(
                img_path, en_audio, ko_audio, 
                en_text, ko_text, i + 1
            )
            clips.append(clip)
        
        # Add outro
        outro = self.create_outro_clip()
        clips.append(outro)
        
        # Concatenate all clips with transitions
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Add background music
        if background_music_path and os.path.exists(background_music_path):
            bg_music = AudioFileClip(background_music_path)
            bg_music = bg_music.volumex(config.music_volume)
            bg_music = bg_music.set_duration(final_video.duration)
            
            # Mix with existing audio
            final_audio = CompositeAudioClip([final_video.audio, bg_music])
            final_video = final_video.set_audio(final_audio)
        
        # Write the final video
        final_video.write_videofile(
            output_path,
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Clean up
        final_video.close()
        
        return output_path