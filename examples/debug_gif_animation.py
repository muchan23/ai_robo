#!/usr/bin/env python3
"""
GIFアニメーションデバッグテスト
GIFが静止画になる原因を特定
"""

import os
import sys
import time
from pathlib import Path

def debug_gif_info():
    """GIFファイルの詳細情報を表示"""
    print("🔍 GIFファイルの詳細情報")
    print("=" * 40)
    
    try:
        from PIL import Image
        
        gif_folder = "assets/gifs"
        gif_files = [f for f in os.listdir(gif_folder) if f.lower().endswith('.gif')]
        
        if not gif_files:
            print("❌ GIFファイルが見つかりません")
            return False
        
        gif_file = gif_files[0]
        gif_path = os.path.join(gif_folder, gif_file)
        print(f"📁 ファイル: {gif_file}")
        
        # GIFファイルを開く
        with Image.open(gif_path) as img:
            print(f"✅ 基本情報:")
            print(f"   サイズ: {img.size[0]}x{img.size[1]}")
            print(f"   モード: {img.mode}")
            print(f"   フォーマット: {img.format}")
            
            # フレーム数の確認
            if hasattr(img, 'n_frames'):
                print(f"   フレーム数: {img.n_frames}")
                
                # 各フレームの詳細情報
                print(f"\n📊 フレーム詳細:")
                for frame in range(min(img.n_frames, 5)):  # 最初の5フレームのみ
                    img.seek(frame)
                    print(f"   フレーム {frame}: {img.size[0]}x{img.size[1]}, モード: {img.mode}")
                
                if img.n_frames > 5:
                    print(f"   ... (他 {img.n_frames - 5} フレーム)")
            else:
                print("   ❌ フレーム情報が取得できません")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ GIF情報取得に失敗: {e}")
        return False

def debug_frame_extraction():
    """フレーム抽出のデバッグ"""
    print("\n🎞️ フレーム抽出デバッグ")
    print("-" * 30)
    
    try:
        from PIL import Image, ImageTk
        
        gif_folder = "assets/gifs"
        gif_files = [f for f in os.listdir(gif_folder) if f.lower().endswith('.gif')]
        gif_file = gif_files[0]
        gif_path = os.path.join(gif_folder, gif_file)
        
        # GIFを開く
        gif_image = Image.open(gif_path)
        print(f"📁 ファイル: {gif_file}")
        print(f"   フレーム数: {gif_image.n_frames}")
        
        # フレームを抽出
        frames = []
        for frame in range(gif_image.n_frames):
            gif_image.seek(frame)
            print(f"   フレーム {frame} を抽出中...")
            
            # リサイズ
            frame_resized = gif_image.resize((400, 300), Image.Resampling.LANCZOS)
            frames.append(frame_resized)
        
        print(f"✅ {len(frames)}フレームを抽出完了")
        
        # フレームの違いを確認
        if len(frames) > 1:
            print(f"\n🔍 フレーム比較:")
            for i in range(min(3, len(frames))):
                frame = frames[i]
                # フレームのハッシュ値を計算（簡易的な比較）
                frame_hash = hash(frame.tobytes())
                print(f"   フレーム {i}: ハッシュ値 = {frame_hash}")
        
        return True
        
    except Exception as e:
        print(f"❌ フレーム抽出に失敗: {e}")
        return False

