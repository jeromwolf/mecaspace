"""Generate YouTube thumbnails for videos."""
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from typing import List, Optional
from .modern_assets import create_modern_thumbnail
import random


def get_font(size: int):
    """Get a font that supports Korean characters."""
    font_paths = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
        "C:/Windows/Fonts/malgunbd.ttf",
        "/System/Library/Fonts/Helvetica.ttc"
    ]
    
    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            continue
    
    return ImageFont.load_default()


def create_gradient_background(width: int, height: int, color1: tuple, color2: tuple) -> Image:
    """Create a gradient background image."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))
    
    return img


def generate_thumbnail(
    day_number: int,
    sentences: List[tuple],
    output_path: str,
    background_image_path: Optional[str] = None
) -> str:
    """Generate a modern YouTube thumbnail."""
    return create_modern_thumbnail(day_number, sentences, output_path, background_image_path)


def generate_thumbnail_old(
    day_number: int,
    sentences: List[tuple],
    output_path: str,
    background_image_path: Optional[str] = None
) -> str:
    """
    Generate a YouTube thumbnail for the video.
    
    Args:
        day_number: The day number for the study series
        sentences: List of (english, korean) sentence pairs
        output_path: Path where the thumbnail will be saved
        background_image_path: Optional custom background image
    
    Returns:
        Path to the generated thumbnail
    """
    # YouTube recommends 1280x720 for thumbnails
    width, height = 1280, 720
    
    if background_image_path and os.path.exists(background_image_path):
        # Use provided background
        img = Image.open(background_image_path)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        # Add dark overlay for better text visibility
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 180))
        img.paste(overlay, (0, 0), overlay)
    else:
        # Create gradient background
        img = create_gradient_background(width, height, (30, 30, 80), (80, 30, 120))
    
    draw = ImageDraw.Draw(img)
    
    # Add decorative elements
    # Draw circles for visual interest
    for i in range(3):
        x = np.random.randint(100, width - 100)
        y = np.random.randint(100, height - 100)
        radius = np.random.randint(30, 60)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], 
                    fill=(255, 255, 255, 30))
    
    # Add day number badge
    badge_font = get_font(60)
    day_text = f"Day {day_number}"
    bbox = draw.textbbox((0, 0), day_text, font=badge_font)
    badge_width = bbox[2] - bbox[0] + 40
    badge_height = bbox[3] - bbox[1] + 20
    
    # Draw badge background
    badge_x = width - badge_width - 40
    badge_y = 40
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_width, badge_y + badge_height],
        radius=25,
        fill=(255, 215, 0)  # Gold color
    )
    
    # Draw day number
    text_x = badge_x + 20
    text_y = badge_y + 10
    draw.text((text_x + 2, text_y + 2), day_text, font=badge_font, fill=(0, 0, 0, 100))  # Shadow
    draw.text((text_x, text_y), day_text, font=badge_font, fill="black")
    
    # Main title
    title_font = get_font(80)
    title_text = "영어 공부"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    title_y = height // 4
    
    # Draw title with shadow
    draw.text((title_x + 4, title_y + 4), title_text, font=title_font, fill=(0, 0, 0, 150))
    draw.text((title_x, title_y), title_text, font=title_font, fill="white")
    
    # Subtitle
    subtitle_font = get_font(50)
    subtitle_text = "Daily English Study"
    bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 100
    
    draw.text((subtitle_x + 3, subtitle_y + 3), subtitle_text, font=subtitle_font, fill=(0, 0, 0, 150))
    draw.text((subtitle_x, subtitle_y), subtitle_text, font=subtitle_font, fill="#FFD700")
    
    # Number of sentences
    count_font = get_font(100)
    count_text = f"{len(sentences)}"
    bbox = draw.textbbox((0, 0), count_text, font=count_font)
    count_width = bbox[2] - bbox[0]
    count_x = (width - count_width) // 2
    count_y = height // 2 + 20
    
    # Draw large number with glow effect
    for i in range(5, 0, -1):
        alpha = int(100 / i)
        offset = i * 2
        draw.text((count_x - offset, count_y - offset), count_text, 
                 font=count_font, fill=(255, 255, 255, alpha))
    draw.text((count_x, count_y), count_text, font=count_font, fill="white")
    
    # "Sentences" text below the number
    desc_font = get_font(40)
    desc_text = "Essential Sentences"
    bbox = draw.textbbox((0, 0), desc_text, font=desc_font)
    desc_width = bbox[2] - bbox[0]
    desc_x = (width - desc_width) // 2
    desc_y = count_y + 110
    
    draw.text((desc_x, desc_y), desc_text, font=desc_font, fill=(200, 200, 200))
    
    # Korean description
    kr_desc_font = get_font(35)
    kr_desc_text = "필수 영어 문장"
    bbox = draw.textbbox((0, 0), kr_desc_text, font=kr_desc_font)
    kr_desc_width = bbox[2] - bbox[0]
    kr_desc_x = (width - kr_desc_width) // 2
    kr_desc_y = desc_y + 50
    
    draw.text((kr_desc_x, kr_desc_y), kr_desc_text, font=kr_desc_font, fill=(200, 200, 200))
    
    # Add Mecaspace branding at bottom
    brand_font = get_font(30)
    brand_text = "메카스페이스"
    bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
    brand_width = bbox[2] - bbox[0]
    brand_x = width - brand_width - 40
    brand_y = height - 80
    
    # Draw brand background
    draw.rounded_rectangle(
        [brand_x - 20, brand_y - 10, width - 20, brand_y + 40],
        radius=20,
        fill=(0, 0, 0, 180)
    )
    
    draw.text((brand_x, brand_y), brand_text, font=brand_font, fill=(255, 255, 255))
    
    # Add channel handle
    handle_font = get_font(20)
    handle_text = "@mecca-.-space"
    draw.text((brand_x, brand_y + 35), handle_text, font=handle_font, fill=(200, 200, 200))
    
    # Save thumbnail
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ Thumbnail created: {output_path}")
    
    return output_path


def generate_thumbnail_from_video_path(video_path: str, sentences: List[tuple]) -> str:
    """
    Generate thumbnail based on video filename.
    
    Args:
        video_path: Path to the video file
        sentences: List of (english, korean) sentence pairs
    
    Returns:
        Path to the generated thumbnail
    """
    # Extract day number from filename if possible
    filename = os.path.basename(video_path)
    day_number = 1  # Default
    
    # Try to extract day number from filename patterns
    import re
    
    # Pattern 1: "Day 577" or "day577"
    day_match = re.search(r'[Dd]ay\s*(\d+)', filename)
    if day_match:
        day_number = int(day_match.group(1))
    else:
        # Pattern 2: "#577" 
        hash_match = re.search(r'#(\d+)', filename)
        if hash_match:
            day_number = int(hash_match.group(1))
        else:
            # Pattern 3: Just numbers in filename
            num_match = re.search(r'(\d+)', filename)
            if num_match:
                day_number = int(num_match.group(1))
    
    # Create thumbnail path (same directory and name as video, but .png)
    thumbnail_path = video_path.replace('.mp4', '_thumbnail.png')
    
    # Try to use a random image from the video as background
    background_path = None
    image_dir = os.path.join(os.path.dirname(os.path.dirname(video_path)), 'images')
    if os.path.exists(image_dir):
        images = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]
        if images:
            # Sort by modification time and use recent images
            images.sort(key=lambda x: os.path.getmtime(os.path.join(image_dir, x)), reverse=True)
            # Pick a random image from the most recent ones
            recent_images = images[:10] if len(images) > 10 else images
            background_path = os.path.join(image_dir, random.choice(recent_images))
    
    return generate_thumbnail(day_number, sentences, thumbnail_path, background_path)