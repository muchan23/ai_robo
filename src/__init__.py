"""
AI Robot プロジェクト
OpenAI Whisper APIを使用した自律型ロボット制御システム
"""

__version__ = "0.1.0"
__author__ = "AI Robot Team"
__description__ = "OpenAI Whisper APIを使用した音声認識システム"

# 主要モジュールのインポート
from .speech_to_text import SpeechToText
from .config import Config, get_config
from .audio_recorder import AudioRecorder
from .ai_chat import AIChat
from .text_to_speech import TextToSpeech
from .voice_conversation import VoiceConversation

__all__ = [
    'SpeechToText',
    'Config', 
    'get_config',
    'AudioRecorder',
    'AIChat',
    'TextToSpeech',
    'VoiceConversation'
]
