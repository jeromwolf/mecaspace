import os
import requests
from typing import List, Optional
from src.core.config import config
import json
import time
import random
from PIL import Image, ImageDraw, ImageFilter


class ImageService:
    def __init__(self):
        self.unsplash_base_url = "https://api.unsplash.com"
        self.access_key = config.unsplash_access_key
        
    def search_images(self, query: str, count: int = 10) -> List[dict]:
        """
        Search for images on Unsplash based on query.
        
        Args:
            query: Search query (e.g., "nature landscape", "study education")
            count: Number of images to fetch
            
        Returns:
            List of image metadata dictionaries
        """
        if not self.access_key:
            print("Warning: Unsplash API key not configured. Using placeholder images.")
            return self._get_placeholder_images(count)
        
        headers = {"Authorization": f"Client-ID {self.access_key}"}
        
        # Add randomization by using page parameter
        # Random page between 1 and 10 to get different results
        random_page = random.randint(1, 10)
        
        params = {
            "query": query,
            "per_page": count,
            "page": random_page,  # Add page parameter for variety
            "orientation": "landscape"
        }
        
        try:
            response = requests.get(
                f"{self.unsplash_base_url}/search/photos",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            results = data.get("results", [])
            # Shuffle results for more randomness
            random.shuffle(results)
            
            for photo in results:
                images.append({
                    "id": photo["id"],
                    "url": photo["urls"]["regular"],
                    "download_url": photo["links"]["download"],
                    "author": photo["user"]["name"],
                    "description": photo.get("description", "")
                })
            
            return images
            
        except Exception as e:
            print(f"Error fetching images from Unsplash: {e}")
            return self._get_placeholder_images(count)
    
    def download_image(self, image_url: str, save_path: str) -> str:
        """Download image from URL and save to local path."""
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return save_path
            
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None
    
    def get_images_for_sentences(self, sentences: List[tuple], 
                                theme: str = "nature landscape") -> List[str]:
        """
        Get images for each sentence pair.
        
        Args:
            sentences: List of (english, korean) sentence tuples
            theme: Theme for image search
            
        Returns:
            List of local image paths
        """
        image_paths = []
        
        # Clean up old images (older than 7 days)
        self._cleanup_old_images(days=7)
        
        # Add timestamp to filename to avoid reusing old images
        timestamp = int(time.time())
        
        # Add variety to search queries based on theme
        theme_variations = {
            "nature": ["nature landscape", "forest scenery", "mountain view", "ocean view", 
                      "sunset nature", "sunrise landscape", "peaceful nature", "green nature",
                      "blue sky nature", "natural beauty"],
            "study": ["study room", "library", "books education", "learning space",
                     "desk study", "classroom", "education background", "academic setting",
                     "student life", "knowledge learning"],
            "city": ["city skyline", "urban landscape", "city lights", "modern city",
                    "downtown view", "metropolitan", "city architecture", "urban life",
                    "cityscape night", "city buildings"],
            "abstract": ["abstract art", "geometric patterns", "colorful abstract", "minimal design",
                        "creative background", "artistic pattern", "modern abstract", "digital art",
                        "abstract shapes", "creative design"]
        }
        
        # Get variations for the theme
        queries = theme_variations.get(theme, [f"{theme} landscape"] * 10)
        
        # Use different query for each image
        for i in range(len(sentences)):
            query = queries[i % len(queries)]
            # Get multiple images and pick a random one
            images = self.search_images(query, 10)
            
            filename = f"background_{timestamp}_{i}.jpg"
            save_path = os.path.join(config.image_output_dir, filename)
            
            if images and len(images) > 0:
                # Pick a random image from the results
                image_data = random.choice(images)
                # Download image
                if image_data.get("url"):
                    downloaded_path = self.download_image(image_data["url"], save_path)
                    if downloaded_path:
                        image_paths.append(downloaded_path)
                    else:
                        # Use placeholder if download fails
                        image_paths.append(self._create_placeholder_image(save_path))
                else:
                    image_paths.append(self._create_placeholder_image(save_path))
            else:
                # No images found, use placeholder
                image_paths.append(self._create_placeholder_image(save_path))
            
            # Rate limiting
            time.sleep(0.5)
        
        return image_paths
    
    def _get_placeholder_images(self, count: int) -> List[dict]:
        """Generate placeholder image data when API is not available."""
        images = []
        for i in range(count):
            images.append({
                "id": f"placeholder_{i}",
                "url": None,
                "download_url": None,
                "author": "Placeholder",
                "description": "Placeholder image"
            })
        return images
    
    def _cleanup_old_images(self, days: int = 7):
        """Remove images older than specified days."""
        try:
            current_time = time.time()
            cutoff_time = current_time - (days * 24 * 60 * 60)
            
            for filename in os.listdir(config.image_output_dir):
                if filename.startswith("background_") and filename.endswith(".jpg"):
                    file_path = os.path.join(config.image_output_dir, filename)
                    if os.path.getmtime(file_path) < cutoff_time:
                        os.remove(file_path)
        except Exception as e:
            # Don't fail if cleanup fails
            pass
    
    def _create_placeholder_image(self, save_path: str) -> str:
        """Create a more sophisticated placeholder image using Pillow."""
        from PIL import Image, ImageDraw, ImageFilter
        import random
        
        width, height = config.video_width, config.video_height
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Create a more interesting gradient with multiple colors
        gradient_styles = [
            # Sunset style
            [(255, 94, 77), (255, 154, 0), (237, 117, 57), (95, 39, 205)],
            # Ocean style
            [(69, 104, 220), (89, 173, 246), (146, 232, 192), (255, 255, 255)],
            # Forest style
            [(34, 139, 34), (60, 179, 113), (152, 251, 152), (255, 250, 205)],
            # Purple dream
            [(138, 43, 226), (218, 112, 214), (255, 182, 193), (255, 228, 225)]
        ]
        
        colors = random.choice(gradient_styles)
        
        # Create smooth gradient
        for y in range(height):
            # Calculate which color segment we're in
            segment = y / height * (len(colors) - 1)
            idx = int(segment)
            
            if idx < len(colors) - 1:
                # Interpolate between colors
                t = segment - idx
                r = int(colors[idx][0] * (1 - t) + colors[idx + 1][0] * t)
                g = int(colors[idx][1] * (1 - t) + colors[idx + 1][1] * t)
                b = int(colors[idx][2] * (1 - t) + colors[idx + 1][2] * t)
            else:
                r, g, b = colors[-1]
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add some geometric shapes for visual interest
        for _ in range(random.randint(3, 7)):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(100, 400)
            opacity = random.randint(20, 60)
            
            # Create a semi-transparent overlay
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            shape_color = (255, 255, 255, opacity)
            if random.choice([True, False]):
                # Draw circle
                overlay_draw.ellipse([x - size, y - size, x + size, y + size], 
                                   fill=shape_color)
            else:
                # Draw rectangle
                overlay_draw.rectangle([x - size//2, y - size//2, x + size//2, y + size//2],
                                     fill=shape_color)
            
            # Apply blur to the overlay
            overlay = overlay.filter(ImageFilter.GaussianBlur(radius=50))
            
            # Composite onto main image
            img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        img.save(save_path)
        return save_path