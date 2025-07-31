# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mecaspace is a YouTube video generation tool for English-Korean language learning. It automatically creates daily study videos with TTS narration, background images, and music.

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Create sample data
python main.py --sample

# Generate video from CSV
python main.py input.csv -o output.mp4 -t nature -m calm

# Run scheduler for daily videos
python scheduler.py

# Create schedule test data
python scheduler.py --create-sample-data

# Weekly content generation
python weekly_content_generator.py --week 1  # Generate specific week
python weekly_content_generator.py --month   # Generate full month plan
cd data/week_1_20250731 && ./generate_week.sh  # Run batch generation
```

## Architecture

The project follows a service-oriented architecture:

- **Core Layer** (`src/core/`): Configuration management using environment variables
- **Service Layer** (`src/services/`): 
  - `tts_service.py`: Dual TTS engine support (Azure Speech, Google TTS)
  - `image_service.py`: Unsplash API integration with fallback placeholders
  - `music_service.py`: Background music management with duration adjustment
  - `video_service.py`: MoviePy-based video composition with transitions
- **Utils Layer** (`src/utils/`):
  - `data_loader.py`: Multi-format input support (CSV, JSON, Excel)
  - `youtube_metadata.py`: Metadata generation for YouTube uploads
- **Main Components**:
  - `main.py`: CLI interface and orchestration
  - `scheduler.py`: Automated daily video generation
  - `weekly_content_generator.py`: Weekly content automation with themed days

## Key Patterns

1. **Service Abstraction**: Each service has clear interfaces (e.g., TTSEngine abstract base)
2. **Fallback Mechanisms**: API failures gracefully degrade (placeholder images, Google TTS fallback)
3. **Configuration-Driven**: All settings via environment variables
4. **Modular Design**: Services can be tested and modified independently
5. **Content Automation**: Weekly themed content (Mon: Cafe, Tue: Shopping, Wed: Business, Thu: Travel, Fri: Daily)

## Recent Updates (v2.1.0)

- Dynamic intro/outro with time-based gradients and animations
- Weekly content automation system with daily themes
- Batch video generation scripts for efficient production
- 4-week content rotation with diverse topics

## Current Status (2025-07-31)

### User Context
- User: 켈리 (Kelly)
- YouTube subscribers: 7명 (목표: 1000명)
- Current focus: 채널 성장을 위한 영상 품질 개선

### Completed Tasks
1. **Dynamic Intro/Outro** ✅
   - Time-based color gradients (morning/afternoon/evening/night)
   - Typing animations and floating elements
   - Interactive buttons (subscribe, like, notification)

2. **Weekly Content Automation** ✅
   - Monday: ☕ 카페영어 (Starbucks ordering)
   - Tuesday: 🛍️ 쇼핑영어 (Size asking, price negotiation)
   - Wednesday: 💼 비즈니스영어 (Email, meetings)
   - Thursday: ✈️ 여행영어 (Airport, hotel)
   - Friday: 🌟 일상영어 (Weather, greetings)
   - Generated 4 weeks of content in `data/week_*` folders

3. **Video Upgrade Strategy** ✅
   - 7-day implementation plan created
   - Day 1: Particle effects & neon glow
   - Day 2: Sound design (ASMR, transitions)
   - Day 3: Thumbnail automation
   - Day 4: 3D text animations
   - Day 5: Interactive elements
   - Day 6: Branding enhancement
   - Day 7: Learning experience improvements
   - Documentation: VIDEO_UPGRADE_STRATEGY.md

### Known Issues
- Video rendering is slow (5+ minutes per video)
- Background video generation processes may still be running (PID: 52946)
- Theme names in batch scripts fixed (cafe→city, shopping→city, etc.)

### Next Steps
- Start implementing Day 1 upgrade (Particle effects & neon glow)
- Monitor weekly content generation progress
- Track subscriber growth and engagement metrics