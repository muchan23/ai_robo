#!/usr/bin/env python3
"""
ラズパイ用GIF全画面表示
テスト用に指定秒数だけ全画面表示
"""

import os
import sys
import time
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import threading

def get_display_info():
    """ディスプレイ情報を取得"""
    try:
        import subprocess
        result = subprocess.run(['xrandr'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if ' connected' in line and 'primary' in line:
                # 例: "HDMI-1 connected primary 1920x1080+0+0"
                parts = line.split()
                for part in parts:
                    if 'x' in part and '+' in part:
                        resolution = part.split('+')[0]
                        return resolution
        return "1920x1080"  # デフォルト
    except:
        return "1920x1080"  # デフォルト

def display_fullscreen_gif(duration_seconds=5):
    """ラズパイでGIFを全画面表示（指定秒数）"""
    print("🍓 ラズパイ全画面GIF表示")
    print("=" * 40)
    
    try:
        # GIFファイルの確認
        gif_folder = "assets/gifs"
        if not os.path.exists(gif_folder):
            print(f"❌ フォルダが見つかりません: {gif_folder}")
            return False
        
        gif_files = [f for f in os.listdir(gif_folder) if f.lower().endswith('.gif')]
        if not gif_files:
            print("❌ GIFファイルが見つかりません")
            return False
        
        gif_file = gif_files[0]
        gif_path = os.path.join(gif_folder, gif_file)
        print(f"📁 ファイル: {gif_file}")
        
        # ディスプレイ情報を取得
        display_resolution = get_display_info()
        print(f"🖥️  ディスプレイ解像度: {display_resolution}")
        
        # GIFファイルを開いて情報を確認
        with Image.open(gif_path) as img:
            print(f"✅ GIF情報:")
            print(f"   サイズ: {img.size[0]}x{img.size[1]}")
            print(f"   フレーム数: {img.n_frames}")
            print(f"   フォーマット: {img.format}")
        
        # ウィンドウを作成
        root = tk.Tk()
        root.title("ラズパイ全画面GIF")
        
        # 全画面設定
        root.attributes('-fullscreen', True)
        root.configure(bg='black')
        
        # ディスプレイサイズを取得
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        print(f"🖥️  画面サイズ: {screen_width}x{screen_height}")
        
        # GIFを再度開いてフレームを抽出
        gif_image = Image.open(gif_path)
        
        # フレームを抽出（画面サイズに合わせてリサイズ）
        frames = []
        for frame_num in range(gif_image.n_frames):
            gif_image.seek(frame_num)
            # 画面サイズに合わせてリサイズ（アスペクト比を保持）
            frame_resized = gif_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(frame_resized)
            frames.append(photo)
            print(f"   フレーム {frame_num} を準備完了")
        
        print(f"✅ {len(frames)}フレームを準備完了")
        
        # ラベルを作成（全画面）
        label = Label(root, bg='black')
        label.pack(expand=True, fill='both')
        
        # アニメーション変数
        current_frame = 0
        animation_running = True
        start_time = time.time()
        
        def animate():
            """アニメーション関数"""
            nonlocal current_frame, animation_running
            
            if not animation_running or not frames:
                return
            
            # 指定時間が経過したら終了
            elapsed_time = time.time() - start_time
            if elapsed_time >= duration_seconds:
                print(f"⏰ {duration_seconds}秒経過、アニメーション終了")
                animation_running = False
                root.destroy()
                return
            
            # 現在のフレームを表示
            label.configure(image=frames[current_frame])
            
            # 次のフレームに移動
            current_frame = (current_frame + 1) % len(frames)
            
            # 次のフレームをスケジュール（100ms後）
            root.after(100, animate)
        
        def force_exit():
            """強制終了"""
            nonlocal animation_running
            animation_running = False
            root.destroy()
        
        # キーバインド（全画面でも動作）
        root.bind('<Escape>', lambda e: force_exit())
        root.bind('<q>', lambda e: force_exit())
        root.bind('<Return>', lambda e: force_exit())
        root.bind('<space>', lambda e: force_exit())
        
        # マウスクリックでも終了
        root.bind('<Button-1>', lambda e: force_exit())
        
        # アニメーション開始
        print(f"🎬 全画面アニメーション開始... ({duration_seconds}秒間)")
        print("💡 ESCキー、Qキー、Enterキー、Spaceキー、またはクリックで終了")
        animate()
        
        # ウィンドウを表示
        root.mainloop()
        
        print("✅ 全画面GIF表示完了")
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def display_fullscreen_gif_with_progress(duration_seconds=5):
    """進捗表示付き全画面GIF表示"""
    print("\n📊 進捗表示付き全画面GIF")
    print("=" * 40)
    
    try:
        gif_folder = "assets/gifs"
        gif_files = [f for f in os.listdir(gif_folder) if f.lower().endswith('.gif')]
        gif_file = gif_files[0]
        gif_path = os.path.join(gif_folder, gif_file)
        
        # ウィンドウを作成
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.configure(bg='black')
        
        # 画面サイズを取得
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # GIFを開く
        gif_image = Image.open(gif_path)
        
        # フレームを抽出
        frames = []
        for frame_num in range(gif_image.n_frames):
            gif_image.seek(frame_num)
            frame_resized = gif_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame_resized))
        
        # ラベルを作成
        label = Label(root, bg='black')
        label.pack(expand=True, fill='both')
        
        # 進捗表示用ラベル
        progress_label = Label(root, text="", fg='white', bg='black', font=('Arial', 24))
        progress_label.place(x=50, y=50)
        
        # アニメーション変数
        current_frame = 0
        animation_running = True
        start_time = time.time()
        
        def animate():
            nonlocal current_frame, animation_running
            
            if not animation_running or not frames:
                return
            
            # 経過時間と進捗を計算
            elapsed_time = time.time() - start_time
            progress = (elapsed_time / duration_seconds) * 100
            
            if elapsed_time >= duration_seconds:
                print(f"⏰ {duration_seconds}秒経過、アニメーション終了")
                animation_running = False
                root.destroy()
                return
            
            # フレーム表示
            label.configure(image=frames[current_frame])
            
            # 進捗表示
            progress_text = f"進捗: {progress:.1f}% ({elapsed_time:.1f}s/{duration_seconds}s)"
            progress_label.configure(text=progress_text)
            
            # 次のフレーム
            current_frame = (current_frame + 1) % len(frames)
            
            # 次のフレームをスケジュール
            root.after(100, animate)
        
        def force_exit():
            nonlocal animation_running
            animation_running = False
            root.destroy()
        
        # キーバインド
        root.bind('<Escape>', lambda e: force_exit())
        root.bind('<q>', lambda e: force_exit())
        root.bind('<Return>', lambda e: force_exit())
        root.bind('<Button-1>', lambda e: force_exit())
        
        # アニメーション開始
        print(f"🎬 進捗表示付き全画面アニメーション開始... ({duration_seconds}秒間)")
        animate()
        
        # ウィンドウ表示
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def main():
    """メイン関数"""
    print("🍓 ラズパイ全画面GIF表示")
    print("=" * 50)
    
    # 表示時間を設定（秒）
    display_duration = 5  # 5秒間表示
    
    print(f"⏱️  表示時間: {display_duration}秒")
    print("💡 途中で終了したい場合は ESCキー、Qキー、Enterキー、Spaceキー、またはクリック")
    
    # 基本全画面表示
    success1 = display_fullscreen_gif(display_duration)
    
    if success1:
        print("\n" + "="*50)
        input("Enterキーを押して進捗表示版を開始...")
        
        # 進捗表示版
        success2 = display_fullscreen_gif_with_progress(display_duration)
        
        if success1 and success2:
            print("\n🎉 全画面GIF表示テスト完了！")
            print("✅ ラズパイで全画面GIF表示が正常に動作します")
        else:
            print("\n❌ 一部のテストが失敗しました")
    else:
        print("\n❌ 全画面GIF表示が失敗しました")

if __name__ == "__main__":
    main()
