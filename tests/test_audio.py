#!/usr/bin/env python3
"""
音声認識テスト
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.audio.voice_recognition_simple import VoiceRecognition

def test_voice_recognition():
    """音声認識テスト"""
    print("🎤 音声認識テスト")
    print("=" * 30)
    
    try:
        voice_recognition = VoiceRecognition()
        print("✅ 音声認識システムの初期化に成功")
        
        # 音声待機テスト
        print("🎤 音声を待機中... (5秒間)")
        audio_data = voice_recognition.wait_for_speech()
        
        if audio_data:
            print("✅ 音声検出に成功")
            
            # 文字起こしテスト
            print("📝 文字起こし中...")
            result = voice_recognition.transcribe_audio(audio_data)
            
            if result:
                print(f"✅ 文字起こし成功: {result}")
            else:
                print("❌ 文字起こしに失敗")
        else:
            print("❌ 音声検出に失敗")
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
    finally:
        if 'voice_recognition' in locals():
            voice_recognition.cleanup()

if __name__ == "__main__":
    test_voice_recognition()
