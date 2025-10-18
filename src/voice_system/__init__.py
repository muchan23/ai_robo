"""
音声システムモジュール
音声認識、AI対話、音声合成の統合システム
"""

from src.voice_system.conversation import VoiceConversation
from src.voice_system.audio.recorder import AudioRecorder
from src.voice_system.speech.recognition import SpeechToText
from src.voice_system.speech.synthesis import TextToSpeech
from src.voice_system.ai.chat import AIChat

__all__ = [
    'VoiceConversation',
    'AudioRecorder',
    'SpeechToText',
    'TextToSpeech',
    'AIChat'
]
