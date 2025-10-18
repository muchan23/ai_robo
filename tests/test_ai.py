#!/usr/bin/env python3
"""
AI対話テスト
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ai.ai_chat import AIChat

def test_ai_chat():
    """AI対話テスト"""
    print("🤖 AI対話テスト")
    print("=" * 30)
    
    try:
        ai_chat = AIChat()
        print("✅ AI対話システムの初期化に成功")
        
        # テストメッセージ
        test_message = "こんにちは、元気ですか？"
        print(f"👤 テストメッセージ: {test_message}")
        
        # AI応答を生成
        print("🤖 AI応答を生成中...")
        response = ai_chat.chat(test_message)
        
        if response:
            print(f"✅ AI応答成功: {response}")
        else:
            print("❌ AI応答に失敗")
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")

if __name__ == "__main__":
    test_ai_chat()
