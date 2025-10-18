#!/usr/bin/env python3
"""
GIF表示システム
音声対話中にGIFアニメーションを表示
"""

import os
import sys
import time
import threading
import logging
from pathlib import Path
from tkinter import Tk, Label, PhotoImage
from PIL import Image, ImageTk
import tkinter as tk

class GIFPlayer:
    """GIF表示クラス"""
    
    def __init__(self, gif_folder="assets/gifs"):
        """初期化"""
        self.logger = self._setup_logging()
        self.gif_folder = gif_folder
        self.root = None
        self.label = None
        self.current_gif = None
        self.is_playing = False
        self.animation_thread = None
        
        # GIFファイルのリストを取得
        self.gif_files = self._get_gif_files()
        
        self.logger.info(f"GIF表示システムを初期化しました（{len(self.gif_files)}個のGIF）")
    
    def _setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def _get_gif_files(self):
        """GIFファイルのリストを取得"""
        gif_files = []
        if os.path.exists(self.gif_folder):
            for file in os.listdir(self.gif_folder):
                if file.lower().endswith(('.gif', '.GIF')):
                    gif_files.append(os.path.join(self.gif_folder, file))
        else:
            # プロジェクトルートからGIFファイルを検索（フォールバック）
            for file in os.listdir('.'):
                if file.lower().endswith(('.gif', '.GIF')):
                    gif_files.append(file)
        
        self.logger.info(f"GIFファイルを発見: {gif_files}")
        return gif_files
    
    def _create_window(self):
        """ウィンドウを作成"""
        self.root = Tk()
        self.root.title("音声対話システム - GIF表示")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        # フルスクリーン設定
        self.root.attributes('-fullscreen', True)
        
        # ラベルを作成
        self.label = Label(self.root, bg='black')
        self.label.pack(expand=True, fill='both')
        
        # キーバインド
        self.root.bind('<Escape>', self._on_escape)
        self.root.bind('<F11>', self._toggle_fullscreen)
        
        self.logger.info("GIF表示ウィンドウを作成しました")
    
    def _on_escape(self, event):
        """ESCキーで終了"""
        self.stop()
    
    def _toggle_fullscreen(self, event):
        """F11キーでフルスクリーン切り替え"""
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
    
    def _load_gif(self, gif_path):
        """GIFファイルを読み込み"""
        try:
            # PILでGIFを読み込み
            gif = Image.open(gif_path)
            frames = []
            
            # フレームを抽出
            for frame in range(gif.n_frames):
                gif.seek(frame)
                # フレームをリサイズ（必要に応じて）
                frame_resized = gif.resize((800, 600), Image.Resampling.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame_resized))
            
            self.logger.info(f"GIFを読み込みました: {gif_path} ({len(frames)}フレーム)")
            return frames
            
        except Exception as e:
            self.logger.error(f"GIF読み込みエラー: {e}")
            return None
    
    def _animate_gif(self, frames, duration=100):
        """GIFアニメーションを実行"""
        try:
            frame_index = 0
            while self.is_playing and self.root:
                if frame_index < len(frames):
                    self.label.configure(image=frames[frame_index])
                    frame_index = (frame_index + 1) % len(frames)
                    time.sleep(duration / 1000.0)
                else:
                    frame_index = 0
        except Exception as e:
            self.logger.error(f"アニメーションエラー: {e}")
    
    def play_gif(self, gif_path=None, duration=100):
        """
        GIFを再生
        
        Args:
            gif_path: GIFファイルのパス（Noneの場合はランダム選択）
            duration: フレーム間隔（ミリ秒）
        """
        if not self.gif_files:
            self.logger.warning("GIFファイルが見つかりません")
            return
        
        # GIFファイルを選択
        if gif_path is None:
            import random
            gif_path = random.choice(self.gif_files)
        
        if not os.path.exists(gif_path):
            self.logger.error(f"GIFファイルが見つかりません: {gif_path}")
            return
        
        self.logger.info(f"GIF再生開始: {gif_path}")
        
        try:
            # ウィンドウを作成（まだ作成されていない場合）
            if self.root is None:
                self._create_window()
            
            # GIFを読み込み
            frames = self._load_gif(gif_path)
            if not frames:
                return
            
            # アニメーションを開始
            self.is_playing = True
            self.animation_thread = threading.Thread(
                target=self._animate_gif, 
                args=(frames, duration)
            )
            self.animation_thread.daemon = True
            self.animation_thread.start()
            
            # ウィンドウを表示
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            
        except Exception as e:
            self.logger.error(f"GIF再生エラー: {e}")
    
    def stop(self):
        """GIF再生を停止"""
        self.logger.info("GIF再生を停止します")
        self.is_playing = False
        
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(timeout=1.0)
        
        if self.root:
            self.root.quit()
            self.root.destroy()
            self.root = None
    
    def show_random_gif(self, duration=100):
        """ランダムなGIFを表示"""
        if self.gif_files:
            import random
            gif_path = random.choice(self.gif_files)
            self.play_gif(gif_path, duration)
    
    def cleanup(self):
        """リソースのクリーンアップ"""
        self.stop()
        self.logger.info("GIF表示システムをクリーンアップしました")


def main():
    """テスト用のメイン関数"""
    print("🎬 GIF表示システムテスト")
    print("=" * 50)
    
    try:
        # GIF表示システムを初期化
        gif_player = GIFPlayer()
        
        if not gif_player.gif_files:
            print("❌ GIFファイルが見つかりません")
            print("💡 gifsフォルダにGIFファイルを配置してください")
            return 1
        
        print(f"✅ {len(gif_player.gif_files)}個のGIFファイルを発見")
        print("🎯 GIF表示を開始します")
        print("💡 ESCキーで終了、F11キーでフルスクリーン切り替え")
        
        # ランダムなGIFを表示
        gif_player.show_random_gif()
        
        # ウィンドウのイベントループを開始
        if gif_player.root:
            gif_player.root.mainloop()
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return 1
    finally:
        if 'gif_player' in locals():
            gif_player.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
