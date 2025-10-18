"""
音声認識・合成モジュール
音声の認識と音声合成機能
"""

from src.voice_system.speech.recognition import SpeechToText
from src.voice_system.speech.synthesis import TextToSpeech
from src.voice_system.speech.whisper_cpp import WhisperCppSTT

__all__ = ['SpeechToText', 'TextToSpeech', 'WhisperCppSTT']
