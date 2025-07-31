import os
import requests
from typing import List, Optional
from src.core.config import config
import json
import time


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
        params = {
            "query": query,
            "per_page": count,
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
            
            for photo in data.get("results", []):
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
        images = self.search_images(theme, len(sentences))
        
        for i, image_data in enumerate(images):
            if i >= len(sentences):
                break
                
            filename = f"background_{i}.jpg"
            save_path = os.path.join(config.image_output_dir, filename)
            
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
    
    def _create_placeholder_image(self, save_path: str) -> str:
        """Create a placeholder image using Pillow."""
        from PIL import Image, ImageDraw, ImageFont
        
        # Create gradient background
        width, height = config.video_width, config.video_height
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Create gradient effect
        for y in range(height):
            r = int(100 + (y / height) * 50)
            g = int(150 + (y / height) * 50)
            b = int(200 - (y / height) * 50)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        img.save(save_path)
        return save_path