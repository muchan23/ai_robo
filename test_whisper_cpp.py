#!/usr/bin/env python3
"""
Whisper.cpp音声認識テストスクリプト
"""

import sys
import logging
from pathlib import Path

# プロジェクトのsrcディレクトリをパスに追加
sys.path.append(str(Path(__file__).parent / 'src'))

from src.voice_system.speech.whisper_cpp import WhisperCppSTT


def main():
    """テスト用のメイン関数"""
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🎤 Whisper.cpp音声認識テスト")
    print("=" * 50)
    
    try:
        # WhisperCppSTTインスタンスを作成
        print("📦 WhisperCppSTTを初期化中...")
        stt = WhisperCppSTT(model_size="small")
        
        # モデル情報を表示
        model_info = stt.get_model_info()
        print(f"✅ モデル情報: {model_info}")
        
        print("\n🎯 使用方法:")
        print("1. 音声ファイルを指定してテスト:")
        print("   python test_whisper_cpp.py --file path/to/audio.wav")
        print("\n2. モデルサイズを指定:")
        print("   python test_whisper_cpp.py --file audio.wav --model-size tiny")
        
        # コマンドライン引数がある場合は実際にテスト
        if len(sys.argv) > 1:
            import argparse
            
            parser = argparse.ArgumentParser(description='Whisper.cpp音声認識テスト')
            parser.add_argument('--file', help='音声ファイルのパス')
            parser.add_argument('--model-size', default='small',
                               choices=['tiny', 'base', 'small', 'medium', 'large'],
                               help='モデルサイズ')
            
            args = parser.parse_args()
            
            if args.file:
                print(f"\n🎵 音声ファイルを処理中: {args.file}")
                result = stt.transcribe_audio_file(args.file)
                print(f"📝 文字起こし結果: {result}")
            else:
                print("❌ 音声ファイルが指定されていません")
                return 1
        
        print("\n✅ テスト完了！")
        return 0
        
    except ImportError as e:
        print(f"❌ 依存関係エラー: {e}")
        print("💡 解決方法:")
        print("   pip install faster-whisper")
        return 1
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
