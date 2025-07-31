from datetime import datetime
from typing import List, Dict, Tuple
import random


class YouTubeMetadata:
    def __init__(self):
        self.title_templates = [
            "매일 영어 공부 #{day} - 필수 표현 {count}개 배우기",
            "영어 공부 Day {day} - {count}개의 필수 영어 문장",
            "영어와 한국어 함께 배우기 - Day {day} ({date})",
            "매일 영어 연습 #{day} | 유용한 문장 {count}개",
            "{date} 영어 공부 - 일상 표현 {count}개 마스터하기"
        ]
        
        self.description_template = """🌟 매일 영어 공부 - Day {day} 🌟

📚 오늘의 수업:
한국어 번역과 함께 필수 영어 문장 {count}개를 배워보세요. 매일 연습하기에 완벽합니다!

🎯 학습 내용:
{sentence_list}

⏰ 학습 일정:
- 각 문장은 쉽게 학습할 수 있도록 표시됩니다
- 영어 발음 후 한국어 번역이 이어집니다
- 초급자와 중급자에게 완벽합니다

📱 학습 팁:
1. 발음을 주의 깊게 들어보세요
2. 각 문장을 따라 말해보세요
3. 일상 대화에서 이 표현들을 사용해보세요
4. 이전 수업을 정기적으로 복습하세요

🔔 매일 영어 수업을 구독하세요!
매일 {upload_time}에 새로운 동영상이 업로드됩니다

📋 전체 문장 목록:
{full_list}

#영어공부 #매일영어 #영어회화 #영어문장 #기초영어 #EnglishStudy #DailyEnglish #LearnEnglish #한국어 #English #Korean #LanguageLearning #EnglishPractice #StudyWithMe #LanguageExchange #DailyPractice #EnglishSpeaking

🎵 배경 음악: {music_credit}
📸 이미지: {image_credit}
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
        upload_time = "오전 8:00 (한국시간)"
        
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
            "calm": "편안한 배경 음악 (저작권 프리)",
            "upbeat": "경쾌한 학습 음악 (저작권 프리)",
            "inspiring": "동기부여 배경 음악 (저작권 프리)"
        }
        
        image_credits = {
            "nature": "Unsplash의 아름다운 자연 사진",
            "study": "Unsplash의 학습 및 교육 이미지",
            "city": "Unsplash의 도시 사진",
            "abstract": "Unsplash의 추상 이미지"
        }
        
        # Generate description
        description = self.description_template.format(
            day=day_number,
            count=len(sentences),
            sentence_list=sentence_list,
            upload_time=upload_time,
            full_list=full_list,
            music_credit=music_credits.get(music_style, "배경 음악"),
            image_credit=image_credits.get(image_theme, "스톡 이미지")
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
            "playlist": "매일 영어 공부 시리즈",
            "language": "en",
            "license": "youtube",
            "embeddable": True,
            "public_stats_viewable": True,
            "publish_at": None,  # Set to schedule for specific time
            "recording_date": date_str,
            "location": {
                "latitude": 37.5665,
                "longitude": 126.9780,
                "location_description": "서울, 대한민국"
            }
        }
        
        return metadata
    
    def generate_thumbnail_text(self, day_number: int, sentence_count: int) -> Dict[str, str]:
        """Generate text overlay for video thumbnail."""
        return {
            "main_text": f"Day {day_number}",
            "subtitle": f"영어 문장 {sentence_count}개",
            "badge_text": "매일 학습",
            "corner_text": "영어/한글"
        }