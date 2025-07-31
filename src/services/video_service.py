import os
from typing import List, Tuple
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from src.core.config import config
import textwrap


class VideoService:
    def __init__(self):
        self.width = config.video_width
        self.height = config.video_height
        self.fps = config.video_fps
        self.sentence_duration = config.sentence_display_time
        self.transition_duration = config.transition_time
    
    def wrap_text(self, text: str, font: ImageFont, max_width: int, draw: ImageDraw) -> str:
        """
        Wrap text to fit within maximum width.
        
        Args:
            text: Text to wrap
            font: Font to use for measuring
            max_width: Maximum width in pixels
            draw: ImageDraw object for text measurement
            
        Returns:
            Text with newlines added for wrapping
        """
        # First try to wrap by words
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = bbox[2] - bbox[0]
            
            if line_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Single word is too long, need to break it
                    lines.append(word)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
        
    def create_text_overlay(self, text: str, position: str = "center", 
                           font_size: int = 60, color: str = "white",
                           stroke_color: str = "black", stroke_width: int = 3,
                           with_background: bool = True) -> ImageClip:
        """
        Create a text overlay with background board for better readability.
        """
        # Create transparent image
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Try to use fonts that support Korean characters
        font_paths = [
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS Korean font
            "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",  # Linux Bold
            "C:/Windows/Fonts/malgunbd.ttf",  # Windows Bold
            "/System/Library/Fonts/Helvetica.ttc"  # Fallback
        ]
        
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except:
                continue
        
        if font is None:
            font = ImageFont.load_default()
        
        # Apply text wrapping
        max_text_width = int(self.width * 0.8)  # Use 80% of screen width
        wrapped_text = self.wrap_text(text, font, max_text_width, draw)
        
        # Get text size with wrapped text
        text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Add padding for background
        padding = 40
        board_width = text_width + padding * 2
        board_height = text_height + padding * 2
        
        # Calculate position
        if position == "center":
            board_x = (self.width - board_width) // 2
            board_y = (self.height - board_height) // 2
        elif position == "top":
            board_x = (self.width - board_width) // 2
            board_y = self.height // 6
        else:  # bottom
            board_x = (self.width - board_width) // 2
            board_y = self.height - (self.height // 4) - board_height // 2
        
        text_x = board_x + padding
        text_y = board_y + padding
        
        # Draw background board with rounded corners
        if with_background:
            # Create a separate image for the board with blur effect
            board_img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            board_draw = ImageDraw.Draw(board_img)
            
            # Draw modern frosted glass effect background
            radius = 30
            board_draw.rounded_rectangle(
                [board_x, board_y, board_x + board_width, board_y + board_height],
                radius=radius,
                fill=(255, 255, 255, 80)  # Light white frosted glass effect
            )
            
            # Apply stronger blur for better frosted glass effect
            from PIL import ImageFilter
            board_img = board_img.filter(ImageFilter.GaussianBlur(radius=5))
            
            # Composite board onto main image
            img = Image.alpha_composite(img, board_img)
            draw = ImageDraw.Draw(img)
        
        # Draw text with subtle shadow for better contrast
        shadow_offset = 3
        draw.multiline_text((text_x + shadow_offset, text_y + shadow_offset), 
                           wrapped_text, font=font, fill=(0, 0, 0, 120), align="center")
        
        # Draw main text
        draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill=color, align="center")
        
        # Convert to numpy array and create ImageClip
        img_array = np.array(img)
        return ImageClip(img_array, duration=self.sentence_duration)
    
    def create_typing_text_overlay(self, text: str, position: str = "center",
                                 font_size: int = 60, color: str = "white",
                                 typing_speed: float = 0.05, with_background: bool = True) -> VideoClip:
        """
        Create a text overlay with typing animation effect.
        Simply creates images with board and text already composited.
        """
        def make_frame(t):
            # Calculate how many characters to show at time t
            total_chars = len(text)
            chars_to_show = int(t / typing_speed)
            if chars_to_show > total_chars:
                chars_to_show = total_chars
            
            # Get the text to display
            display_text = text[:chars_to_show]
            
            # Add cursor if still typing
            if chars_to_show < total_chars and int(t * 2) % 2 == 0:
                display_text += "|"
            
            # Create transparent image for just the board and text area
            # Not the full screen to avoid covering the background
            return self._create_text_with_board(display_text, position, font_size, color, with_background)
        
        # Calculate duration based on typing speed
        duration = len(text) * typing_speed + 1  # +1 for completion pause
        
        return VideoClip(make_frame, duration=duration)
    
    def _create_text_with_board(self, text: str, position: str, font_size: int, 
                                color: str, with_background: bool) -> np.ndarray:
        """Helper method to create text with background board."""
        # Font setup
        font_paths = [
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "C:/Windows/Fonts/malgunbd.ttf",
            "/System/Library/Fonts/Helvetica.ttc"
        ]
        
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except:
                continue
        
        if font is None:
            font = ImageFont.load_default()
        
        # Create a small image just for measuring text
        test_img = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
        test_draw = ImageDraw.Draw(test_img)
        
        # Measure the full text (without cursor) for consistent board size
        full_text = text.rstrip('|')
        
        # Apply text wrapping
        max_text_width = int(self.width * 0.8)  # Use 80% of screen width
        wrapped_full_text = self.wrap_text(full_text, font, max_text_width, test_draw)
        
        bbox = test_draw.multiline_textbbox((0, 0), wrapped_full_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Add padding
        padding = 40
        board_width = text_width + padding * 2
        board_height = text_height + padding * 2
        
        # Calculate position
        if position == "center":
            board_x = (self.width - board_width) // 2
            board_y = (self.height - board_height) // 2
        elif position == "top":
            board_x = (self.width - board_width) // 2
            board_y = self.height // 6
        else:  # bottom
            board_x = (self.width - board_width) // 2
            board_y = self.height - (self.height // 4) - board_height // 2
        
        # Create image just for the board area, not full screen
        board_img = Image.new('RGBA', (board_width, board_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(board_img)
        
        if with_background:
            # Draw modern frosted glass effect background
            radius = 30
            draw.rounded_rectangle(
                [0, 0, board_width, board_height],
                radius=radius,
                fill=(255, 255, 255, 80)  # Light white frosted glass effect
            )
            
            # Apply blur
            from PIL import ImageFilter
            board_img = board_img.filter(ImageFilter.GaussianBlur(radius=2))
            draw = ImageDraw.Draw(board_img)
        
        # Wrap the current text (might include cursor)
        wrapped_text = self.wrap_text(text, font, max_text_width, draw)
        
        # Draw text with shadow for better contrast
        shadow_offset = 3
        draw.multiline_text((padding + shadow_offset, padding + shadow_offset), 
                           wrapped_text, font=font, fill=(0, 0, 0, 120), align="center")
        
        # Draw main text
        draw.multiline_text((padding, padding), wrapped_text, font=font, fill=color, align="center")
        
        # Now create full screen image and paste the board at the right position
        full_img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        full_img.paste(board_img, (board_x, board_y), board_img)
        
        # Convert to RGB for moviepy
        return np.array(full_img.convert('RGB'))
    
    def create_typing_text_overlay_v2(self, text: str, position: str = "center",
                                     font_size: int = 60, color: str = "white",
                                     typing_speed: float = 0.05) -> VideoClip:
        """
        Create text overlay with typing animation that preserves background.
        Uses ImageClip with mask for proper transparency.
        """
        # Font setup
        font_paths = [
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "C:/Windows/Fonts/malgunbd.ttf",
            "/System/Library/Fonts/Helvetica.ttc"
        ]
        
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except:
                continue
        
        if font is None:
            font = ImageFont.load_default()
        
        # Pre-calculate dimensions
        test_img = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
        test_draw = ImageDraw.Draw(test_img)
        bbox = test_draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Add padding
        padding = 40
        board_width = text_width + padding * 2
        board_height = text_height + padding * 2
        
        # Calculate position
        if position == "center":
            pos_x = (self.width - board_width) // 2
            pos_y = (self.height - board_height) // 2
        elif position == "top":
            pos_x = (self.width - board_width) // 2
            pos_y = self.height // 6
        else:  # bottom
            pos_x = (self.width - board_width) // 2
            pos_y = self.height - (self.height // 4) - board_height // 2
        
        def make_frame(t):
            # Calculate characters to show
            total_chars = len(text)
            chars_to_show = int(t / typing_speed)
            if chars_to_show > total_chars:
                chars_to_show = total_chars
            
            display_text = text[:chars_to_show]
            if chars_to_show < total_chars and int(t * 2) % 2 == 0:
                display_text += "|"
            
            # Create board+text image (not full screen)
            img = Image.new('RGBA', (board_width, board_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw modern frosted glass effect background
            radius = 30
            draw.rounded_rectangle(
                [0, 0, board_width, board_height],
                radius=radius,
                fill=(255, 255, 255, 80)  # Light white frosted glass effect
            )
            
            # Apply stronger blur for better frosted glass effect
            from PIL import ImageFilter
            img = img.filter(ImageFilter.GaussianBlur(radius=5))
            draw = ImageDraw.Draw(img)
            
            # Draw text with shadow for better contrast
            shadow_offset = 3
            draw.text((padding + shadow_offset, padding + shadow_offset), 
                     display_text, font=font, fill=(0, 0, 0, 120))
            draw.text((padding, padding), display_text, font=font, fill=color)
            
            return np.array(img)
        
        # Calculate duration - typing time + display time
        typing_duration = len(text) * typing_speed
        display_duration = 3.0  # Keep text displayed for 3 seconds after typing completes
        duration = typing_duration + display_duration
        
        # Create clip with proper transparency using ImageClip
        frames = []
        fps = 30  # frames per second
        total_frames = int(duration * fps)
        
        for frame_num in range(total_frames):
            t = frame_num / fps
            frames.append(make_frame(t))
        
        # Create ImageSequenceClip from frames
        from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
        clip = ImageSequenceClip(frames, fps=fps)
        clip = clip.set_position((pos_x, pos_y))
        
        return clip
    
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
        header_text = f"Sentence #{sentence_number}"
        header = self.create_text_overlay(header_text, "top", 35, "#FFD700", with_background=True)
        
        # Load audio first to calculate typing speed based on audio duration
        en_audio = AudioFileClip(en_audio_path)
        ko_audio = AudioFileClip(ko_audio_path)
        
        # Calculate typing speed to match audio duration
        # Make typing finish just before audio ends
        en_typing_speed = (en_audio.duration - 0.5) / len(en_text) if len(en_text) > 0 else 0.05
        ko_typing_speed = (ko_audio.duration - 0.5) / len(ko_text) if len(ko_text) > 0 else 0.05
        
        # Limit typing speed to reasonable range
        en_typing_speed = max(0.02, min(0.08, en_typing_speed))
        ko_typing_speed = max(0.02, min(0.08, ko_typing_speed))
        
        # Create text overlays without typing animation for faster rendering
        # TODO: Re-enable typing animation after performance optimization
        en_text_overlay = self.create_text_overlay(en_text, "center", 55, "white", with_background=True)
        ko_text_overlay = self.create_text_overlay(ko_text, "bottom", 50, "#87CEEB", with_background=True)
        
        # Create static English text for Korean section (no typing animation)
        en_text_static = self.create_text_overlay(en_text, "center", 55, "white", with_background=True)
        
        # Calculate timings with longer pauses for learning
        en_typing_duration = en_text_overlay.duration
        ko_typing_duration = ko_text_overlay.duration
        en_audio_duration = en_audio.duration
        ko_audio_duration = ko_audio.duration
        
        # Longer pauses for better learning experience
        pause_after_typing = 1.0  # Pause after typing completes
        pause_after_audio = 2.0   # Pause after audio completes for comprehension
        pause_before_repeat = 1.0  # Pause before repeating English
        
        # English section timing
        en_text_start = 0
        en_audio_start = 0.3  # Start audio shortly after typing begins
        en_section_duration = en_audio_start + en_audio_duration + pause_after_audio
        
        # Korean section timing  
        ko_text_start = en_section_duration
        ko_audio_start = ko_text_start + 0.3
        ko_section_duration = 0.3 + ko_audio_duration + pause_after_audio
        
        # English repeat section timing
        en_repeat_start = en_section_duration + ko_section_duration
        en_repeat_audio_start = en_repeat_start + pause_before_repeat
        en_repeat_section_duration = pause_before_repeat + en_audio_duration + pause_after_audio
        
        total_duration = en_section_duration + ko_section_duration + en_repeat_section_duration
        
        # Set timings for text and audio
        # English typing animation only during English section
        en_text_timed = en_text_overlay.set_start(en_text_start).set_duration(en_section_duration)
        # Static English text during Korean section
        en_text_static_timed = en_text_static.set_start(ko_text_start).set_duration(ko_section_duration)
        # Static English text during English repeat section
        en_text_static_repeat = en_text_static.set_start(en_repeat_start).set_duration(en_repeat_section_duration)
        ko_text_timed = ko_text_overlay.set_start(ko_text_start)
        # Korean text also visible during English repeat section
        ko_text_static = self.create_text_overlay(ko_text, "bottom", 50, "#87CEEB", with_background=True)
        ko_text_static_timed = ko_text_static.set_start(en_repeat_start).set_duration(en_repeat_section_duration)
        
        en_audio_timed = en_audio.set_start(en_audio_start)
        ko_audio_timed = ko_audio.set_start(ko_audio_start)
        en_audio_repeat = en_audio.set_start(en_repeat_audio_start)
        
        # Combine audio
        audio = CompositeAudioClip([en_audio_timed, ko_audio_timed, en_audio_repeat])
        
        # Update background duration
        background = background.set_duration(total_duration)
        header = header.set_duration(total_duration)
        
        # Composite video
        video = CompositeVideoClip([
            background,
            header.set_opacity(0.95),
            en_text_timed.crossfadein(0.3),
            en_text_static_timed,  # Static English text during Korean section
            ko_text_timed.crossfadein(0.3),
            en_text_static_repeat,  # Static English text during English repeat
            ko_text_static_timed    # Static Korean text during English repeat
        ])
        
        # Set audio
        video = video.set_audio(audio)
        
        return video
    
    def create_intro_clip(self, title: str, subtitle: str) -> VideoClip:
        """Create an intro clip for the video with dynamic animations."""
        import numpy as np
        import random
        from datetime import datetime
        
        # Create animated gradient background based on time of day
        hour = datetime.now().hour
        if 5 <= hour < 12:  # Morning - sunrise colors
            colors_start = [(255, 94, 77), (255, 127, 80)]  # Coral/Peach
            colors_end = [(255, 206, 84), (255, 239, 159)]  # Golden/Light yellow
        elif 12 <= hour < 17:  # Afternoon - bright sky
            colors_start = [(135, 206, 235), (176, 224, 230)]  # Sky blue
            colors_end = [(255, 255, 255), (240, 248, 255)]  # White/Alice blue
        elif 17 <= hour < 20:  # Evening - sunset
            colors_start = [(255, 94, 77), (255, 127, 80)]  # Coral/Peach
            colors_end = [(147, 112, 219), (138, 43, 226)]  # Purple/Violet
        else:  # Night - dark blue
            colors_start = [(25, 25, 112), (0, 0, 128)]  # Midnight/Navy blue
            colors_end = [(72, 61, 139), (75, 0, 130)]  # Dark slate/Indigo
        
        def make_frame(t):
            # Animated gradient that shifts over time
            gradient = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Create smooth color transition
            for y in range(self.height):
                ratio = y / self.height
                # Add time-based animation
                shift = np.sin(t * 0.5) * 0.1
                ratio = max(0, min(1, ratio + shift))
                
                # Interpolate between colors
                color_idx = int(t * 0.3) % 2
                start_color = colors_start[color_idx]
                end_color = colors_end[color_idx]
                
                for c in range(3):
                    gradient[y, :, c] = int(start_color[c] + (end_color[c] - start_color[c]) * ratio)
            
            return gradient
        
        # Create static gradient background instead of animated for better performance
        gradient = make_frame(0)  # Use first frame as static background
        background = ImageClip(gradient).set_duration(4)
        
        # Create title with fade effect instead of typing for better performance
        title_clip = self.create_text_overlay(title, "center", 80, "white", with_background=True)
        title_clip = title_clip.set_duration(3).set_start(0.3).crossfadein(0.5)
        
        # Create subtitle with slide-in animation
        subtitle_clip = self.create_text_overlay(subtitle, "bottom", 40, "#FFD700", with_background=True)
        subtitle_clip = subtitle_clip.set_duration(3).set_start(1.0)
        # Add slide-in effect from bottom
        subtitle_clip = subtitle_clip.set_position(lambda t: ('center', 
                                                            self.height - 100 + (200 * max(0, 1 - t * 2))))
        
        # Add decorative elements - animated circles
        decorations = []
        for i in range(3):
            # Create small circle decoration
            circle_size = random.randint(50, 100)
            circle_img = Image.new('RGBA', (circle_size, circle_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(circle_img)
            draw.ellipse([0, 0, circle_size, circle_size], 
                        fill=(255, 255, 255, 30))  # Semi-transparent white
            
            circle_clip = ImageClip(np.array(circle_img)).set_duration(4)
            # Random starting position
            start_x = random.randint(0, self.width - circle_size)
            start_y = random.randint(0, self.height - circle_size)
            # Floating animation
            circle_clip = circle_clip.set_position(
                lambda t, sx=start_x, sy=start_y: 
                (sx + np.sin(t * 2) * 30, sy - t * 50)
            )
            # Create fade effect manually since set_opacity doesn't accept functions
            circle_clip = circle_clip.crossfadein(0.5).crossfadeout(2.0)
            decorations.append(circle_clip)
        
        # Composite all elements
        intro = CompositeVideoClip([
            background,
            *decorations,
            title_clip.crossfadein(0.5),
            subtitle_clip.crossfadein(0.5)
        ])
        
        # Add overall fade in effect
        intro = intro.crossfadein(0.5)
        
        return intro
    
    def create_animated_subscribe_button(self) -> VideoClip:
        """Create an animated subscribe button without artifacts."""
        # Create a clean subscribe button overlay
        button_width = 300
        button_height = 70
        
        # Create the button image
        img = Image.new('RGBA', (button_width + 40, button_height + 40), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw shadow
        draw.rounded_rectangle(
            [5, 5, button_width + 5, button_height + 5],
            radius=35,
            fill=(0, 0, 0, 80)
        )
        
        # Draw main button
        draw.rounded_rectangle(
            [0, 0, button_width, button_height],
            radius=35,
            fill=(204, 0, 0)  # YouTube red
        )
        
        # Add text
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
        except:
            font = ImageFont.load_default()
            
        text = "SUBSCRIBE"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (button_width - text_width) // 2
        text_y = (button_height - text_height) // 2
        draw.text((text_x, text_y), text, font=font, fill="white")
        
        # Convert to clip
        button_clip = ImageClip(np.array(img)).set_duration(5)
        
        # Position at center
        button_x = (self.width - button_width) // 2
        button_y = self.height // 2 + 20
        button_clip = button_clip.set_position((button_x - 20, button_y - 20))
        
        # Add subtle fade in
        button_clip = button_clip.crossfadein(0.5)
        
        return button_clip
    
    def create_bell_animation(self) -> VideoClip:
        """Create a clean notification bell icon."""
        # Create bell icon
        bell_size = 50
        img = Image.new('RGBA', (bell_size + 20, bell_size + 20), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw bell shape with cleaner design
        # Bell top (dome)
        draw.ellipse([10, 10, bell_size + 10, bell_size - 5], 
                    fill=(255, 255, 255))
        
        # Bell bottom
        draw.rectangle([15, bell_size - 10, bell_size + 5, bell_size + 5], 
                      fill=(255, 255, 255))
        
        # Bell clapper
        draw.ellipse([bell_size // 2 - 3, bell_size + 3, 
                     bell_size // 2 + 7, bell_size + 13], 
                    fill=(255, 255, 255))
        
        # Convert to clip
        bell_clip = ImageClip(np.array(img)).set_duration(4)
        
        # Position next to subscribe button
        bell_x = self.width // 2 + 180
        bell_y = self.height // 2 + 35
        bell_clip = bell_clip.set_position((bell_x, bell_y))
        
        # Add fade in with delay
        bell_clip = bell_clip.set_start(0.3).crossfadein(0.3)
        
        return bell_clip
    
    def create_like_button(self) -> VideoClip:
        """Create a like button with thumb up icon."""
        # Create like button
        button_width = 120
        button_height = 50
        
        img = Image.new('RGBA', (button_width + 20, button_height + 20), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw button background
        draw.rounded_rectangle(
            [0, 0, button_width, button_height],
            radius=25,
            fill=(50, 50, 50)
        )
        
        # Draw thumb up icon (simple version)
        thumb_x = 15
        thumb_y = 15
        # Thumb
        draw.rectangle([thumb_x, thumb_y, thumb_x + 15, thumb_y + 20], 
                      fill=(255, 255, 255))
        # Thumb tip
        draw.ellipse([thumb_x + 2, thumb_y - 5, thumb_x + 13, thumb_y + 5], 
                    fill=(255, 255, 255))
        
        # Add text
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        except:
            font = ImageFont.load_default()
            
        text = "LIKE"
        draw.text((thumb_x + 25, thumb_y + 2), text, font=font, fill="white")
        
        # Convert to clip
        like_clip = ImageClip(np.array(img)).set_duration(5)
        
        # Position below subscribe button
        like_x = (self.width - button_width) // 2 - 10
        like_y = self.height // 2 + 110
        like_clip = like_clip.set_position((like_x, like_y))
        
        # Add fade in with delay
        like_clip = like_clip.set_start(0.5).crossfadein(0.3)
        
        return like_clip
    
    def create_outro_clip(self) -> VideoClip:
        """Create an outro clip with dynamic animations and interactive elements."""
        import numpy as np
        import random
        
        # Create animated particle background
        def make_particle_background(t):
            # Dark to light gradient for outro
            gradient = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Create radial gradient from center
            center_x, center_y = self.width // 2, self.height // 2
            for y in range(self.height):
                for x in range(0, self.width, 4):  # Skip pixels for performance
                    # Calculate distance from center
                    dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                    max_dist = np.sqrt(center_x**2 + center_y**2)
                    ratio = dist / max_dist
                    
                    # Pulsing effect
                    pulse = np.sin(t * 2) * 0.1 + 0.9
                    ratio *= pulse
                    
                    # Color based on distance (purple to blue gradient)
                    r = int(147 * (1 - ratio) + 25 * ratio)
                    g = int(112 * (1 - ratio) + 25 * ratio) 
                    b = int(219 * (1 - ratio) + 112 * ratio)
                    
                    gradient[y, x:x+4] = [r, g, b]
            
            return gradient
        
        # Create static gradient background for better performance
        gradient = make_particle_background(0)  # Use first frame as static background
        background = ImageClip(gradient).set_duration(6)
        
        # Create thank you message with wave animation
        thank_you_text = "Thank you for watching!"
        thank_you_clip = self.create_text_overlay(thank_you_text, "top", 70, "white", with_background=True)
        thank_you_clip = thank_you_clip.set_duration(6)
        # Wave animation for text
        thank_you_clip = thank_you_clip.set_position(
            lambda t: ('center', 100 + np.sin(t * 3) * 20)
        )
        
        # Create animated subscribe section
        subscribe_container = self._create_animated_subscribe_section()
        
        # Create next video teaser
        next_video_text = "See you in the next lesson! 📚"
        next_video_clip = self.create_text_overlay(next_video_text, "bottom", 35, "#87CEEB", with_background=True)
        next_video_clip = next_video_clip.set_duration(4).set_start(2)
        next_video_clip = next_video_clip.crossfadein(0.5)
        
        # Add floating emoji decorations
        emojis = ["⭐", "💡", "🎯", "✨"]
        emoji_clips = []
        for i, emoji in enumerate(emojis):
            emoji_clip = self.create_text_overlay(emoji, "center", 40, "white", with_background=False)
            emoji_clip = emoji_clip.set_duration(6)
            
            # Random starting position around the edges
            if i % 2 == 0:
                start_x = random.choice([50, self.width - 100])
                start_y = random.randint(200, self.height - 200)
            else:
                start_x = random.randint(100, self.width - 100)
                start_y = random.choice([50, self.height - 100])
            
            # Floating animation
            emoji_clip = emoji_clip.set_position(
                lambda t, sx=start_x, sy=start_y, idx=i: 
                (sx + np.sin(t * 2 + idx) * 50, 
                 sy + np.cos(t * 1.5 + idx) * 30)
            )
            # Fade in and out effects
            emoji_clip = emoji_clip.crossfadein(1.0).crossfadeout(1.0)
            emoji_clips.append(emoji_clip)
        
        # Composite all elements
        outro = CompositeVideoClip([
            background,
            *emoji_clips,
            thank_you_clip.crossfadein(0.5),
            subscribe_container,
            next_video_clip
        ])
        
        # Add overall fade out effect
        outro = outro.crossfadeout(1.0)
        
        return outro
    
    def _create_animated_subscribe_section(self) -> VideoClip:
        """Create an animated subscribe button section with interactive feel."""
        # Main container position
        container_y = self.height // 2
        
        # Subscribe button with pulse animation
        subscribe_btn = self.create_animated_subscribe_button()
        subscribe_btn = subscribe_btn.set_position(
            lambda t: ((self.width - 300) // 2, 
                      container_y + np.sin(t * 4) * 5)  # Subtle pulse
        )
        
        # Bell icon with shake animation
        bell = self.create_bell_animation()
        bell = bell.set_position(
            lambda t: (self.width // 2 + 180 + np.sin(t * 20) * 3 if 1 < t < 1.5 else self.width // 2 + 180,
                      container_y + 35)
        )
        
        # Like button with bounce animation
        like_btn = self.create_like_button()
        like_btn = like_btn.set_position(
            lambda t: ((self.width - 120) // 2 - 10,
                      container_y + 110 - abs(np.sin(t * 3)) * 10 if t < 2 else container_y + 110)
        )
        
        # Create "Don't forget to" text
        reminder_text = "Don't forget to"
        reminder_clip = self.create_text_overlay(reminder_text, "center", 30, "#FFD700", with_background=True)
        reminder_clip = reminder_clip.set_duration(6)
        reminder_clip = reminder_clip.set_position(('center', container_y - 80))
        reminder_clip = reminder_clip.crossfadein(0.3)
        
        # Combine all subscribe section elements
        return CompositeVideoClip([
            reminder_clip,
            subscribe_btn,
            bell,
            like_btn
        ])
    
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
            try:
                print(f"🎵 Adding background music from: {background_music_path}")
                bg_music = AudioFileClip(background_music_path)
                print(f"   Music duration: {bg_music.duration:.1f}s, Video duration: {final_video.duration:.1f}s")
                
                # Ensure background music matches video duration
                if bg_music.duration > final_video.duration:
                    bg_music = bg_music.subclip(0, final_video.duration)
                elif bg_music.duration < final_video.duration:
                    # If music is shorter, loop it manually
                    loops_needed = int(final_video.duration / bg_music.duration) + 1
                    bg_music_clips = [bg_music] * loops_needed
                    bg_music = concatenate_audioclips(bg_music_clips)
                    bg_music = bg_music.subclip(0, final_video.duration)
                
                # Apply volume adjustment
                print(f"   Applying volume: {config.music_volume}")
                bg_music = bg_music.volumex(config.music_volume)
                
                # Add fade in/out for smoother experience
                bg_music = bg_music.audio_fadein(2.0).audio_fadeout(2.0)
                
                # Mix with existing audio
                if final_video.audio:
                    final_audio = CompositeAudioClip([final_video.audio, bg_music])
                else:
                    final_audio = bg_music
                    
                final_video = final_video.set_audio(final_audio)
                print(f"✅ Background music added successfully")
            except Exception as e:
                print(f"❌ Warning: Could not add background music: {e}")
                # Continue without background music if there's an error
        else:
            print(f"⚠️ No background music path provided or file doesn't exist: {background_music_path}")
        
        # Write the final video with progress tracking
        print(f"🎬 Starting video rendering... This may take a few minutes.")
        print(f"📊 Total duration: {final_video.duration:.1f} seconds")
        
        final_video.write_videofile(
            output_path,
            fps=30,  # Standard YouTube FPS
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            preset='slow',  # Better quality encoding
            bitrate='8000k',  # High bitrate for 1080p (8 Mbps)
            audio_bitrate='192k',  # High quality audio
            threads=4,  # Use multiple threads
            logger='bar'  # Show progress bar
        )
        
        # Clean up
        final_video.close()
        
        return output_path