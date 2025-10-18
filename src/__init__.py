"""
AI Robot プロジェクト
OpenAI Whisper APIを使用した自律型ロボット制御システム
"""

__version__ = "0.1.0"
__author__ = "AI Robot Team"
__description__ = "OpenAI Whisper APIを使用した音声認識システム"

# 主要モジュールのインポート
from src.config import Config, get_config
from src.voice_system import VoiceConversation, AudioRecorder, SpeechToText, TextToSpeech, AIChat

__all__ = [
    'Config', 
    'get_config',
    'VoiceConversation',
    'AudioRecorder',
    'SpeechToText',
    'TextToSpeech',
    'AIChat'
]
