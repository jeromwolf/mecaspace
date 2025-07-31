#!/bin/bash
# Weekly Content Generation Script
# Generated: 2025-07-31 22:40:33

echo "🎬 Starting weekly content generation..."


# MONDAY - ☕ 카페에서 쓰는 영어 - 카페에서 자리 찾기
echo "📹 Creating monday content..."
python main.py "2025.08.11_monday.csv" -o "2025.08.11_카페영어.mp4" -t cafe -m upbeat
echo "✅ Completed monday content"
echo ""

# TUESDAY - 🛍️ 쇼핑할 때 쓰는 영어 - 가격 흥정하기
echo "📹 Creating tuesday content..."
python main.py "2025.08.12_tuesday.csv" -o "2025.08.12_쇼핑영어.mp4" -t shopping -m calm
echo "✅ Completed tuesday content"
echo ""

# WEDNESDAY - 💼 직장에서 쓰는 영어 - 회의 영어
echo "📹 Creating wednesday content..."
python main.py "2025.08.13_wednesday.csv" -o "2025.08.13_비즈니스영어.mp4" -t business -m calm
echo "✅ Completed wednesday content"
echo ""

# THURSDAY - ✈️ 여행할 때 쓰는 영어 - 호텔에서
echo "📹 Creating thursday content..."
python main.py "2025.08.14_thursday.csv" -o "2025.08.14_여행영어.mp4" -t travel -m inspiring
echo "✅ Completed thursday content"
echo ""

# FRIDAY - 🌟 일상에서 쓰는 영어 - 인사와 안부
echo "📹 Creating friday content..."
python main.py "2025.08.15_friday.csv" -o "2025.08.15_일상영어.mp4" -t daily -m upbeat
echo "✅ Completed friday content"
echo ""

echo "🎉 Weekly content generation complete!"
echo "📁 Videos are saved in: output/videos/"
