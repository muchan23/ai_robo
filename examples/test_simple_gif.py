#!/usr/bin/env python3
"""
シンプルなGIF表示テスト
assets/gifs/フォルダのGIFファイルを表示
"""

import os
import sys
from pathlib import Path

def test_gif_files():
    """GIFファイルの存在確認テスト"""
    print("🎬 シンプルなGIF表示テスト")
    print("=" * 40)
    
    # assets/gifsフォルダの確認
    gif_folder = "assets/gifs"
    
    if not os.path.exists(gif_folder):
        print(f"❌ フォルダが見つかりません: {gif_folder}")
        print("💡 assets/gifs/フォルダを作成してください")
        return False
    
    print(f"✅ フォルダが見つかりました: {gif_folder}")
    
    # GIFファイルの検索
    gif_files = []
    for file in os.listdir(gif_folder):
        if file.lower().endswith(('.gif', '.GIF')):
            gif_files.append(file)
    
    if not gif_files:
        print("❌ GIFファイルが見つかりません")
        print("💡 assets/gifs/フォルダにGIFファイルを配置してください")
        return False
    
    print(f"✅ {len(gif_files)}個のGIFファイルを発見:")
    for i, gif_file in enumerate(gif_files, 1):
        file_path = os.path.join(gif_folder, gif_file)
        file_size = os.path.getsize(file_path)
        print(f"   {i}. {gif_file} ({file_size:,} bytes)")
    
    return True

def test_pillow_import():
    """Pillowライブラリのインポートテスト"""
    print("\n📦 Pillowライブラリのテスト")
    print("-" * 30)
    
    try:
        from PIL import Image
        print("✅ PIL (Pillow) のインポートに成功")
        
        # バージョン情報を表示
        import PIL
        print(f"   バージョン: {PIL.__version__}")
        
        return True
    except ImportError as e:
        print(f"❌ PIL (Pillow) のインポートに失敗: {e}")
        print("💡 以下のコマンドでインストールしてください:")
        print("   pip install Pillow")
        return False

def test_gif_loading():
    """GIFファイルの読み込みテスト"""
    print("\n🖼️ GIFファイルの読み込みテスト")
    print("-" * 30)
    
    try:
        from PIL import Image
        
        gif_folder = "assets/gifs"
        gif_files = [f for f in os.listdir(gif_folder) if f.lower().endswith('.gif')]
        
        if not gif_files:
            print("❌ GIFファイルが見つかりません")
            return False
        
        # 最初のGIFファイルをテスト
        gif_file = gif_files[0]
        gif_path = os.path.join(gif_folder, gif_file)
        
        print(f"📁 テストファイル: {gif_file}")
        
        # GIFファイルを開く
        with Image.open(gif_path) as img:
            print(f"✅ GIFファイルの読み込みに成功")
            print(f"   サイズ: {img.size[0]}x{img.size[1]}")
            print(f"   モード: {img.mode}")
            print(f"   フォーマット: {img.format}")
            
            # フレーム数の確認
            if hasattr(img, 'n_frames'):
                print(f"   フレーム数: {img.n_frames}")
            else:
                print("   フレーム数: 1 (静止画)")
        
        return True
        
    except Exception as e:
        print(f"❌ GIFファイルの読み込みに失敗: {e}")
        return False

def main():
    """メイン関数"""
    print("🎬 ラズパイGIF表示テスト")
    print("=" * 50)
    
    # テスト1: GIFファイルの存在確認
    if not test_gif_files():
        return 1
    
    # テスト2: Pillowライブラリの確認
    if not test_pillow_import():
        return 1
    
    # テスト3: GIFファイルの読み込み
    if not test_gif_loading():
        return 1
    
    print("\n🎉 すべてのテストが成功しました！")
    print("💡 次のステップ: 実際のGIF表示機能を実装できます")
    
    return 0

if __name__ == "__main__":
    exit(main())
