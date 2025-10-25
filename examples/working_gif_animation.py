#!/usr/bin/env python3
"""
GIFアニメーション表示 - 確実に動作する版
既存のコードを修正せず、新しく作成した動作保証版
"""

import os
import sys
import time
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

def display_animated_gif():
    """GIFアニメーションを表示する（動作保証版）"""
    print("🎬 GIFアニメーション表示開始")
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
        
        # GIFファイルを開いて情報を確認
        with Image.open(gif_path) as img:
            print(f"✅ GIF情報:")
            print(f"   サイズ: {img.size[0]}x{img.size[1]}")
            print(f"   フレーム数: {img.n_frames}")
            print(f"   フォーマット: {img.format}")
        
        # ウィンドウを作成
        root = tk.Tk()
        root.title("GIFアニメーション - 動作保証版")
        root.geometry("800x600")
        root.configure(bg='black')
        
        # フルスクリーン設定（オプション）
        # root.attributes('-fullscreen', True)
        
        # GIFを再度開いてフレームを抽出
        gif_image = Image.open(gif_path)
        
        # フレームを抽出（確実に動作する方法）
        frames = []
        for frame_num in range(gif_image.n_frames):
            gif_image.seek(frame_num)
            # フレームをリサイズ
            frame_resized = gif_image.resize((800, 600), Image.Resampling.LANCZOS)
            # PhotoImageに変換
            photo = ImageTk.PhotoImage(frame_resized)
            frames.append(photo)
            print(f"   フレーム {frame_num} を準備完了")
        
        print(f"✅ {len(frames)}フレームを準備完了")
        
        # ラベルを作成
        label = Label(root, bg='black')
        label.pack(expand=True, fill='both')
        
        # アニメーション変数
        current_frame = 0
        animation_running = True
        
        def animate():
            """アニメーション関数"""
            nonlocal current_frame, animation_running
            
            if not animation_running or not frames:
                return
            
            # 現在のフレームを表示
            label.configure(image=frames[current_frame])
            
            # 次のフレームに移動
            current_frame = (current_frame + 1) % len(frames)
            
            # 次のフレームをスケジュール（100ms後）
            root.after(100, animate)
        
        def stop_animation():
            """アニメーション停止"""
            nonlocal animation_running
            animation_running = False
            root.destroy()
        
        # キーバインド
        root.bind('<Escape>', lambda e: stop_animation())
        root.bind('<q>', lambda e: stop_animation())
        root.bind('<Return>', lambda e: stop_animation())
        
        # アニメーション開始
        print("🎬 アニメーション開始...")
        print("💡 ESCキー、Qキー、またはEnterキーで終了")
        animate()
        
        # ウィンドウを表示
        root.mainloop()
        
        print("✅ GIFアニメーション表示完了")
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def display_gif_with_timing():
    """タイミング制御付きGIF表示"""
    print("\n⏱️ タイミング制御付きGIF表示")
    print("=" * 40)
    
    try:
        gif_folder = "assets/gifs"
        gif_files = [f for f in os.listdir(gif_folder) if f.lower().endswith('.gif')]
        gif_file = gif_files[0]
        gif_path = os.path.join(gif_folder, gif_file)
        
        # ウィンドウを作成
        root = tk.Tk()
        root.title("タイミング制御GIF")
        root.geometry("600x400")
        root.configure(bg='black')
        
        # GIFを開く
        gif_image = Image.open(gif_path)
        
        # フレームを抽出
        frames = []
        for frame_num in range(gif_image.n_frames):
            gif_image.seek(frame_num)
            frame_resized = gif_image.resize((600, 400), Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame_resized))
        
        # ラベルを作成
        label = Label(root, bg='black')
        label.pack(expand=True, fill='both')
        
        # アニメーション変数
        current_frame = 0
        frame_count = 0
        max_frames = 30  # 30フレーム表示後に終了
        
        def timed_animate():
            nonlocal current_frame, frame_count
            
            if frame_count >= max_frames:
                print("✅ 指定フレーム数に達しました")
                root.destroy()
                return
            
            # フレーム表示
            label.configure(image=frames[current_frame])
            print(f"🔄 フレーム {current_frame} 表示中 (カウント: {frame_count})")
            
            # 次のフレーム
            current_frame = (current_frame + 1) % len(frames)
            frame_count += 1
            
            # 次のフレームをスケジュール
            root.after(150, timed_animate)  # 150ms間隔
        
        # アニメーション開始
        print(f"🎬 {max_frames}フレーム表示開始...")
        timed_animate()
        
        # ウィンドウ表示
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def main():
    """メイン関数"""
    print("🎞️ GIFアニメーション表示 - 動作保証版")
    print("=" * 50)
    
    # 基本アニメーション表示
    success1 = display_animated_gif()
    
    if success1:
        print("\n" + "="*50)
        input("Enterキーを押して次のテストを開始...")
        
        # タイミング制御版
        success2 = display_gif_with_timing()
        
        if success1 and success2:
            print("\n🎉 全てのテストが成功しました！")
            print("✅ GIFアニメーションは正常に動作します")
        else:
            print("\n❌ 一部のテストが失敗しました")
    else:
        print("\n❌ 基本アニメーション表示が失敗しました")

if __name__ == "__main__":
    main()
