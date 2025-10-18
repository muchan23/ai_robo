#!/usr/bin/env python3
"""
ラズパイ用Whisper.cppテストスクリプト
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

def test_import():
    """importテスト"""
    print("🔍 モジュールimportテスト中...")
    
    try:
        from src.voice_system.speech.whisper_cpp import WhisperCppSTT, RealtimeWhisper
        print("✅ WhisperCppSTT, RealtimeWhisper のimport成功")
        return True
    except ImportError as e:
        print(f"❌ importエラー: {e}")
        return False

def test_whisper_cpp():
    """WhisperCppSTTテスト"""
    print("\n🎤 WhisperCppSTTテスト中...")
    
    try:
        from src.voice_system.speech.whisper_cpp import WhisperCppSTT
        
        # 初期化テスト
        stt = WhisperCppSTT(model_size="tiny")  # 軽量モデルを使用
        model_info = stt.get_model_info()
        print(f"✅ WhisperCppSTT初期化成功: {model_info}")
        return True
        
    except ImportError as e:
        print(f"❌ 依存関係エラー: {e}")
        print("💡 解決方法:")
        print("   pip install faster-whisper")
        return False
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return False

def test_realtime_whisper():
    """RealtimeWhisperテスト"""
    print("\n🎤 RealtimeWhisperテスト中...")
    
    try:
        from src.voice_system.speech.whisper_cpp import RealtimeWhisper
        
        # 初期化テスト（実際の音声認識は開始しない）
        realtime_whisper = RealtimeWhisper(model_size="tiny")
        print("✅ RealtimeWhisper初期化成功")
        return True
        
    except ImportError as e:
        print(f"❌ 依存関係エラー: {e}")
        print("💡 解決方法:")
        print("   pip install faster-whisper numpy pyaudio")
        return False
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return False

def main():
    """メイン関数"""
    print("🍓 ラズパイ用Whisper.cppテスト")
    print("=" * 50)
    
    # テスト実行
    tests = [
        ("importテスト", test_import),
        ("WhisperCppSTTテスト", test_whisper_cpp),
        ("RealtimeWhisperテスト", test_realtime_whisper)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}実行中...")
        result = test_func()
        results.append((test_name, result))
    
    # 結果表示
    print("\n" + "=" * 50)
    print("📊 テスト結果:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 すべてのテストが成功しました！")
        print("💡 次のステップ:")
        print("   python test_realtime_mic.py  # リアルタイム音声認識テスト")
    else:
        print("\n⚠️  一部のテストが失敗しました")
        print("💡 依存関係を確認してください:")
        print("   pip install -r requirements.txt")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
