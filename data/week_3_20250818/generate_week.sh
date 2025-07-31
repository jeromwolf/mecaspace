#!/bin/bash
# Weekly Content Generation Script
# Generated: 2025-07-31 22:40:33

echo "🎬 Starting weekly content generation..."


# MONDAY - ☕ 카페에서 쓰는 영어 - 스타벅스 주문 마스터하기
echo "📹 Creating monday content..."
python main.py "2025.08.18_monday.csv" -o "2025.08.18_카페영어.mp4" -t cafe -m upbeat
echo "✅ Completed monday content"
echo ""

# TUESDAY - 🛍️ 쇼핑할 때 쓰는 영어 - 옷 사이즈 묻기
echo "📹 Creating tuesday content..."
python main.py "2025.08.19_tuesday.csv" -o "2025.08.19_쇼핑영어.mp4" -t shopping -m calm
echo "✅ Completed tuesday content"
echo ""

# WEDNESDAY - 💼 직장에서 쓰는 영어 - 이메일 시작하기
echo "📹 Creating wednesday content..."
python main.py "2025.08.20_wednesday.csv" -o "2025.08.20_비즈니스영어.mp4" -t business -m calm
echo "✅ Completed wednesday content"
echo ""

# THURSDAY - ✈️ 여행할 때 쓰는 영어 - 공항에서
echo "📹 Creating thursday content..."
python main.py "2025.08.21_thursday.csv" -o "2025.08.21_여행영어.mp4" -t travel -m inspiring
echo "✅ Completed thursday content"
echo ""

# FRIDAY - 🌟 일상에서 쓰는 영어 - 날씨 이야기
echo "📹 Creating friday content..."
python main.py "2025.08.22_friday.csv" -o "2025.08.22_일상영어.mp4" -t daily -m upbeat
echo "✅ Completed friday content"
echo ""

echo "🎉 Weekly content generation complete!"
echo "📁 Videos are saved in: output/videos/"
