"""Modern 2025 YouTube-style assets generator."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from typing import List, Optional
import random
from datetime import datetime


def get_font(size: int, weight: str = "regular"):
    """Get a modern font that supports Korean characters."""
    font_paths = {
        "regular": [
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
            "/System/Library/Fonts/Helvetica.ttc",
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        ],
        "bold": [
            "/System/Library/Fonts/Supplemental/Arial Black.ttf",
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
        ]
    }
    
    paths = font_paths.get(weight, font_paths["regular"])
    
    for font_path in paths:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            continue
    
    return ImageFont.load_default()


def create_modern_intro(width: int = 1920, height: int = 1080):
    """Create a modern, minimalist intro with variations."""
    # Choose a random style
    style = random.choice(['gradient', 'circles', 'lines', 'dots', 'wave'])
    
    # Create dark background
    img = Image.new('RGB', (width, height), (15, 15, 15))
    draw = ImageDraw.Draw(img)
    
    # Add different background patterns based on style
    if style == 'gradient':
        # Diagonal gradient effect
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        for i in range(width):
            alpha = int(255 * (i / width) * 0.3)
            overlay_draw.line([(i, 0), (i, height)], 
                             fill=(139, 92, 246, alpha))  # Purple accent
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
    elif style == 'circles':
        # Random circles pattern
        for _ in range(5):
            x = random.randint(0, width)
            y = random.randint(0, height)
            radius = random.randint(100, 300)
            opacity = random.randint(10, 30)
            circle_color = (139, 92, 246, opacity)
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=circle_color)
            overlay = overlay.filter(ImageFilter.GaussianBlur(radius=50))
            img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
            
    elif style == 'lines':
        # Geometric lines pattern
        for i in range(0, width, 100):
            opacity = random.randint(20, 60)
            draw.line([(i, 0), (i + height//2, height)], fill=(139, 92, 246, opacity), width=2)
            
    elif style == 'dots':
        # Dot pattern
        for x in range(50, width, 80):
            for y in range(50, height, 80):
                if random.random() > 0.7:
                    radius = random.randint(2, 8)
                    opacity = random.randint(100, 200)
                    draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                               fill=(139, 92, 246, opacity))
                    
    elif style == 'wave':
        # Wave pattern
        for y in range(0, height, 40):
            points = []
            for x in range(0, width + 50, 50):
                wave_y = y + np.sin(x / 100) * 20
                points.append((x, wave_y))
            if len(points) > 1:
                draw.line(points, fill=(139, 92, 246, 40), width=2)
    
    draw = ImageDraw.Draw(img)
    
    # Modern typography - large, bold, minimal
    title_font = get_font(120, "bold")
    subtitle_font = get_font(40)
    
    # Choose layout variation
    layout = random.choice(['left', 'center', 'right'])
    
    # Main title with modern spacing
    title = "DAILY"
    title2 = "ENGLISH"
    
    if layout == 'left':
        x_offset = 120
        y_start = height // 3
        align = 'left'
    elif layout == 'center':
        x_offset = width // 2
        y_start = height // 3
        align = 'center'
    else:  # right
        x_offset = width - 120
        y_start = height // 3
        align = 'right'
    
    # Draw DAILY
    bbox = draw.textbbox((0, 0), title, font=title_font)
    text_width = bbox[2] - bbox[0]
    if align == 'center':
        x_pos = x_offset - text_width // 2
    elif align == 'right':
        x_pos = x_offset - text_width
    else:
        x_pos = x_offset
        
    draw.text((x_pos, y_start), title, font=title_font, fill=(255, 255, 255))
    
    # Draw ENGLISH with accent color
    bbox2 = draw.textbbox((0, 0), title2, font=title_font)
    text_width2 = bbox2[2] - bbox2[0]
    if align == 'center':
        x_pos2 = x_offset - text_width2 // 2
    elif align == 'right':
        x_pos2 = x_offset - text_width2
    else:
        x_pos2 = x_offset
        
    draw.text((x_pos2, y_start + 130), title2, font=title_font, fill=(139, 92, 246))
    
    # Modern subtitle with lighter weight
    subtitle = "Essential sentences for Korean learners"
    bbox3 = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    text_width3 = bbox3[2] - bbox3[0]
    if align == 'center':
        x_pos3 = x_offset - text_width3 // 2
    elif align == 'right':
        x_pos3 = x_offset - text_width3
    else:
        x_pos3 = x_offset
        
    draw.text((x_pos3, y_start + 280), subtitle, font=subtitle_font, fill=(180, 180, 180))
    
    # Add modern geometric element
    accent_y = y_start + 350
    if align == 'center':
        accent_x = x_offset - 100
    elif align == 'right':
        accent_x = x_offset - 200
    else:
        accent_x = x_offset
        
    draw.rectangle([(accent_x, accent_y), (accent_x + 200, accent_y + 4)], 
                  fill=(139, 92, 246))
    
    # Add date/episode info
    date_font = get_font(25)
    today = datetime.now().strftime("%B %d, %Y")
    draw.text((50, 50), today, font=date_font, fill=(100, 100, 100))
    
    # Minimal branding in corner
    brand_font = get_font(30)
    brand = "MECASPACE"
    draw.text((width - 250, height - 80), brand, font=brand_font, fill=(120, 120, 120))
    
    return img


def create_modern_outro(width: int = 1920, height: int = 1080):
    """Create a modern outro with clean design."""
    # Dark background
    img = Image.new('RGB', (width, height), (15, 15, 15))
    
    # Add subtle texture
    noise = Image.new('RGB', (width, height))
    noise_pixels = noise.load()
    for i in range(width):
        for j in range(height):
            val = np.random.randint(10, 25)
            noise_pixels[i, j] = (val, val, val)
    
    img = Image.blend(img, noise, 0.1)
    draw = ImageDraw.Draw(img)
    
    # Modern centered layout
    center_x = width // 2
    
    # Thank you text - modern, minimal
    thanks_font = get_font(80, "bold")
    thanks = "THANKS FOR"
    thanks2 = "WATCHING"
    
    # Center align text
    bbox1 = draw.textbbox((0, 0), thanks, font=thanks_font)
    bbox2 = draw.textbbox((0, 0), thanks2, font=thanks_font)
    
    thanks_x = center_x - (bbox1[2] - bbox1[0]) // 2
    thanks2_x = center_x - (bbox2[2] - bbox2[0]) // 2
    
    y_pos = height // 3 - 50
    
    draw.text((thanks_x, y_pos), thanks, font=thanks_font, fill=(255, 255, 255))
    draw.text((thanks2_x, y_pos + 90), thanks2, font=thanks_font, fill=(139, 92, 246))
    
    # Modern CTA section with better spacing
    cta_y = height // 2 + 20
    
    # Subscribe button - modern flat design
    btn_width = 280
    btn_height = 56
    btn_x = center_x - btn_width // 2
    
    # Button background with rounded corners
    # Create a rounded rectangle
    corner_radius = 28
    # Draw rounded rectangle manually for better control
    draw.rounded_rectangle(
        [(btn_x, cta_y), (btn_x + btn_width, cta_y + btn_height)],
        radius=corner_radius,
        fill=(204, 0, 0)
    )
    
    # Button text
    btn_font = get_font(26, "bold")
    btn_text = "SUBSCRIBE"
    bbox = draw.textbbox((0, 0), btn_text, font=btn_font)
    text_x = center_x - (bbox[2] - bbox[0]) // 2
    text_y = cta_y + (btn_height - (bbox[3] - bbox[1])) // 2
    
    draw.text((text_x, text_y), btn_text, font=btn_font, fill=(255, 255, 255))
    
    # Modern icons section with better spacing
    icon_y = cta_y + 80
    icon_font = get_font(22)
    
    # Like and Bell in a single line with better spacing
    combined_text = "👍 LIKE     🔔 NOTIFY"
    bbox = draw.textbbox((0, 0), combined_text, font=icon_font)
    icon_x = center_x - (bbox[2] - bbox[0]) // 2
    
    draw.text((icon_x, icon_y), combined_text, font=icon_font, fill=(180, 180, 180))
    
    # Bottom section - next video teaser
    bottom_font = get_font(22)
    next_text = "NEW VIDEO TOMORROW"
    bbox = draw.textbbox((0, 0), next_text, font=bottom_font)
    next_x = center_x - (bbox[2] - bbox[0]) // 2
    
    draw.text((next_x, height - 120), next_text, font=bottom_font, fill=(100, 100, 100))
    
    # Minimal branding
    brand_font = get_font(30)
    draw.text((center_x - 70, height - 60), "MECASPACE", font=brand_font, fill=(80, 80, 80))
    
    return img


def create_modern_thumbnail(
    day_number: int,
    sentences: List[tuple],
    output_path: str,
    background_image_path: Optional[str] = None
) -> str:
    """Create a modern YouTube thumbnail."""
    width, height = 1280, 720
    
    # Create base image
    if background_image_path and os.path.exists(background_image_path):
        img = Image.open(background_image_path)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        # Apply modern dark overlay with gradient
        overlay = Image.new('RGBA', (width, height))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Gradient from left (darker) to right (lighter)
        for x in range(width):
            alpha = int(220 - (x / width) * 100)
            overlay_draw.line([(x, 0), (x, height)], fill=(0, 0, 0, alpha))
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    else:
        # Modern gradient background
        img = Image.new('RGB', (width, height))
        pixels = img.load()
        
        for x in range(width):
            for y in range(height):
                # Diagonal gradient
                r = int(15 + (x + y) / (width + height) * 30)
                g = int(15 + (x + y) / (width + height) * 25)
                b = int(25 + (x + y) / (width + height) * 40)
                pixels[x, y] = (r, g, b)
    
    draw = ImageDraw.Draw(img)
    
    # Modern left-aligned layout
    left_margin = 80
    
    # Day number - modern badge style
    day_font = get_font(140, "bold")
    day_text = f"{day_number}"
    
    # Draw day number with accent
    draw.text((left_margin, 80), "DAY", font=get_font(40), fill=(139, 92, 246))
    draw.text((left_margin, 130), day_text, font=day_font, fill=(255, 255, 255))
    
    # Main content - big number
    number_font = get_font(200, "bold")
    number = f"{len(sentences)}"
    
    # Draw large number in center-right
    draw.text((width - 400, height // 2 - 150), number, font=number_font, fill=(139, 92, 246))
    
    # Modern description
    desc_font = get_font(50, "bold")
    desc_text = "ESSENTIAL"
    desc_text2 = "SENTENCES"
    
    draw.text((left_margin, height // 2 + 20), desc_text, font=desc_font, fill=(255, 255, 255))
    draw.text((left_margin, height // 2 + 80), desc_text2, font=desc_font, fill=(255, 255, 255))
    
    # Korean text - smaller, modern
    kr_font = get_font(35)
    kr_text = "필수 영어 문장"
    draw.text((left_margin, height // 2 + 150), kr_text, font=kr_font, fill=(180, 180, 180))
    
    # Modern branding - bottom right corner
    brand_bg_x = width - 200
    brand_bg_y = height - 80
    
    # Subtle brand background
    draw.rectangle([(brand_bg_x - 10, brand_bg_y - 10), 
                   (width - 20, height - 20)], 
                  fill=(25, 25, 25))
    
    brand_font = get_font(24)
    draw.text((brand_bg_x, brand_bg_y), "MECASPACE", font=brand_font, fill=(255, 255, 255))
    
    # Add modern accent line
    draw.rectangle([(left_margin, height - 100), (left_margin + 300, height - 96)], 
                  fill=(139, 92, 246))
    
    # Save with high quality
    img.save(output_path, 'PNG', quality=95, optimize=True)
    print(f"✅ Modern thumbnail created: {output_path}")
    
    return output_path


def main():
    """Create and save modern assets."""
    assets_dir = os.path.join(os.path.dirname(__file__), '../../assets/modern')
    os.makedirs(assets_dir, exist_ok=True)
    
    # Create modern intro
    intro = create_modern_intro()
    intro_path = os.path.join(assets_dir, 'intro.png')
    intro.save(intro_path, 'PNG', quality=95)
    print(f"✅ Modern intro created: {intro_path}")
    
    # Create modern outro
    outro = create_modern_outro()
    outro_path = os.path.join(assets_dir, 'outro.png')
    outro.save(outro_path, 'PNG', quality=95)
    print(f"✅ Modern outro created: {outro_path}")
    
    # Test thumbnail
    test_sentences = [
        ("Test sentence 1", "테스트 문장 1"),
        ("Test sentence 2", "테스트 문장 2"),
        ("Test sentence 3", "테스트 문장 3")
    ]
    
    thumbnail_path = os.path.join(assets_dir, 'test_thumbnail.png')
    create_modern_thumbnail(577, test_sentences, thumbnail_path)
    
    return intro_path, outro_path


if __name__ == "__main__":
    main()