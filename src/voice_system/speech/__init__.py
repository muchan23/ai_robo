"""
音声認識・合成モジュール
音声の認識と音声合成機能
"""

from .recognition import SpeechToText
from .synthesis import TextToSpeech

__all__ = ['SpeechToText', 'TextToSpeech']
