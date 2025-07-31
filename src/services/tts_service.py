import os
from abc import ABC, abstractmethod
from typing import List, Tuple
import azure.cognitiveservices.speech as speechsdk
from gtts import gTTS
from src.core.config import config


class TTSEngine(ABC):
    @abstractmethod
    def generate_audio(self, text: str, language: str, output_path: str) -> str:
        pass


class AzureTTS(TTSEngine):
    def __init__(self):
        if not config.azure_speech_key or not config.azure_speech_region:
            raise ValueError("Azure Speech credentials not configured")
        
        self.speech_config = speechsdk.SpeechConfig(
            subscription=config.azure_speech_key,
            region=config.azure_speech_region
        )
        
    def generate_audio(self, text: str, language: str, output_path: str) -> str:
        voice_name = config.tts_voice_en if language == "en" else config.tts_voice_ko
        self.speech_config.speech_synthesis_voice_name = voice_name
        
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )
        
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{language}">
            <voice name="{voice_name}">
                <prosody rate="{config.tts_speed}">
                    {text}
                </prosody>
            </voice>
        </speak>
        """
        
        result = synthesizer.speak_ssml_async(ssml).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return output_path
        else:
            raise Exception(f"Speech synthesis failed: {result.reason}")


class GoogleTTS(TTSEngine):
    def generate_audio(self, text: str, language: str, output_path: str) -> str:
        lang_code = "en" if language == "en" else "ko"
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(output_path)
        return output_path


class TTSService:
    def __init__(self):
        if config.tts_engine == "azure":
            self.engine = AzureTTS()
        else:
            self.engine = GoogleTTS()
    
    def generate_sentence_audio(self, sentences: List[Tuple[str, str]], 
                              output_dir: str) -> List[Tuple[str, str]]:
        """
        Generate audio files for English and Korean sentences.
        
        Args:
            sentences: List of (english, korean) sentence tuples
            output_dir: Directory to save audio files
            
        Returns:
            List of (english_audio_path, korean_audio_path) tuples
        """
        audio_files = []
        
        for i, (en_text, ko_text) in enumerate(sentences):
            en_audio_path = os.path.join(output_dir, f"sentence_{i}_en.wav")
            ko_audio_path = os.path.join(output_dir, f"sentence_{i}_ko.wav")
            
            self.engine.generate_audio(en_text, "en", en_audio_path)
            self.engine.generate_audio(ko_text, "ko", ko_audio_path)
            
            audio_files.append((en_audio_path, ko_audio_path))
        
        return audio_files