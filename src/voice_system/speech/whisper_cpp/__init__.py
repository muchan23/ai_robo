"""
Whisper.cpp音声認識モジュール
ローカル環境で高速な音声認識を提供
"""

from .whisper_cpp_stt import WhisperCppSTT
from .realtime_whisper import RealtimeWhisper

__all__ = ['WhisperCppSTT', 'RealtimeWhisper']
