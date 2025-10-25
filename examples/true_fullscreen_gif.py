#!/usr/bin/env python3
"""
真の全画面GIF表示 - ラズパイのタスクバーを隠す
タスクバーを完全に隠して真の全画面表示を実現
"""

import os
import sys
import time
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import subprocess

def hide_taskbar():
    """ラズパイのタスクバーを隠す"""
    try:
        # LXPanel（ラズパイのデフォルトパネル）を隠す
        subprocess.run(['pkill', '-f', 'lxpanel'], check=False)
        print("✅ タスクバーを隠しました")
        return True
    except Exception as e:
        print(f"⚠️  タスクバーを隠せませんでした: {e}")
        return False

def show_taskbar():
    """ラズパイのタスクバーを表示"""
    try:
        # LXPanelを再起動
        subprocess.Popen(['lxpanel', '&'], shell=True)
        print("✅ タスクバーを復元しました")
        return True
    except Exception as e:
        print(f"⚠️  タスクバーを復元できませんでした: {e}")
        return False

def get_true_screen_size():
    """画面サイズを1024x768に固定"""
    return 1024, 768

def display_true_fullscreen_gif(duration_seconds=5):
    """真の全画面GIF表示（タスクバーを隠す）"""
    print("🍓 真の全画面GIF表示")
    print("=" * 40)
    
    taskbar_hidden = False
    
    try:
        # タスクバーを隠す
        print("🔧 タスクバーを隠しています...")
        taskbar_hidden = hide_taskbar()
        time.sleep(1)  # タスクバーが完全に隠れるまで待機
        
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
        
        # 画面サイズを1024x768に固定
        screen_width, screen_height = get_true_screen_size()
        print(f"🖥️  固定画面サイズ: {screen_width}x{screen_height}")
        
        # GIFファイルを開いて情報を確認
        with Image.open(gif_path) as img:
            print(f"✅ GIF情報:")
            print(f"   サイズ: {img.size[0]}x{img.size[1]}")
            print(f"   フレーム数: {img.n_frames}")
            print(f"   フォーマット: {img.format}")
        
        # ウィンドウを作成
        root = tk.Tk()
        root.title("真の全画面GIF")
        
        # 真の全画面設定
        root.attributes('-fullscreen', True)
        root.attributes('-topmost', True)  # 最前面に表示
        root.configure(bg='black')
        
        # ウィンドウの位置とサイズを1024x768に設定
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # GIFを再度開いてフレームを抽出
        gif_image = Image.open(gif_path)
        
        # フレームを抽出（1024x768に合わせてリサイズ）
        frames = []
        for frame_num in range(gif_image.n_frames):
            gif_image.seek(frame_num)
            # 1024x768に合わせてリサイズ
            frame_resized = gif_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(frame_resized)
            frames.append(photo)
            print(f"   フレーム {frame_num} を準備完了")
        
        print(f"✅ {len(frames)}フレームを準備完了")
        
        # ラベルを作成（真の全画面）
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
        
        # キーバインド（真の全画面でも動作）
        root.bind('<Escape>', lambda e: force_exit())
        root.bind('<q>', lambda e: force_exit())
        root.bind('<Return>', lambda e: force_exit())
        root.bind('<space>', lambda e: force_exit())
        
        # マウスクリックでも終了
        root.bind('<Button-1>', lambda e: force_exit())
        
        # アニメーション開始
        print(f"🎬 真の全画面アニメーション開始... ({duration_seconds}秒間)")
        print("💡 ESCキー、Qキー、Enterキー、Spaceキー、またはクリックで終了")
        animate()
        
        # ウィンドウを表示
        root.mainloop()
        
        print("✅ 真の全画面GIF表示完了")
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False
    finally:
        # タスクバーを復元
        if taskbar_hidden:
            print("🔧 タスクバーを復元しています...")
            show_taskbar()
            time.sleep(1)  # タスクバーが復元されるまで待機

def display_fullscreen_with_hide_panel(duration_seconds=5):
    """パネルを隠して全画面表示"""
    print("\n🔧 パネル隠し全画面GIF表示")
    print("=" * 40)
    
    try:
        # パネルを隠す
        print("🔧 パネルを隠しています...")
        subprocess.run(['pkill', '-f', 'lxpanel'], check=False)
        time.sleep(1)
        
        gif_folder = "assets/gifs"
        gif_files = [f for f in os.listdir(gif_folder) if f.lower().endswith('.gif')]
        gif_file = gif_files[0]
        gif_path = os.path.join(gif_folder, gif_file)
        
        # ウィンドウを作成
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.attributes('-topmost', True)
        root.configure(bg='black')
        
        # 画面サイズを1024x768に固定
        screen_width, screen_height = 1024, 768
        print(f"🖥️  固定画面サイズ: {screen_width}x{screen_height}")
        
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
        
        # アニメーション変数
        current_frame = 0
        animation_running = True
        start_time = time.time()
        
        def animate():
            nonlocal current_frame, animation_running
            
            if not animation_running or not frames:
                return
            
            elapsed_time = time.time() - start_time
            if elapsed_time >= duration_seconds:
                print(f"⏰ {duration_seconds}秒経過、アニメーション終了")
                animation_running = False
                root.destroy()
                return
            
            # フレーム表示
            label.configure(image=frames[current_frame])
            current_frame = (current_frame + 1) % len(frames)
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
        print(f"🎬 パネル隠し全画面アニメーション開始... ({duration_seconds}秒間)")
        animate()
        
        # ウィンドウ表示
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False
    finally:
        # パネルを復元
        print("🔧 パネルを復元しています...")
        subprocess.Popen(['lxpanel', '&'], shell=True)
        time.sleep(1)

def main():
    """メイン関数"""
    print("🍓 真の全画面GIF表示（タスクバー隠し）")
    print("=" * 50)
    
    # 表示時間を設定（秒）
    display_duration = 5  # 5秒間表示
    
    print(f"⏱️  表示時間: {display_duration}秒")
    print("💡 途中で終了したい場合は ESCキー、Qキー、Enterキー、Spaceキー、またはクリック")
    print("⚠️  注意: タスクバーが一時的に隠れますが、終了時に自動復元されます")
    
    # 真の全画面表示
    success1 = display_true_fullscreen_gif(display_duration)
    
    if success1:
        print("\n" + "="*50)
        input("Enterキーを押してパネル隠し版を開始...")
        
        # パネル隠し版
        success2 = display_fullscreen_with_hide_panel(display_duration)
        
        if success1 and success2:
            print("\n🎉 真の全画面GIF表示テスト完了！")
            print("✅ タスクバーを隠した真の全画面表示が正常に動作します")
        else:
            print("\n❌ 一部のテストが失敗しました")
    else:
        print("\n❌ 真の全画面GIF表示が失敗しました")

if __name__ == "__main__":
    main()
