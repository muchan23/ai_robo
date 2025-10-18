#!/usr/bin/env python3
"""
Whisper.cppリアルタイム音声認識テストスクリプト
"""

import sys
import logging
import time
import threading
from pathlib import Path

# プロジェクトのsrcディレクトリをパスに追加
sys.path.append(str(Path(__file__).parent / 'src'))

from src.voice_system.speech.whisper_cpp import WhisperCppSTT


class RealtimeWhisperTest:
    """リアルタイム音声認識テストクラス"""
    
    def __init__(self):
        self.stt = None
        self.is_running = False
        
    def on_transcription_result(self, result_bytes: bytes):
        """文字起こし結果のコールバック"""
        result = result_bytes.decode('utf-8')
        print(f"🎤 認識結果: {result}")
    
    def start_realtime_test(self, model_size: str = "small"):
        """リアルタイム音声認識テストを開始"""
        
        print("🎤 Whisper.cppリアルタイム音声認識テスト")
        print("=" * 50)
        
        try:
            # WhisperCppSTTインスタンスを作成
            print("📦 WhisperCppSTTを初期化中...")
            self.stt = WhisperCppSTT(model_size=model_size)
            
            # モデル情報を表示
            model_info = self.stt.get_model_info()
            print(f"✅ モデル情報: {model_info}")
            
            print("\n🎯 リアルタイム音声認識を開始します")
            print("💡 注意: このテストは音声ファイルベースのシミュレーションです")
            print("   実際のマイク入力には音声録音機能が必要です")
            
            # リアルタイム音声認識を開始
            self.stt.start_realtime_transcription(
                audio_callback=self.on_transcription_result,
                sample_rate=16000,
                chunk_duration=1.0,
                language="ja"
            )
            
            self.is_running = True
            
            print("\n⏹️  Ctrl+C で停止")
            
            # メインループ
            try:
                while self.is_running:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("\n🛑 停止中...")
                self.stop_test()
                
        except ImportError as e:
            print(f"❌ 依存関係エラー: {e}")
            print("💡 解決方法:")
            print("   pip install faster-whisper")
            return 1
            
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            return 1
        
        return 0
    
    def stop_test(self):
        """テストを停止"""
        if self.stt:
            self.stt.stop_realtime_transcription()
        self.is_running = False
        print("✅ テストを停止しました")


def main():
    """メイン関数"""
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Whisper.cppリアルタイム音声認識テスト')
    parser.add_argument('--model-size', default='small',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='モデルサイズ')
    
    args = parser.parse_args()
    
    # テスト実行
    test = RealtimeWhisperTest()
    return test.start_realtime_test(args.model_size)


if __name__ == "__main__":
    exit(main())
