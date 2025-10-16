#!/usr/bin/env python3
"""
顔表情表示システム
モニターに表情を表示するための基本システム
"""

import pygame
import logging
import time
import threading
from typing import Dict, Optional, Tuple
from enum import Enum
from pathlib import Path


class Emotion(Enum):
    """感情の種類"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    SURPRISED = "surprised"
    THINKING = "thinking"
    LISTENING = "listening"
    SPEAKING = "speaking"


class FaceDisplay:
    """顔表情表示クラス"""
    
    def __init__(self, 
                 screen_width: int = 800,
                 screen_height: int = 600,
                 fullscreen: bool = False):
        """
        初期化
        
        Args:
            screen_width: 画面幅
            screen_height: 画面高さ
            fullscreen: フルスクリーンモード
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fullscreen = fullscreen
        
        self.logger = logging.getLogger(__name__)
        
        # pygame初期化
        self.display_available = False
        try:
            pygame.init()
            
            # ディスプレイの可用性をチェック
            if not pygame.display.get_init():
                raise pygame.error("Display not initialized")
            
            # 画面設定
            if fullscreen:
                self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((screen_width, screen_height))
            
            pygame.display.set_caption("AI Robot Face")
            self.display_available = True
            self.logger.info("ディスプレイ初期化成功")
            
        except (pygame.error, Exception) as e:
            self.logger.error(f"ディスプレイ初期化エラー: {e}")
            print(f"ディスプレイ初期化エラー: {e}")
            print("ヘッドレスモードで動作します（表情表示なし）")
            self.display_available = False
            self.screen = None
        
        # 色定義
        self.colors = {
            'background': (240, 240, 240),
            'face': (255, 220, 177),
            'eye': (255, 255, 255),
            'pupil': (0, 0, 0),
            'mouth': (200, 100, 100),
            'eyebrow': (139, 69, 19)
        }
        
        # 現在の感情状態
        self.current_emotion = Emotion.NEUTRAL
        self.is_animating = False
        self.animation_thread = None
        
        # 表情パラメータ
        self.face_params = self._get_emotion_params(Emotion.NEUTRAL)
        
        # アニメーション用
        self.animation_start_time = 0
        self.animation_duration = 0.5  # 秒
        
        self.logger.info("顔表情表示システムを初期化しました")
    
    def _get_emotion_params(self, emotion: Emotion) -> Dict:
        """
        感情に応じた顔のパラメータを取得
        
        Args:
            emotion: 感情の種類
            
        Returns:
            顔のパラメータ辞書
        """
        params = {
            Emotion.NEUTRAL: {
                'eye_open': 0.8,
                'eyebrow_angle': 0,
                'mouth_curve': 0,
                'mouth_open': 0.1,
                'eye_size': 1.0,
                'face_color': self.colors['face']
            },
            Emotion.HAPPY: {
                'eye_open': 0.6,
                'eyebrow_angle': 0,
                'mouth_curve': 0.3,
                'mouth_open': 0.2,
                'eye_size': 1.0,
                'face_color': self.colors['face']
            },
            Emotion.SAD: {
                'eye_open': 0.7,
                'eyebrow_angle': -0.2,
                'mouth_curve': -0.3,
                'mouth_open': 0.1,
                'eye_size': 0.9,
                'face_color': (240, 200, 160)
            },
            Emotion.ANGRY: {
                'eye_open': 0.9,
                'eyebrow_angle': -0.3,
                'mouth_curve': -0.1,
                'mouth_open': 0.3,
                'eye_size': 1.1,
                'face_color': (255, 200, 160)
            },
            Emotion.SURPRISED: {
                'eye_open': 1.0,
                'eyebrow_angle': 0.3,
                'mouth_curve': 0,
                'mouth_open': 0.4,
                'eye_size': 1.2,
                'face_color': self.colors['face']
            },
            Emotion.THINKING: {
                'eye_open': 0.5,
                'eyebrow_angle': 0.1,
                'mouth_curve': 0,
                'mouth_open': 0.05,
                'eye_size': 0.8,
                'face_color': (250, 210, 180)
            },
            Emotion.LISTENING: {
                'eye_open': 0.8,
                'eyebrow_angle': 0.1,
                'mouth_curve': 0,
                'mouth_open': 0.1,
                'eye_size': 1.0,
                'face_color': self.colors['face']
            },
            Emotion.SPEAKING: {
                'eye_open': 0.7,
                'eyebrow_angle': 0,
                'mouth_curve': 0.1,
                'mouth_open': 0.3,
                'eye_size': 1.0,
                'face_color': self.colors['face']
            }
        }
        
        return params.get(emotion, params[Emotion.NEUTRAL])
    
    def set_emotion(self, emotion: Emotion, animate: bool = True):
        """
        感情を設定する
        
        Args:
            emotion: 設定する感情
            animate: アニメーションするかどうか
        """
        if emotion == self.current_emotion:
            return
        
        self.logger.info(f"感情を変更: {self.current_emotion.value} → {emotion.value}")
        
        if animate:
            self._animate_emotion_change(emotion)
        else:
            self.current_emotion = emotion
            self.face_params = self._get_emotion_params(emotion)
    
    def _animate_emotion_change(self, target_emotion: Emotion):
        """
        感情変化のアニメーション
        
        Args:
            target_emotion: 目標の感情
        """
        if self.is_animating:
            return
        
        self.is_animating = True
        self.animation_start_time = time.time()
        
        # アニメーションスレッドを開始
        self.animation_thread = threading.Thread(
            target=self._animation_worker,
            args=(target_emotion,)
        )
        self.animation_thread.daemon = True
        self.animation_thread.start()
    
    def _animation_worker(self, target_emotion: Emotion):
        """
        アニメーションワーカースレッド
        
        Args:
            target_emotion: 目標の感情
        """
        start_params = self._get_emotion_params(self.current_emotion)
        target_params = self._get_emotion_params(target_emotion)
        
        while self.is_animating:
            current_time = time.time()
            elapsed = current_time - self.animation_start_time
            
            if elapsed >= self.animation_duration:
                # アニメーション完了
                self.current_emotion = target_emotion
                self.face_params = target_params
                self.is_animating = False
                break
            
            # 補間計算
            progress = elapsed / self.animation_duration
            progress = min(progress, 1.0)
            
            # イージング関数（ease-in-out）
            ease_progress = 0.5 * (1 + (2 * progress - 1) ** 3)
            
            # パラメータを補間
            self.face_params = {}
            for key in start_params:
                start_val = start_params[key]
                target_val = target_params[key]
                
                if isinstance(start_val, (int, float)):
                    self.face_params[key] = start_val + (target_val - start_val) * ease_progress
                else:
                    self.face_params[key] = target_val
            
            time.sleep(0.016)  # 60FPS
    
    def draw_face(self):
        """顔を描画する"""
        if not self.display_available or self.screen is None:
            return
        
        try:
            # 背景をクリア
            self.screen.fill(self.colors['background'])
            
            # 顔の中心座標
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2
            
            # 顔の描画
            self._draw_face_outline(center_x, center_y)
            
            # 目を描画
            self._draw_eyes(center_x, center_y)
            
            # 眉毛を描画
            self._draw_eyebrows(center_x, center_y)
            
            # 口を描画
            self._draw_mouth(center_x, center_y)
            
            # 画面を更新
            pygame.display.flip()
            
        except (pygame.error, Exception) as e:
            self.logger.error(f"描画エラー: {e}")
            self.display_available = False
    
    def _draw_face_outline(self, center_x: int, center_y: int):
        """顔の輪郭を描画"""
        face_radius = min(self.screen_width, self.screen_height) // 4
        
        pygame.draw.circle(
            self.screen,
            self.face_params['face_color'],
            (center_x, center_y),
            face_radius
        )
    
    def _draw_eyes(self, center_x: int, center_y: int):
        """目を描画"""
        eye_y = center_y - 50
        eye_spacing = 80
        
        # 左目
        left_eye_x = center_x - eye_spacing // 2
        self._draw_eye(left_eye_x, eye_y)
        
        # 右目
        right_eye_x = center_x + eye_spacing // 2
        self._draw_eye(right_eye_x, eye_y)
    
    def _draw_eye(self, x: int, y: int):
        """単一の目を描画"""
        eye_size = int(30 * self.face_params['eye_size'])
        eye_open = self.face_params['eye_open']
        
        # 目の白い部分
        pygame.draw.ellipse(
            self.screen,
            self.colors['eye'],
            (x - eye_size // 2, y - eye_size // 2, eye_size, int(eye_size * eye_open))
        )
        
        # 瞳孔
        pupil_size = int(eye_size * 0.3)
        pupil_y = y - pupil_size // 2
        
        pygame.draw.circle(
            self.screen,
            self.colors['pupil'],
            (x, pupil_y),
            pupil_size // 2
        )
    
    def _draw_eyebrows(self, center_x: int, center_y: int):
        """眉毛を描画"""
        eyebrow_y = center_y - 100
        eyebrow_spacing = 80
        eyebrow_angle = self.face_params['eyebrow_angle']
        
        # 左眉毛
        left_eyebrow_x = center_x - eyebrow_spacing // 2
        self._draw_eyebrow(left_eyebrow_x, eyebrow_y, eyebrow_angle)
        
        # 右眉毛
        right_eyebrow_x = center_x + eyebrow_spacing // 2
        self._draw_eyebrow(right_eyebrow_x, eyebrow_y, -eyebrow_angle)
    
    def _draw_eyebrow(self, x: int, y: int, angle: float):
        """単一の眉毛を描画"""
        eyebrow_length = 40
        eyebrow_thickness = 4
        
        # 角度に応じて眉毛の位置を調整
        offset_y = int(angle * 20)
        
        pygame.draw.line(
            self.screen,
            self.colors['eyebrow'],
            (x - eyebrow_length // 2, y + offset_y),
            (x + eyebrow_length // 2, y + offset_y),
            eyebrow_thickness
        )
    
    def _draw_mouth(self, center_x: int, center_y: int):
        """口を描画"""
        mouth_y = center_y + 50
        mouth_curve = self.face_params['mouth_curve']
        mouth_open = self.face_params['mouth_open']
        
        mouth_width = 60
        mouth_height = int(20 * (1 + mouth_open))
        
        # 口の形状を計算
        if mouth_curve > 0:
            # 笑顔
            pygame.draw.arc(
                self.screen,
                self.colors['mouth'],
                (center_x - mouth_width // 2, mouth_y - mouth_height // 2, 
                 mouth_width, mouth_height),
                0, 3.14159,
                4
            )
        elif mouth_curve < 0:
            # 悲しい顔
            pygame.draw.arc(
                self.screen,
                self.colors['mouth'],
                (center_x - mouth_width // 2, mouth_y - mouth_height // 2, 
                 mouth_width, mouth_height),
                3.14159, 6.28318,
                4
            )
        else:
            # 中性
            pygame.draw.ellipse(
                self.screen,
                self.colors['mouth'],
                (center_x - mouth_width // 2, mouth_y - mouth_height // 2, 
                 mouth_width, mouth_height)
            )
    
    def run(self):
        """メインループを実行"""
        clock = pygame.time.Clock()
        running = True
        
        self.logger.info("顔表情表示システムを開始しました")
        
        while running:
            if self.display_available:
                try:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running = False
                            elif event.key == pygame.K_1:
                                self.set_emotion(Emotion.HAPPY)
                            elif event.key == pygame.K_2:
                                self.set_emotion(Emotion.SAD)
                            elif event.key == pygame.K_3:
                                self.set_emotion(Emotion.ANGRY)
                            elif event.key == pygame.K_4:
                                self.set_emotion(Emotion.SURPRISED)
                            elif event.key == pygame.K_0:
                                self.set_emotion(Emotion.NEUTRAL)
                    
                    # 顔を描画
                    self.draw_face()
                except (pygame.error, Exception) as e:
                    self.logger.error(f"イベント処理エラー: {e}")
                    self.display_available = False
            else:
                # ヘッドレスモードでは短時間待機
                time.sleep(0.1)
            
            # FPS制限
            clock.tick(60)
        
        pygame.quit()
        self.logger.info("顔表情表示システムを終了しました")


def main():
    """テスト用のメイン関数"""
    import argparse
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='顔表情表示システムテスト')
    parser.add_argument('--fullscreen', action='store_true', help='フルスクリーンモード')
    parser.add_argument('--width', type=int, default=800, help='画面幅')
    parser.add_argument('--height', type=int, default=600, help='画面高さ')
    
    args = parser.parse_args()
    
    try:
        # 顔表情表示システムを作成
        face_display = FaceDisplay(
            screen_width=args.width,
            screen_height=args.height,
            fullscreen=args.fullscreen
        )
        
        print("顔表情表示システム")
        print("キー操作:")
        print("  0: 中性")
        print("  1: 喜び")
        print("  2: 悲しみ")
        print("  3: 怒り")
        print("  4: 驚き")
        print("  ESC: 終了")
        
        # メインループを実行
        face_display.run()
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
