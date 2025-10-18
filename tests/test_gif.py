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

from src.display.gif_player_ultra_simple import GIFPlayerUltraSimple

def test_gif_player():
    """GIF表示テスト"""
    print("🎬 GIF表示テスト")
    print("=" * 30)
    
    try:
        gif_player = GIFPlayerUltraSimple()
        print("✅ GIF表示システムの初期化に成功")
        
        if not gif_player.gif_files:
            print("❌ GIFファイルが見つかりません")
            print("💡 assets/gifsフォルダにGIFファイルを配置してください")
            return
        
        print(f"✅ {len(gif_player.gif_files)}個のGIFファイルを発見")
        print("🎯 GIF表示を開始します")
        print("💡 操作方法:")
        print("   ESCキー: 終了")
        print("   F11キー: フルスクリーン切り替え")
        print("   スペースキー: GIF表示切り替え")
        print("   Hキー: GIF非表示")
        print("   Sキー: GIF表示")
        
        # 継続的にGIFを表示
        gif_player.start_continuous_display()
        
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
