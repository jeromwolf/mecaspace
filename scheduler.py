#!/usr/bin/env python3
import os
import schedule
import time
from datetime import datetime
import subprocess
import logging
from src.utils.data_loader import DataLoader


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)


class VideoScheduler:
    def __init__(self, data_directory: str = "data/daily_sentences"):
        self.data_directory = data_directory
        self.processed_directory = os.path.join(data_directory, "processed")
        os.makedirs(self.processed_directory, exist_ok=True)
        
    def get_next_data_file(self):
        """Get the next unprocessed data file."""
        # Look for CSV files in the data directory
        for filename in sorted(os.listdir(self.data_directory)):
            if filename.endswith('.csv') and not filename.startswith('.'):
                file_path = os.path.join(self.data_directory, filename)
                if os.path.isfile(file_path):
                    return file_path
        return None
    
    def create_daily_video(self):
        """Create today's video."""
        logging.info("Starting daily video creation...")
        
        # Get next data file
        data_file = self.get_next_data_file()
        if not data_file:
            logging.warning("No data files found to process")
            return
        
        logging.info(f"Processing file: {data_file}")
        
        # Generate output filename with date
        date_str = datetime.now().strftime("%Y%m%d")
        output_name = f"daily_english_{date_str}.mp4"
        
        # Run the main script
        try:
            cmd = [
                "python", "main.py",
                data_file,
                "-o", output_name,
                "-t", "nature",  # You can randomize theme
                "-m", "calm"     # You can randomize music
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logging.info(f"Video created successfully: {output_name}")
                
                # Move processed file
                processed_path = os.path.join(
                    self.processed_directory,
                    os.path.basename(data_file)
                )
                os.rename(data_file, processed_path)
                logging.info(f"Moved processed file to: {processed_path}")
                
                # Optional: Upload to YouTube here
                # self.upload_to_youtube(output_name)
                
            else:
                logging.error(f"Video creation failed: {result.stderr}")
                
        except Exception as e:
            logging.error(f"Error creating video: {str(e)}")
    
    def upload_to_youtube(self, video_path: str):
        """
        Upload video to YouTube (requires YouTube API setup).
        This is a placeholder - you'll need to implement YouTube upload.
        """
        logging.info(f"YouTube upload placeholder for: {video_path}")
        # TODO: Implement YouTube upload using google-api-python-client
        # You'll need OAuth2 credentials and YouTube Data API v3
    
    def run(self):
        """Start the scheduler."""
        logging.info("Video scheduler started")
        
        # Schedule daily video creation at 8:00 AM
        schedule.every().day.at("08:00").do(self.create_daily_video)
        
        # For testing: run every minute
        # schedule.every(1).minutes.do(self.create_daily_video)
        
        # Run immediately on start (optional)
        # self.create_daily_video()
        
        logging.info("Scheduler is running. Press Ctrl+C to stop.")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


def create_sample_schedule_data():
    """Create sample data files for the next 7 days."""
    data_dir = "data/daily_sentences"
    os.makedirs(data_dir, exist_ok=True)
    
    # Sample sentences for each day
    daily_sentences = [
        # Day 1
        [
            ("Good morning!", "좋은 아침!"),
            ("How did you sleep?", "잘 잤어요?"),
            ("I slept well, thank you.", "잘 잤어요, 감사합니다."),
            ("What's for breakfast?", "아침 식사는 뭐예요?"),
            ("Let's have coffee together.", "같이 커피 마셔요."),
        ],
        # Day 2
        [
            ("What time is it?", "지금 몇 시예요?"),
            ("It's time to go.", "갈 시간이에요."),
            ("I'm running late.", "늦고 있어요."),
            ("See you later!", "나중에 봐요!"),
            ("Have a safe trip.", "안전히 가세요."),
        ],
        # Day 3
        [
            ("How's the weather?", "날씨가 어때요?"),
            ("It's sunny today.", "오늘은 맑아요."),
            ("Don't forget your umbrella.", "우산 잊지 마세요."),
            ("It might rain later.", "나중에 비가 올 수도 있어요."),
            ("Stay warm!", "따뜻하게 입으세요!"),
        ],
    ]
    
    for i, sentences in enumerate(daily_sentences, 1):
        filename = f"day_{i:03d}_sentences.csv"
        filepath = os.path.join(data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("English,Korean\n")
            for en, ko in sentences:
                f.write(f'"{en}","{ko}"\n')
        
        print(f"Created: {filepath}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Video creation scheduler")
    parser.add_argument(
        "--create-sample-data",
        action="store_true",
        help="Create sample data files for testing"
    )
    parser.add_argument(
        "--run-once",
        action="store_true",
        help="Run video creation once and exit"
    )
    
    args = parser.parse_args()
    
    if args.create_sample_data:
        create_sample_schedule_data()
        print("Sample data created in data/daily_sentences/")
    elif args.run_once:
        scheduler = VideoScheduler()
        scheduler.create_daily_video()
    else:
        scheduler = VideoScheduler()
        scheduler.run()