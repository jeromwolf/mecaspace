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