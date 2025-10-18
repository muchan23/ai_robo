"""
音声認識・合成モジュール
音声の認識と音声合成機能
"""

from src.voice_system.speech.recognition import SpeechToText
from src.voice_system.speech.synthesis import TextToSpeech

__all__ = ['SpeechToText', 'TextToSpeech']
