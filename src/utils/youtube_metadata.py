from datetime import datetime
from typing import List, Dict, Tuple
import random


class YouTubeMetadata:
    def __init__(self):
        self.title_templates = [
            "Daily English Study #{day} - Learn {count} Essential Phrases",
            "영어 공부 Day {day} - {count} Essential English Sentences",
            "Learn English & Korean Together - Day {day} ({date})",
            "Daily English Practice #{day} | {count} Useful Sentences",
            "{date} English Study - Master {count} Daily Phrases"
        ]
        
        self.description_template = """🌟 Daily English Study - Day {day} 🌟

📚 Today's Lesson:
Learn {count} essential English sentences with Korean translations. Perfect for daily practice!

🎯 What You'll Learn:
{sentence_list}

⏰ Study Schedule:
- Each sentence is displayed for easy learning
- English pronunciation followed by Korean translation
- Perfect for beginners and intermediate learners

📱 Study Tips:
1. Listen carefully to the pronunciation
2. Repeat after each sentence
3. Try to use these phrases in daily conversation
4. Review previous lessons regularly

🔔 Subscribe for Daily English Lessons!
New videos uploaded every day at {upload_time}

📋 Full Sentence List:
{full_list}

#EnglishStudy #영어공부 #DailyEnglish #LearnEnglish #한국어 #English #Korean #LanguageLearning #영어회화 #EnglishPractice #StudyWithMe #LanguageExchange #영어문장 #DailyPractice #EnglishSpeaking

🎵 Background Music: {music_credit}
📸 Images: {image_credit}
"""
        
        self.tags = [
            # English tags
            "learn english", "english study", "english practice", "daily english",
            "english sentences", "english phrases", "english speaking", "english lesson",
            "english for beginners", "english pronunciation", "improve english",
            "english vocabulary", "english grammar", "esl", "english as second language",
            
            # Korean tags
            "영어공부", "영어회화", "영어문장", "매일영어", "영어학습",
            "기초영어", "영어발음", "영어강의", "영어독학", "생활영어",
            
            # Mixed tags
            "korean english", "한국인을 위한 영어", "study english korean",
            "bilingual study", "language learning", "polyglot"
        ]
        
        self.categories = {
            "Education": 27,
            "People & Blogs": 22,
            "Howto & Style": 26
        }
    
    def generate_metadata(self, sentences: List[Tuple[str, str]], 
                         day_number: int = None,
                         music_style: str = "calm",
                         image_theme: str = "nature") -> Dict[str, any]:
        """
        Generate YouTube metadata for the video.
        
        Args:
            sentences: List of (english, korean) sentence pairs
            day_number: Day number for series (auto-generated if None)
            music_style: Style of background music used
            image_theme: Theme of images used
            
        Returns:
            Dictionary with title, description, tags, etc.
        """
        if day_number is None:
            day_number = (datetime.now() - datetime(2024, 1, 1)).days
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        upload_time = "8:00 AM KST"
        
        # Generate title
        title = random.choice(self.title_templates).format(
            day=day_number,
            count=len(sentences),
            date=date_str
        )
        
        # Create sentence preview (first 3 sentences)
        sentence_preview = []
        for i, (en, ko) in enumerate(sentences[:3]):
            sentence_preview.append(f"{i+1}. {en}")
        sentence_list = "\n".join(sentence_preview)
        if len(sentences) > 3:
            sentence_list += f"\n... and {len(sentences) - 3} more!"
        
        # Create full sentence list
        full_list_items = []
        for i, (en, ko) in enumerate(sentences):
            full_list_items.append(f"{i+1}. {en}\n   → {ko}")
        full_list = "\n".join(full_list_items)
        
        # Music and image credits
        music_credits = {
            "calm": "Relaxing Background Music (Royalty Free)",
            "upbeat": "Upbeat Study Music (Royalty Free)",
            "inspiring": "Motivational Background Music (Royalty Free)"
        }
        
        image_credits = {
            "nature": "Beautiful Nature Photography from Unsplash",
            "study": "Study & Education Images from Unsplash",
            "city": "Urban Photography from Unsplash"
        }
        
        # Generate description
        description = self.description_template.format(
            day=day_number,
            count=len(sentences),
            sentence_list=sentence_list,
            upload_time=upload_time,
            full_list=full_list,
            music_credit=music_credits.get(music_style, "Background Music"),
            image_credit=image_credits.get(image_theme, "Stock Images")
        )
        
        # Select tags (use most relevant ones)
        selected_tags = random.sample(self.tags, min(len(self.tags), 15))
        
        # Create metadata dictionary
        metadata = {
            "title": title,
            "description": description,
            "tags": selected_tags,
            "category_id": self.categories["Education"],
            "privacy_status": "public",
            "thumbnail_time": "00:00:05",  # 5 seconds into video
            "playlist": "Daily English Study Series",
            "language": "en",
            "license": "youtube",
            "embeddable": True,
            "public_stats_viewable": True,
            "publish_at": None,  # Set to schedule for specific time
            "recording_date": date_str,
            "location": {
                "latitude": 37.5665,
                "longitude": 126.9780,
                "location_description": "Seoul, South Korea"
            }
        }
        
        return metadata
    
    def generate_thumbnail_text(self, day_number: int, sentence_count: int) -> Dict[str, str]:
        """Generate text overlay for video thumbnail."""
        return {
            "main_text": f"Day {day_number}",
            "subtitle": f"{sentence_count} English Sentences",
            "badge_text": "DAILY STUDY",
            "corner_text": "EN/KO"
        }