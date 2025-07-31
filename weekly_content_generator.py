#!/usr/bin/env python3
"""
주간 콘텐츠 자동 생성 스크립트
요일별로 정해진 주제의 영어 학습 비디오를 자동 생성합니다.
"""

import os
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

class WeeklyContentGenerator:
    def __init__(self):
        self.content_templates = {
            'monday': {
                'series': '카페영어',
                'theme': 'city',
                'music': 'upbeat',
                'title_prefix': '☕ 카페에서 쓰는 영어',
                'topics': [
                    {
                        'title': '스타벅스 주문 마스터하기',
                        'sentences': [
                            ("Can I get a grande iced americano?", "그란데 사이즈 아이스 아메리카노 주세요"),
                            ("I'll have it to go, please", "테이크아웃으로 할게요"),
                            ("Can I get extra shot?", "샷 추가해 주세요"),
                            ("Do you have any dairy-free options?", "유제품 없는 옵션 있나요?"),
                            ("Can I use my tumbler?", "제 텀블러 사용해도 될까요?")
                        ]
                    },
                    {
                        'title': '카페에서 자리 찾기',
                        'sentences': [
                            ("Is this seat taken?", "이 자리 있나요?"),
                            ("Do you have WiFi here?", "와이파이 있나요?"),
                            ("What's the WiFi password?", "와이파이 비밀번호가 뭐예요?"),
                            ("Where is the power outlet?", "콘센트가 어디 있나요?"),
                            ("Can I sit here for a while?", "여기 잠깐 앉아있어도 될까요?")
                        ]
                    }
                ]
            },
            'tuesday': {
                'series': '쇼핑영어',
                'theme': 'city',
                'music': 'calm',
                'title_prefix': '🛍️ 쇼핑할 때 쓰는 영어',
                'topics': [
                    {
                        'title': '옷 사이즈 묻기',
                        'sentences': [
                            ("Do you have this in medium?", "이거 미디엄 사이즈 있나요?"),
                            ("Can I try this on?", "이거 입어봐도 될까요?"),
                            ("Where is the fitting room?", "피팅룸이 어디인가요?"),
                            ("This is too tight", "이거 너무 꽉 끼네요"),
                            ("Do you have a bigger size?", "더 큰 사이즈 있나요?")
                        ]
                    },
                    {
                        'title': '가격 흥정하기',
                        'sentences': [
                            ("How much is this?", "이거 얼마예요?"),
                            ("Can you give me a discount?", "할인해 주실 수 있나요?"),
                            ("Is this on sale?", "이거 세일 상품인가요?"),
                            ("I'll take it", "이걸로 할게요"),
                            ("Can I pay by card?", "카드로 결제 가능한가요?")
                        ]
                    }
                ]
            },
            'wednesday': {
                'series': '비즈니스영어',
                'theme': 'study',
                'music': 'calm',
                'title_prefix': '💼 직장에서 쓰는 영어',
                'topics': [
                    {
                        'title': '이메일 시작하기',
                        'sentences': [
                            ("I hope this email finds you well", "안녕하세요"),
                            ("I'm writing to inquire about...", "...에 대해 문의드립니다"),
                            ("Thank you for your quick response", "빠른 답변 감사합니다"),
                            ("Please find attached...", "첨부 파일을 확인해 주세요"),
                            ("I look forward to hearing from you", "답변 기다리겠습니다")
                        ]
                    },
                    {
                        'title': '회의 영어',
                        'sentences': [
                            ("Let's get started", "시작하겠습니다"),
                            ("Could you elaborate on that?", "좀 더 자세히 설명해 주실 수 있나요?"),
                            ("I'd like to add something", "제가 덧붙이고 싶은 게 있습니다"),
                            ("Let me share my screen", "화면 공유하겠습니다"),
                            ("Any questions so far?", "여기까지 질문 있으신가요?")
                        ]
                    }
                ]
            },
            'thursday': {
                'series': '여행영어',
                'theme': 'nature',
                'music': 'inspiring',
                'title_prefix': '✈️ 여행할 때 쓰는 영어',
                'topics': [
                    {
                        'title': '공항에서',
                        'sentences': [
                            ("Where is the check-in counter?", "체크인 카운터가 어디인가요?"),
                            ("I'd like an aisle seat, please", "통로쪽 좌석으로 주세요"),
                            ("How much is the excess baggage fee?", "초과 수하물 요금이 얼마인가요?"),
                            ("Which gate is it?", "몇 번 게이트인가요?"),
                            ("Is the flight on time?", "비행기 제시간에 출발하나요?")
                        ]
                    },
                    {
                        'title': '호텔에서',
                        'sentences': [
                            ("I have a reservation under Kim", "김으로 예약했습니다"),
                            ("What time is check-out?", "체크아웃 시간이 언제인가요?"),
                            ("Could I have a wake-up call?", "모닝콜 부탁드려요"),
                            ("Is breakfast included?", "조식이 포함되어 있나요?"),
                            ("Can I extend my stay?", "하루 더 묵을 수 있나요?")
                        ]
                    }
                ]
            },
            'friday': {
                'series': '일상영어',
                'theme': 'abstract',
                'music': 'upbeat',
                'title_prefix': '🌟 일상에서 쓰는 영어',
                'topics': [
                    {
                        'title': '날씨 이야기',
                        'sentences': [
                            ("It's such a nice day today", "오늘 날씨 정말 좋네요"),
                            ("It looks like it's going to rain", "비가 올 것 같아요"),
                            ("It's freezing outside", "밖이 너무 추워요"),
                            ("The weather is perfect", "날씨가 완벽해요"),
                            ("I hope it clears up soon", "날씨가 곧 개었으면 좋겠어요")
                        ]
                    },
                    {
                        'title': '인사와 안부',
                        'sentences': [
                            ("How have you been?", "어떻게 지내셨어요?"),
                            ("Long time no see!", "오랜만이에요!"),
                            ("I've been busy lately", "요즘 바빴어요"),
                            ("Take care of yourself", "건강 조심하세요"),
                            ("Have a great weekend!", "좋은 주말 보내세요!")
                        ]
                    }
                ]
            }
        }

    def get_week_content(self, week_number=1):
        """특정 주차의 콘텐츠를 생성합니다."""
        week_content = []
        
        for day, day_name in enumerate(['monday', 'tuesday', 'wednesday', 'thursday', 'friday']):
            day_config = self.content_templates[day_name]
            # 주차에 따라 다른 토픽 선택
            topic_index = (week_number - 1) % len(day_config['topics'])
            topic = day_config['topics'][topic_index]
            
            content = {
                'day': day + 1,
                'day_name': day_name,
                'series': day_config['series'],
                'theme': day_config['theme'],
                'music': day_config['music'],
                'title': f"{day_config['title_prefix']} - {topic['title']}",
                'sentences': topic['sentences']
            }
            week_content.append(content)
        
        return week_content

    def create_weekly_csv(self, week_number=1, start_date=None):
        """주간 콘텐츠 CSV 파일들을 생성합니다."""
        if start_date is None:
            start_date = datetime.now()
        
        # 주간 폴더 생성
        week_folder = f"data/week_{week_number}_{start_date.strftime('%Y%m%d')}"
        os.makedirs(week_folder, exist_ok=True)
        
        week_content = self.get_week_content(week_number)
        
        for i, content in enumerate(week_content):
            date = start_date + timedelta(days=i)
            filename = f"{date.strftime('%Y.%m.%d')}_{content['day_name']}.csv"
            filepath = os.path.join(week_folder, filename)
            
            # CSV 데이터 생성
            data = []
            for en, ko in content['sentences']:
                data.append({
                    'English': en,
                    'Korean': ko
                })
            
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8')
            
            # 메타데이터 저장
            metadata = {
                'date': date.strftime('%Y-%m-%d'),
                'day': content['day_name'],
                'series': content['series'],
                'theme': content['theme'],
                'music': content['music'],
                'title': content['title'],
                'output_filename': f"{date.strftime('%Y.%m.%d')}_{content['series']}.mp4"
            }
            
            metadata_file = filepath.replace('.csv', '_metadata.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Created: {filename}")
        
        # 주간 실행 스크립트 생성
        self._create_batch_script(week_folder, week_content, start_date)
        
        return week_folder

    def _create_batch_script(self, week_folder, week_content, start_date):
        """주간 비디오를 한 번에 생성하는 배치 스크립트를 만듭니다."""
        script_content = """#!/bin/bash
# Weekly Content Generation Script
# Generated: {timestamp}

echo "🎬 Starting weekly content generation..."

""".format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        for i, content in enumerate(week_content):
            date = start_date + timedelta(days=i)
            csv_file = f"{date.strftime('%Y.%m.%d')}_{content['day_name']}.csv"
            output_file = f"{date.strftime('%Y.%m.%d')}_{content['series']}.mp4"
            
            script_content += f"""
# {content['day_name'].upper()} - {content['title']}
echo "📹 Creating {content['day_name']} content..."
python main.py "{csv_file}" -o "{output_file}" -t {content['theme']} -m {content['music']}
echo "✅ Completed {content['day_name']} content"
echo ""
"""

        script_content += """
echo "🎉 Weekly content generation complete!"
echo "📁 Videos are saved in: output/videos/"
"""

        script_path = os.path.join(week_folder, "generate_week.sh")
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # 실행 권한 부여
        os.chmod(script_path, 0o755)
        print(f"\n✅ Batch script created: {script_path}")

    def create_month_plan(self):
        """한 달치 콘텐츠 계획을 생성합니다."""
        print("📅 Creating monthly content plan...\n")
        
        for week in range(1, 5):
            start_date = datetime.now() + timedelta(weeks=week-1)
            # 월요일로 조정
            days_ahead = 0 - start_date.weekday()  # 0 is Monday
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            start_date = start_date + timedelta(days_ahead)
            
            print(f"📍 Week {week} (Starting {start_date.strftime('%Y-%m-%d')})")
            folder = self.create_weekly_csv(week, start_date)
            print(f"   Folder: {folder}\n")

    def generate_special_content(self, occasion, sentences):
        """특별한 날을 위한 콘텐츠를 생성합니다."""
        special_themes = {
            'christmas': {'theme': 'holiday', 'music': 'upbeat', 'emoji': '🎄'},
            'newyear': {'theme': 'celebration', 'music': 'inspiring', 'emoji': '🎊'},
            'valentine': {'theme': 'love', 'music': 'calm', 'emoji': '❤️'},
            'halloween': {'theme': 'spooky', 'music': 'upbeat', 'emoji': '🎃'}
        }
        
        config = special_themes.get(occasion, {'theme': 'special', 'music': 'calm', 'emoji': '🌟'})
        
        # CSV 생성
        data = []
        for en, ko in sentences:
            data.append({'English': en, 'Korean': ko})
        
        df = pd.DataFrame(data)
        filename = f"data/special_{occasion}_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"{config['emoji']} Special content created: {filename}")
        return filename, config


# CLI 인터페이스
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Weekly Content Generator")
    parser.add_argument('--week', type=int, help='Generate specific week content')
    parser.add_argument('--month', action='store_true', help='Generate full month plan')
    parser.add_argument('--preview', action='store_true', help='Preview content without creating files')
    
    args = parser.parse_args()
    
    generator = WeeklyContentGenerator()
    
    if args.preview:
        # 콘텐츠 미리보기
        print("📋 Content Preview:\n")
        for week in range(1, 3):
            print(f"=== WEEK {week} ===")
            content = generator.get_week_content(week)
            for day_content in content:
                print(f"\n{day_content['day_name'].upper()}: {day_content['title']}")
                print(f"Series: {day_content['series']} | Theme: {day_content['theme']}")
                print("Sentences:")
                for i, (en, ko) in enumerate(day_content['sentences'], 1):
                    print(f"  {i}. {en}")
                    print(f"     → {ko}")
    
    elif args.month:
        generator.create_month_plan()
    
    elif args.week:
        folder = generator.create_weekly_csv(args.week)
        print(f"\n✅ Week {args.week} content ready in: {folder}")
        print(f"💡 Run the batch script to generate all videos: cd {folder} && ./generate_week.sh")
    
    else:
        # 기본: 이번 주 콘텐츠 생성
        folder = generator.create_weekly_csv(1)
        print(f"\n✅ This week's content ready in: {folder}")
        print(f"💡 Run the batch script to generate all videos: cd {folder} && ./generate_week.sh")