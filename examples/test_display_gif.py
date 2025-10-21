#!/usr/bin/env python3
"""
ラズパイディスプレイGIF表示テスト
assets/gifs/フォルダのGIFファイルをディスプレイに表示
"""

import os
import sys
import time
from pathlib import Path

def test_tkinter_import():
    """Tkinterライブラリのインポートテスト"""
    print("🖥️ Tkinterライブラリのテスト")
    print("-" * 30)
    
    try:
        import tkinter as tk
        from tkinter import Label
        print("✅ Tkinter のインポートに成功")
        
        # バージョン情報を表示
        print(f"   Tkinterバージョン: {tk.TkVersion}")
        print(f"   Tclバージョン: {tk.TclVersion}")
        
        return True
    except ImportError as e:
        print(f"❌ Tkinter のインポートに失敗: {e}")
        print("💡 ラズパイでTkinterを有効化してください:")
        print("   sudo apt-get install python3-tk")
        return False

def test_display_creation():
    """ディスプレイ作成テスト"""
    print("\n🖼️ ディスプレイ作成テスト")
    print("-" * 30)
    
    try:
        import tkinter as tk
        from tkinter import Label
        
        # ウィンドウを作成
        root = tk.Tk()
        root.title("GIF表示テスト")
        root.geometry("800x600")
        root.configure(bg='black')
        
        # ラベルを作成
        label = Label(root, text="ディスプレイテスト", bg='black', fg='white', font=('Arial', 24))
        label.pack(expand=True, fill='both')
        
        print("✅ ディスプレイの作成に成功")
        print("   サイズ: 800x600")
        print("   背景色: 黒")
        
        # 3秒間表示
        print("⏱️ 3秒間表示します...")
        root.update()
        time.sleep(3)
        
        # ウィンドウを閉じる
        root.destroy()
        print("✅ ディスプレイのテスト完了")
        
        return True
        
    except Exception as e:
        print(f"❌ ディスプレイ作成に失敗: {e}")
        return False

def test_gif_display():
    """GIF表示テスト"""
    print("\n🎬 GIF表示テスト")
    print("-" * 30)
    
    try:
        from PIL import Image, ImageTk
        import tkinter as tk
        from tkinter import Label
        
        # GIFファイルの確認
        gif_folder = "assets/gifs"
        gif_files = [f for f in os.listdir(gif_folder) if f.lower().endswith('.gif')]
        
        if not gif_files:
            print("❌ GIFファイルが見つかりません")
            return False
        
        gif_file = gif_files[0]
        gif_path = os.path.join(gif_folder, gif_file)
        print(f"📁 表示ファイル: {gif_file}")
        
        # ウィンドウを作成
        root = tk.Tk()
        root.title("GIF表示テスト")
        root.geometry("800x600")
        root.configure(bg='black')
        
        # フルスクリーン設定
        root.attributes('-fullscreen', True)
        
        # GIFを読み込み
        gif_image = Image.open(gif_path)
        gif_resized = gif_image.resize((800, 600), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(gif_resized)
        
        # ラベルに表示
        label = Label(root, image=photo, bg='black')
        label.pack(expand=True, fill='both')
        
        print("✅ GIF表示に成功")
        print("   フルスクリーンモード")
        print("⏱️ 5秒間表示します...")
        print("💡 ESCキーで終了")
        
        # キーバインド
        def on_escape(event):
            root.destroy()
        root.bind('<Escape>', on_escape)
        
        # 表示
        root.update()
        time.sleep(5)
        
        # ウィンドウを閉じる
        root.destroy()
        print("✅ GIF表示テスト完了")
        
        return True
        
    except Exception as e:
        print(f"❌ GIF表示に失敗: {e}")
        return False

def test_gif_animation():
    """GIFアニメーション表示テスト"""
    print("\n🎞️ GIFアニメーション表示テスト")
    print("-" * 30)
    
    try:
        from PIL import Image, ImageTk
        import tkinter as tk
        from tkinter import Label
        
        # GIFファイルの確認
        gif_folder = "assets/gifs"
        gif_files = [f for f in os.listdir(gif_folder) if f.lower().endswith('.gif')]
        
        if not gif_files:
            print("❌ GIFファイルが見つかりません")
            return False
        
        gif_file = gif_files[0]
        gif_path = os.path.join(gif_folder, gif_file)
        print(f"📁 アニメーションファイル: {gif_file}")
        
        # ウィンドウを作成
        root = tk.Tk()
        root.title("GIFアニメーション表示テスト")
        root.geometry("800x600")
        root.configure(bg='black')
        
        # フルスクリーン設定
        root.attributes('-fullscreen', True)
        
        # GIFを読み込み
        gif_image = Image.open(gif_path)
        
        # フレームを抽出
        frames = []
        for frame in range(gif_image.n_frames):
            gif_image.seek(frame)
            frame_resized = gif_image.resize((800, 600), Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame_resized))
        
        print(f"✅ {len(frames)}フレームを読み込み")
        
        # ラベルを作成
        label = Label(root, bg='black')
        label.pack(expand=True, fill='both')
        
        # アニメーション変数
        current_frame = 0
        
        def animate():
            nonlocal current_frame
            if frames:
                label.configure(image=frames[current_frame])
                current_frame = (current_frame + 1) % len(frames)
                root.after(100, animate)  # 100ms間隔
        
        # アニメーション開始
        animate()
        
        print("✅ GIFアニメーション表示に成功")
        print("⏱️ 10秒間アニメーション表示します...")
        print("💡 ESCキーで終了")
        
        # キーバインド
        def on_escape(event):
            root.destroy()
        root.bind('<Escape>', on_escape)
        
        # 表示
        root.update()
        time.sleep(10)
        
        # ウィンドウを閉じる
        root.destroy()
        print("✅ GIFアニメーション表示テスト完了")
        
        return True
        
    except Exception as e:
        print(f"❌ GIFアニメーション表示に失敗: {e}")
        return False

def main():
    """メイン関数"""
    print("🎬 ラズパイディスプレイGIF表示テスト")
    print("=" * 50)
    
    # テスト1: Tkinterライブラリの確認
    if not test_tkinter_import():
        return 1
    
    # テスト2: ディスプレイ作成テスト
    if not test_display_creation():
        return 1
    
    # テスト3: GIF表示テスト
    if not test_gif_display():
        return 1
    
    # テスト4: GIFアニメーション表示テスト
    if not test_gif_animation():
        return 1
    
    print("\n🎉 すべてのテストが成功しました！")
    print("💡 ラズパイでGIF表示が正常に動作します")
    
    return 0

if __name__ == "__main__":
    exit(main())
