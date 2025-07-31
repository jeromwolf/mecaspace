#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime
from src.core.config import config
from src.services.tts_service import TTSService
from src.services.image_service import ImageService
from src.services.music_service import MusicService
from src.services.video_service import VideoService
from src.utils.data_loader import DataLoader
from src.utils.youtube_metadata import YouTubeMetadata
from src.utils.thumbnail_generator import generate_thumbnail_from_video_path


def create_video(input_file: str, output_name: str = None, 
                 theme: str = "nature", music_style: str = "calm"):
    """
    Create a video from sentence data.
    
    Args:
        input_file: Path to CSV/JSON/Excel file with sentences
        output_name: Name for output video (auto-generated if None)
        theme: Theme for background images
        music_style: Style of background music
    """
    print(f"🎬 Starting video creation process...")
    
    # Load sentences
    print(f"📚 Loading sentences from: {input_file}")
    sentences = DataLoader.load_sentences(input_file)
    print(f"✅ Loaded {len(sentences)} sentence pairs")
    
    # Initialize services
    tts_service = TTSService()
    image_service = ImageService()
    music_service = MusicService()
    video_service = VideoService()
    youtube_metadata = YouTubeMetadata()
    
    # Create output filename if not provided
    if not output_name:
        date_str = datetime.now().strftime("%Y%m%d")
        output_name = f"english_study_{date_str}.mp4"
    
    output_path = os.path.join(config.video_output_dir, output_name)
    
    # Generate audio files
    print(f"🎙️ Generating audio files...")
    audio_files = tts_service.generate_sentence_audio(
        sentences, config.audio_output_dir
    )
    print(f"✅ Generated {len(audio_files) * 2} audio files")
    
    # Get background images
    print(f"🖼️ Collecting background images...")
    image_paths = image_service.get_images_for_sentences(sentences, theme)
    print(f"✅ Collected {len(image_paths)} images")
    
    # Get background music
    print(f"🎵 Preparing background music...")
    estimated_duration = len(sentences) * (config.sentence_display_time + 2)
    music_path = music_service.get_background_music(estimated_duration, music_style)
    print(f"✅ Background music ready")
    
    # Create video
    print(f"🎥 Creating video...")
    video_path = video_service.create_full_video(
        sentences, audio_files, image_paths, music_path, output_path
    )
    print(f"✅ Video created: {video_path}")
    
    # Generate YouTube metadata
    print(f"📝 Generating YouTube metadata...")
    metadata = youtube_metadata.generate_metadata(
        sentences, 
        music_style=music_style,
        image_theme=theme
    )
    
    # Save metadata
    metadata_path = output_path.replace('.mp4', '_metadata.txt')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write(f"Title:\n{metadata['title']}\n\n")
        f.write(f"Description:\n{metadata['description']}\n\n")
        f.write(f"Tags:\n{', '.join(metadata['tags'])}\n")
    
    print(f"✅ Metadata saved: {metadata_path}")
    
    # Generate thumbnail
    print(f"🖼️ Generating thumbnail...")
    thumbnail_path = generate_thumbnail_from_video_path(video_path, sentences)
    
    print(f"\n🎉 Video creation complete!")
    print(f"📹 Video: {video_path}")
    print(f"📄 Metadata: {metadata_path}")
    print(f"🖼️ Thumbnail: {thumbnail_path}")
    
    return video_path, metadata


def main():
    parser = argparse.ArgumentParser(
        description="Create English study videos for YouTube"
    )
    parser.add_argument(
        "input", 
        nargs="?",
        help="Input file (CSV/JSON/Excel) with English-Korean sentence pairs"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output video filename (auto-generated if not specified)"
    )
    parser.add_argument(
        "-t", "--theme",
        default="nature",
        choices=["nature", "study", "city", "abstract"],
        help="Theme for background images (default: nature)"
    )
    parser.add_argument(
        "-m", "--music",
        default="calm",
        choices=["calm", "upbeat", "inspiring"],
        help="Background music style (default: calm)"
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Create a sample CSV file"
    )
    
    args = parser.parse_args()
    
    # Create sample data if requested
    if args.sample:
        sample_path = "sample_sentences.csv"
        DataLoader.create_sample_data(sample_path)
        print(f"✅ Sample file created: {sample_path}")
        print("Run the program again with this file to create a video:")
        print(f"  python main.py {sample_path}")
        return
    
    # Check if input is provided when not creating sample
    if not args.input:
        print(f"❌ Error: Input file is required unless using --sample")
        parser.print_help()
        sys.exit(1)
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file not found: {args.input}")
        sys.exit(1)
    
    try:
        create_video(
            args.input,
            args.output,
            args.theme,
            args.music
        )
    except Exception as e:
        import traceback
        print(f"❌ Error: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()