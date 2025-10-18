#!/usr/bin/env python3
"""
GIF表示システム（簡易版）
スレッドエラーを回避した安全な実装
"""

import os
import sys
import time
import logging
import threading
from pathlib import Path
from tkinter import Tk, Label
from PIL import Image, ImageTk

class GIFPlayerSimple:
    """GIF表示クラス（簡易版）"""
    
    def __init__(self, gif_folder="assets/gifs"):
        """初期化"""
        self.logger = self._setup_logging()
        self.gif_folder = gif_folder
        self.root = None
        self.label = None
        self.current_gif = None
        self.is_playing = False
        self.frames = []
        self.current_frame = 0
        
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
        self.root.bind('<space>', self._toggle_gif)  # スペースキーでGIF表示切り替え
        self.root.bind('<h>', self._hide_gif)       # HキーでGIF非表示
        self.root.bind('<s>', self._show_gif)        # SキーでGIF表示
        
        self.logger.info("GIF表示ウィンドウを作成しました")
    
    def _on_escape(self, event):
        """ESCキーで終了"""
        self.stop()
    
    def _toggle_fullscreen(self, event):
        """F11キーでフルスクリーン切り替え"""
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
    
    def _toggle_gif(self, event):
        """スペースキーでGIF表示切り替え"""
        if self.is_playing:
            self._hide_gif(event)
        else:
            self._show_gif(event)
    
    def _hide_gif(self, event):
        """HキーでGIF非表示"""
        self.is_playing = False
        if self.label:
            self.label.configure(image='')
        print("🎬 GIF表示を停止しました")
    
    def _show_gif(self, event):
        """SキーでGIF表示"""
        if not self.is_playing:
            self.start_continuous_display()
        print("🎬 GIF表示を開始しました")
    
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
    
    def _animate_gif(self):
        """GIFアニメーションを実行（メインスレッドで実行）"""
        if self.is_playing and self.frames and self.label:
            try:
                # 現在のフレームを表示
                self.label.configure(image=self.frames[self.current_frame])
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                
                # 次のフレームをスケジュール
                if self.root:
                    self.root.after(100, self._animate_gif)
                    
            except Exception as e:
                self.logger.error(f"アニメーションエラー: {e}")
    
    def start_continuous_display(self, duration=100):
        """
        継続的にGIFを表示（音声対話中ずっと表示）
        
        Args:
            duration: フレーム間隔（ミリ秒）
        """
        if not self.gif_files:
            self.logger.warning("GIFファイルが見つかりません")
            return
        
        self.logger.info("継続的GIF表示を開始します")
        
        try:
            # ウィンドウを作成（まだ作成されていない場合）
            if self.root is None:
                self._create_window()
            
            # ランダムなGIFを選択
            import random
            gif_path = random.choice(self.gif_files)
            
            # GIFを読み込み
            self.frames = self._load_gif(gif_path)
            if not self.frames:
                return
            
            # アニメーションを開始
            self.is_playing = True
            self.current_frame = 0
            
            # ウィンドウを表示
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            
            # アニメーションを開始（メインスレッドで実行）
            self._animate_gif()
            
        except Exception as e:
            self.logger.error(f"継続的GIF表示エラー: {e}")
    
    def stop(self):
        """GIF再生を停止"""
        self.logger.info("GIF再生を停止します")
        self.is_playing = False
        
        if self.root:
            self.root.quit()
            self.root.destroy()
            self.root = None
    
    def cleanup(self):
        """リソースのクリーンアップ"""
        self.stop()
        self.logger.info("GIF表示システムをクリーンアップしました")


def main():
    """テスト用のメイン関数"""
    print("🎬 GIF表示システムテスト（簡易版）")
    print("=" * 50)
    
    try:
        # GIF表示システムを初期化
        gif_player = GIFPlayerSimple()
        
        if not gif_player.gif_files:
            print("❌ GIFファイルが見つかりません")
            print("💡 assets/gifsフォルダにGIFファイルを配置してください")
            return 1
        
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
        print(f"❌ エラー: {e}")
        return 1
    finally:
        if 'gif_player' in locals():
            gif_player.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
