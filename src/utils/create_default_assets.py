"""Create default intro and outro images for videos."""
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np


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


def create_intro_image(width: int = 1920, height: int = 1080):
    """Create default intro image with Mecaspace branding."""
    # Create gradient background (dark blue to purple)
    img = create_gradient_background(width, height, (25, 25, 112), (75, 0, 130))
    draw = ImageDraw.Draw(img)
    
    # Add decorative elements
    # Draw circles for visual interest
    for i in range(5):
        x = np.random.randint(100, width - 100)
        y = np.random.randint(100, height - 100)
        radius = np.random.randint(20, 80)
        opacity = np.random.randint(20, 60)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], 
                    fill=(255, 255, 255, opacity))
    
    # Add Mecaspace logo/text in top left
    logo_font = get_font(40)
    logo_text = "메카스페이스"
    draw.text((50, 50), logo_text, font=logo_font, fill=(255, 255, 255, 200))
    
    # Add channel handle below
    handle_font = get_font(25)
    handle_text = "@mecca-.-space"
    draw.text((50, 100), handle_text, font=handle_font, fill=(255, 255, 255, 150))
    
    # Add main title
    title_font = get_font(100)
    subtitle_font = get_font(50)
    
    # Main title
    title = "Daily English Study"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    title_y = height // 3
    
    # Draw title with shadow
    draw.text((title_x + 5, title_y + 5), title, font=title_font, fill=(0, 0, 0, 128))
    draw.text((title_x, title_y), title, font=title_font, fill="white")
    
    # Subtitle
    subtitle = "매일 영어 공부"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 150
    
    draw.text((subtitle_x + 3, subtitle_y + 3), subtitle, font=subtitle_font, fill=(0, 0, 0, 128))
    draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill="#FFD700")
    
    # Add tagline
    tagline_font = get_font(35)
    tagline = "Learn Essential English Sentences Every Day"
    bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_width = bbox[2] - bbox[0]
    tagline_x = (width - tagline_width) // 2
    tagline_y = height - height // 4
    
    draw.text((tagline_x, tagline_y), tagline, font=tagline_font, fill=(200, 200, 200))
    
    return img


def create_outro_image(width: int = 1920, height: int = 1080):
    """Create default outro image with cleaner design."""
    # Create gradient background (dark blue to purple)
    img = create_gradient_background(width, height, (20, 20, 60), (60, 20, 100))
    draw = ImageDraw.Draw(img)
    
    # Add decorative circles for visual interest
    for i in range(3):
        x = np.random.randint(200, width - 200)
        y = np.random.randint(200, height - 200)
        radius = np.random.randint(50, 150)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], 
                    fill=(255, 255, 255, 20))
    
    # Add thank you message
    title_font = get_font(90)
    title = "Thank You!"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    title_y = height // 5
    
    # Draw title with glow effect
    for i in range(5, 0, -1):
        alpha = int(80 / i)
        draw.text((title_x, title_y), title, font=title_font, 
                 fill=(255, 255, 255, alpha))
    draw.text((title_x, title_y), title, font=title_font, fill="white")
    
    # Korean thank you
    subtitle_font = get_font(50)
    subtitle = "시청해 주셔서 감사합니다!"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 130
    
    draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill="#FFD700")
    
    # Add message about buttons appearing
    msg_font = get_font(35)
    msg_text = "Please Subscribe & Like for more content!"
    bbox = draw.textbbox((0, 0), msg_text, font=msg_font)
    msg_width = bbox[2] - bbox[0]
    msg_x = (width - msg_width) // 2
    msg_y = height // 2
    
    draw.text((msg_x, msg_y), msg_text, font=msg_font, fill=(200, 200, 200))
    
    # Korean message
    msg_kr = "구독과 좋아요 부탁드립니다!"
    bbox = draw.textbbox((0, 0), msg_kr, font=msg_font)
    msg_kr_width = bbox[2] - bbox[0]
    msg_kr_x = (width - msg_kr_width) // 2
    msg_kr_y = msg_y + 50
    
    draw.text((msg_kr_x, msg_kr_y), msg_kr, font=msg_font, fill=(200, 200, 200))
    
    # Add Mecaspace branding at top right
    brand_font = get_font(40)
    brand_text = "메카스페이스"
    draw.text((width - 300, 50), brand_text, font=brand_font, fill=(255, 255, 255, 200))
    
    # Add handle below brand
    handle_font = get_font(25)
    handle_text = "@mecca-.-space"
    draw.text((width - 300, 100), handle_text, font=handle_font, fill=(255, 255, 255, 150))
    
    # Add subscribe & like icon text in bottom right
    icon_font = get_font(50)
    icon_text = "구독&좋아요 👍"
    draw.text((width - 350, height - 100), icon_text, font=icon_font, fill=(255, 215, 0))
    
    # Add next video schedule at bottom center
    next_font = get_font(30)
    next_text = "매일 새로운 영어 공부 영상"
    bbox = draw.textbbox((0, 0), next_text, font=next_font)
    next_width = bbox[2] - bbox[0]
    next_x = (width - next_width) // 2
    next_y = height - 80
    
    draw.text((next_x, next_y), next_text, font=next_font, fill=(200, 200, 200))
    
    return img


def main():
    """Create and save default assets."""
    assets_dir = os.path.join(os.path.dirname(__file__), '../../assets/default')
    os.makedirs(assets_dir, exist_ok=True)
    
    # Create intro image
    intro = create_intro_image()
    intro_path = os.path.join(assets_dir, 'intro.png')
    intro.save(intro_path, 'PNG')
    print(f"✅ Created intro image: {intro_path}")
    
    # Create outro image
    outro = create_outro_image()
    outro_path = os.path.join(assets_dir, 'outro.png')
    outro.save(outro_path, 'PNG')
    print(f"✅ Created outro image: {outro_path}")
    
    return intro_path, outro_path


if __name__ == "__main__":
    main()