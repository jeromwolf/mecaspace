import csv
import json
import pandas as pd
from typing import List, Tuple, Dict
import os


class DataLoader:
    @staticmethod
    def load_from_csv(file_path: str) -> List[Tuple[str, str]]:
        """
        Load sentence pairs from CSV file.
        Expected format: english,korean
        """
        sentences = []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Skip header if present
            first_row = next(reader, None)
            if first_row and first_row[0].lower() in ['english', 'en', 'eng']:
                pass  # This was a header, skip it
            else:
                # This was data, include it
                if len(first_row) >= 2:
                    sentences.append((first_row[0].strip(), first_row[1].strip()))
            
            # Read the rest
            for row in reader:
                if len(row) >= 2:
                    sentences.append((row[0].strip(), row[1].strip()))
        
        return sentences
    
    @staticmethod
    def load_from_json(file_path: str) -> List[Tuple[str, str]]:
        """
        Load sentence pairs from JSON file.
        Expected format: [{"english": "...", "korean": "..."}, ...]
        """
        sentences = []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        for item in data:
            if isinstance(item, dict) and 'english' in item and 'korean' in item:
                sentences.append((item['english'], item['korean']))
        
        return sentences
    
    @staticmethod
    def load_from_excel(file_path: str, sheet_name: str = None) -> List[Tuple[str, str]]:
        """
        Load sentence pairs from Excel file.
        """
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        sentences = []
        
        # Try to find english and korean columns
        en_col = None
        ko_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if 'english' in col_lower or 'en' == col_lower:
                en_col = col
            elif 'korean' in col_lower or 'ko' == col_lower or '한국어' in col:
                ko_col = col
        
        if en_col and ko_col:
            for _, row in df.iterrows():
                if pd.notna(row[en_col]) and pd.notna(row[ko_col]):
                    sentences.append((str(row[en_col]).strip(), str(row[ko_col]).strip()))
        else:
            # Assume first two columns
            for _, row in df.iterrows():
                if pd.notna(row.iloc[0]) and pd.notna(row.iloc[1]):
                    sentences.append((str(row.iloc[0]).strip(), str(row.iloc[1]).strip()))
        
        return sentences
    
    @staticmethod
    def load_sentences(file_path: str) -> List[Tuple[str, str]]:
        """
        Automatically detect file type and load sentences.
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.csv':
            return DataLoader.load_from_csv(file_path)
        elif ext == '.json':
            return DataLoader.load_from_json(file_path)
        elif ext in ['.xlsx', '.xls']:
            return DataLoader.load_from_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    @staticmethod
    def create_sample_data(output_path: str):
        """Create a sample CSV file for testing."""
        sample_sentences = [
            ("Hello, how are you?", "안녕하세요, 어떻게 지내세요?"),
            ("I'm learning English.", "저는 영어를 배우고 있습니다."),
            ("Nice to meet you.", "만나서 반갑습니다."),
            ("What's your name?", "이름이 무엇입니까?"),
            ("I love studying languages.", "저는 언어 공부하는 것을 좋아합니다."),
            ("The weather is nice today.", "오늘 날씨가 좋네요."),
            ("Let's practice together.", "함께 연습해요."),
            ("Thank you very much.", "정말 감사합니다."),
            ("See you tomorrow.", "내일 봐요."),
            ("Have a great day!", "좋은 하루 보내세요!")
        ]
        
        with open(output_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['English', 'Korean'])
            writer.writerows(sample_sentences)
        
        print(f"Sample data created at: {output_path}")