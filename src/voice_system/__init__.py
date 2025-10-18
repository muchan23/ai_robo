"""
音声システムモジュール
音声認識、AI対話、音声合成の統合システム
"""

from .conversation import VoiceConversation
from .audio.recorder import AudioRecorder
from .speech.recognition import SpeechToText
from .speech.synthesis import TextToSpeech
from .ai.chat import AIChat

__all__ = [
    'VoiceConversation',
    'AudioRecorder',
    'SpeechToText',
    'TextToSpeech',
    'AIChat'
]
