#!/usr/bin/env python3
"""
音声合成テスト
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.tts.tts_synthesis import TTSSynthesis

def test_tts_synthesis():
    """音声合成テスト"""
    print("🔊 音声合成テスト")
    print("=" * 30)
    
    try:
        tts = TTSSynthesis()
        print("✅ 音声合成システムの初期化に成功")
        
        # テストテキスト
        test_text = "こんにちは、音声合成のテストです。"
        print(f"📝 テストテキスト: {test_text}")
        
        # 音声合成・再生
        print("🔊 音声合成中...")
        tts.speak_text(test_text)
        print("✅ 音声合成・再生に成功")
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
    finally:
        if 'tts' in locals():
            tts.cleanup()

if __name__ == "__main__":
    test_tts_synthesis()