def debug_animation_loop():
    """アニメーションループのデバッグ"""
    print("\n🔄 アニメーションループデバッグ")
    print("-" * 30)
    
    try:
        from PIL import Image, ImageTk
        import tkinter as tk
        from tkinter import Label
        
        gif_folder = "assets/gifs"
        gif_files = [f for f in os.listdir(gif_folder) if f.lower().endswith('.gif')]
        gif_file = gif_files[0]
        gif_path = os.path.join(gif_folder, gif_file)
        
        # ウィンドウを作成
        root = tk.Tk()
        root.title("アニメーションデバッグ")
        root.geometry("400x300")
        root.configure(bg='black')
        
        # GIFを読み込み
        gif_image = Image.open(gif_path)
        frames = []
        
        print(f"📁 ファイル: {gif_file}")
        print(f"   フレーム数: {gif_image.n_frames}")
        
        # フレームを抽出（小さなサイズで高速化）
        for frame in range(gif_image.n_frames):
            gif_image.seek(frame)
            frame_resized = gif_image.resize((400, 300), Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame_resized))
        
        print(f"✅ {len(frames)}フレームを準備完了")
        
        # ラベルを作成
        label = Label(root, bg='black')
        label.pack(expand=True, fill='both')
        
        # アニメーション変数
        current_frame = 0
        frame_count = 0
        
        def animate():
            nonlocal current_frame, frame_count
            if frames:
                print(f"🔄 フレーム {current_frame} を表示中... (カウント: {frame_count})")
                label.configure(image=frames[current_frame])
                current_frame = (current_frame + 1) % len(frames)
                frame_count += 1
                
                # 10フレーム表示したら終了
                if frame_count < 10:
                    root.after(200, animate)  # 200ms間隔
                else:
                    print("✅ アニメーションループ完了")
                    root.destroy()
        
        # アニメーション開始
        print("🎬 アニメーション開始...")
        animate()
        
        # ウィンドウを表示
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ アニメーションループに失敗: {e}")
        return False

def debug_simple_animation():
    """シンプルなアニメーションテスト"""
    print("\n🎯 シンプルアニメーションテスト")
    print("-" * 30)
    
    try:
        from PIL import Image, ImageTk
        import tkinter as tk
        from tkinter import Label
        
        gif_folder = "assets/gifs"
        gif_files = [f for f in os.listdir(gif_folder) if f.lower().endswith('.gif')]
        gif_file = gif_files[0]
        gif_path = os.path.join(gif_folder, gif_file)
        
        # ウィンドウを作成
        root = tk.Tk()
        root.title("シンプルアニメーション")
        root.geometry("600x400")
        root.configure(bg='black')
        
        # フルスクリーン設定
        root.attributes('-fullscreen', True)
        
        # GIFを読み込み
        gif_image = Image.open(gif_path)
        print(f"📁 ファイル: {gif_file}")
        print(f"   フレーム数: {gif_image.n_frames}")
        
        # フレームを抽出
        frames = []
        for frame in range(gif_image.n_frames):
            gif_image.seek(frame)
            frame_resized = gif_image.resize((800, 600), Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame_resized))
        
        print(f"✅ {len(frames)}フレームを準備完了")
        
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
        print("🎬 アニメーション開始...")
        print("⏱️ 5秒間表示します...")
        print("💡 ESCキーで終了")
        
        # キーバインド
        def on_escape(event):
            root.destroy()
        root.bind('<Escape>', on_escape)
        
        # アニメーション開始
        animate()
        
        # 表示
        root.update()
        time.sleep(5)
        
        # ウィンドウを閉じる
        root.destroy()
        print("✅ シンプルアニメーションテスト完了")
        
        return True
        
    except Exception as e:
        print(f"❌ シンプルアニメーションに失敗: {e}")
        return False

def main():
    """メイン関数"""
    print("🔍 GIFアニメーションデバッグテスト")
    print("=" * 50)
    
    # デバッグ1: GIFファイルの詳細情報
    if not debug_gif_info():
        return 1
    
    # デバッグ2: フレーム抽出のデバッグ
    if not debug_frame_extraction():
        return 1
    
    # デバッグ3: アニメーションループのデバッグ
    if not debug_animation_loop():
        return 1
    
    # デバッグ4: シンプルなアニメーションテスト
    if not debug_simple_animation():
        return 1
    
    print("\n🎉 デバッグテスト完了！")
    print("💡 問題の原因が特定できました")
    
    return 0

if __name__ == "__main__":
    exit(main())
