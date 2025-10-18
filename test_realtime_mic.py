#!/usr/bin/env python3
"""
Whisper.cppリアルタイム音声認識テストスクリプト（マイク入力版）
"""

import sys
import logging
import time
from pathlib import Path

# プロジェクトのsrcディレクトリをパスに追加
sys.path.append(str(Path(__file__).parent / 'src'))

from src.voice_system.speech.whisper_cpp import RealtimeWhisper


def main():
    """メイン関数"""
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🎤 Whisper.cppリアルタイム音声認識テスト（マイク入力版）")
    print("=" * 60)
    
    def on_transcription(text: str):
        print(f"🎤 認識結果: {text}")
    
    def on_error(error: Exception):
        print(f"❌ エラー: {error}")
    
    try:
        # RealtimeWhisperインスタンスを作成
        print("📦 RealtimeWhisperを初期化中...")
        realtime_whisper = RealtimeWhisper(model_size="small")
        
        print("🎯 マイクからの音声認識を開始します")
        print("💡 話しかけてください...")
        print("⏹️  Ctrl+C で停止")
        
        # 音声認識を開始
        realtime_whisper.start_listening(
            on_transcription=on_transcription,
            on_error=on_error
        )
        
        # メインループ
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n🛑 停止中...")
            realtime_whisper.stop_listening()
            print("✅ テストを停止しました")
            
    except ImportError as e:
        print(f"❌ 依存関係エラー: {e}")
        print("💡 解決方法:")
        print("   pip install faster-whisper numpy pyaudio")
        return 1
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
