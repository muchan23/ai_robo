#!/usr/bin/env python3
"""
GIF表示テスト
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.display.gif_player import GIFPlayer

def test_gif_player():
    """GIF表示テスト"""
    print("🎬 GIF表示テスト")
    print("=" * 30)
    
    try:
        gif_player = GIFPlayer()
        print("✅ GIF表示システムの初期化に成功")
        
        if not gif_player.gif_files:
            print("❌ GIFファイルが見つかりません")
            print("💡 プロジェクトルートにGIFファイルを配置してください")
            return
        
        print(f"✅ {len(gif_player.gif_files)}個のGIFファイルを発見")
        print("🎯 GIF表示を開始します")
        print("💡 ESCキーで終了、F11キーでフルスクリーン切り替え")
        
        # ランダムなGIFを表示
        gif_player.show_random_gif()
        
        # ウィンドウのイベントループを開始
        if gif_player.root:
            gif_player.root.mainloop()
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
    finally:
        if 'gif_player' in locals():
            gif_player.cleanup()

if __name__ == "__main__":
    test_gif_player()
