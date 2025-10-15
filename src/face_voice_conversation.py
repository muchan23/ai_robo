#!/usr/bin/env python3
"""
顔表情付き音声会話システム
音声会話と表情表示を統合したシステム
"""

import os
import logging
import time
import threading
import pygame
from typing import Optional, Callable
from pathlib import Path

from voice_conversation import VoiceConversation
from face_display import FaceDisplay, Emotion


class FaceVoiceConversation:
    """顔表情付き音声会話システムクラス"""
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 chat_model: str = "gpt-4o-mini",
                 tts_voice: str = "alloy",
                 tts_model: str = "tts-1",
                 whisper_model: str = "whisper-1",
                 system_prompt: Optional[str] = None,
                 screen_width: int = 800,
                 screen_height: int = 600,
                 fullscreen: bool = False):
        """
        初期化
        
        Args:
            api_key: OpenAI APIキー
            chat_model: ChatGPTモデル
            tts_voice: TTS音声の種類
            tts_model: TTSモデル
            whisper_model: Whisperモデル
            system_prompt: AIのシステムプロンプト
            screen_width: 画面幅
            screen_height: 画面高さ
            fullscreen: フルスクリーンモード
        """
        self.logger = logging.getLogger(__name__)
        
        # 音声会話システムを初期化
        self.voice_conversation = VoiceConversation(
            api_key=api_key,
            chat_model=chat_model,
            tts_voice=tts_voice,
            tts_model=tts_model,
            whisper_model=whisper_model,
            system_prompt=system_prompt
        )
        
        # 顔表情表示システムを初期化
        self.face_display = FaceDisplay(
            screen_width=screen_width,
            screen_height=screen_height,
            fullscreen=fullscreen
        )
        
        # 状態管理
        self.is_running = False
        self.face_thread = None
        
        # コールバック関数を設定
        self.voice_conversation.on_user_speech = self._on_user_speech
        self.voice_conversation.on_ai_response = self._on_ai_response
        self.voice_conversation.on_error = self._on_error
        
        # コールバック関数
        self.on_user_speech: Optional[Callable[[str], None]] = None
        self.on_ai_response: Optional[Callable[[str], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
        
        self.logger.info("顔表情付き音声会話システムを初期化しました")
    
    def start_conversation(self, 
                          auto_mode: bool = True,
                          max_duration: float = 30.0,
                          silence_threshold: float = 0.01,
                          silence_duration: float = 2.0):
        """
        音声会話を開始する
        
        Args:
            auto_mode: 自動音声検出モードかどうか
            max_duration: 最大録音時間（秒）
            silence_threshold: 無音判定の閾値
            silence_duration: 無音継続時間（秒）
        """
        if self.is_running:
            self.logger.warning("既に会話システムが動作中です")
            return
        
        self.is_running = True
        
        # 顔表情表示を開始
        self.face_thread = threading.Thread(target=self._face_display_loop)
        self.face_thread.daemon = True
        self.face_thread.start()
        
        # 音声会話を開始
        self.voice_conversation.start_conversation(
            auto_mode=auto_mode,
            max_duration=max_duration,
            silence_threshold=silence_threshold,
            silence_duration=silence_duration
        )
        
        self.logger.info("顔表情付き音声会話システムを開始しました")
    
    def stop_conversation(self):
        """音声会話を停止する"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # 音声会話を停止
        self.voice_conversation.stop_conversation()
        
        # 顔表情表示を停止
        if self.face_thread:
            self.face_thread.join()
        
        self.logger.info("顔表情付き音声会話システムを停止しました")
    
    def _face_display_loop(self):
        """顔表情表示のメインループ"""
        try:
            # 初期状態を設定
            self.face_display.set_emotion(Emotion.NEUTRAL, animate=False)
            
            # メインループ
            clock = pygame.time.Clock()
            
            while self.is_running:
                # イベント処理
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.is_running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.is_running = False
                
                # 顔を描画
                self.face_display.draw_face()
                
                # FPS制限
                clock.tick(60)
                
        except Exception as e:
            self.logger.error(f"顔表情表示エラー: {e}")
        finally:
            pygame.quit()
    
    def _on_user_speech(self, text: str):
        """ユーザーの音声認識結果のコールバック"""
        self.logger.info(f"ユーザー発言: {text}")
        
        # 表情を「聞いている」状態に変更
        self.face_display.set_emotion(Emotion.LISTENING)
        
        # 外部コールバック実行
        if self.on_user_speech:
            self.on_user_speech(text)
    
    def _on_ai_response(self, text: str):
        """AI応答のコールバック"""
        self.logger.info(f"AI応答: {text}")
        
        # 応答内容に基づいて表情を決定
        emotion = self._analyze_emotion_from_text(text)
        self.face_display.set_emotion(emotion)
        
        # 外部コールバック実行
        if self.on_ai_response:
            self.on_ai_response(text)
    
    def _on_error(self, error: Exception):
        """エラーのコールバック"""
        self.logger.error(f"システムエラー: {error}")
        
        # エラー時は悲しい表情
        self.face_display.set_emotion(Emotion.SAD)
        
        # 外部コールバック実行
        if self.on_error:
            self.on_error(error)
    
    def _analyze_emotion_from_text(self, text: str) -> Emotion:
        """
        テキストから感情を分析する
        
        Args:
            text: 分析するテキスト
            
        Returns:
            分析された感情
        """
        text_lower = text.lower()
        
        # 喜びのキーワード
        happy_keywords = ['ありがとう', '嬉しい', '楽しい', '面白い', '素晴らしい', '最高', 'いい', '良い']
        if any(keyword in text_lower for keyword in happy_keywords):
            return Emotion.HAPPY
        
        # 悲しみのキーワード
        sad_keywords = ['悲しい', '残念', '申し訳ない', 'ごめん', 'すみません', '困った', '大変']
        if any(keyword in text_lower for keyword in sad_keywords):
            return Emotion.SAD
        
        # 驚きのキーワード
        surprised_keywords = ['驚いた', 'びっくり', 'すごい', '本当', 'まさか', '信じられない']
        if any(keyword in text_lower for keyword in surprised_keywords):
            return Emotion.SURPRISED
        
        # 怒りのキーワード
        angry_keywords = ['怒る', '腹立つ', 'イライラ', 'うるさい', 'やめて', 'だめ']
        if any(keyword in text_lower for keyword in angry_keywords):
            return Emotion.ANGRY
        
        # 思考のキーワード
        thinking_keywords = ['考え', '思う', 'どう', 'なぜ', 'なんで', '理由', '原因']
        if any(keyword in text_lower for keyword in thinking_keywords):
            return Emotion.THINKING
        
        # デフォルトは中性
        return Emotion.NEUTRAL
    
    def set_emotion(self, emotion: Emotion, animate: bool = True):
        """
        表情を手動で設定する
        
        Args:
            emotion: 設定する感情
            animate: アニメーションするかどうか
        """
        self.face_display.set_emotion(emotion, animate)
    
    def process_audio_file(self, audio_file_path: str) -> str:
        """
        指定された音声ファイルを処理してAI応答を返す
        
        Args:
            audio_file_path: 音声ファイルのパス
            
        Returns:
            AI応答のテキスト
        """
        # 聞いている表情に変更
        self.face_display.set_emotion(Emotion.LISTENING)
        
        # 音声処理
        response = self.voice_conversation.process_audio_file(audio_file_path)
        
        # 応答内容に基づいて表情を変更
        emotion = self._analyze_emotion_from_text(response)
        self.face_display.set_emotion(emotion)
        
        return response
    
    def speak_response(self, text: str):
        """
        指定されたテキストを音声で再生する
        
        Args:
            text: 再生するテキスト
        """
        # 話している表情に変更
        self.face_display.set_emotion(Emotion.SPEAKING)
        
        # 音声再生
        self.voice_conversation.speak_response(text)
        
        # 再生完了後は中性に戻す
        time.sleep(0.5)  # 少し待機
        self.face_display.set_emotion(Emotion.NEUTRAL)
    
    def reset_conversation(self):
        """会話履歴をリセットする"""
        self.voice_conversation.reset_conversation()
        self.face_display.set_emotion(Emotion.NEUTRAL)
        self.logger.info("会話履歴をリセットしました")
    
    def set_system_prompt(self, prompt: str):
        """
        システムプロンプトを変更する
        
        Args:
            prompt: 新しいシステムプロンプト
        """
        self.voice_conversation.set_system_prompt(prompt)
        self.logger.info("システムプロンプトを変更しました")
    
    def set_tts_voice(self, voice: str):
        """
        TTS音声を変更する
        
        Args:
            voice: 新しい音声の種類
        """
        self.voice_conversation.set_tts_voice(voice)
        self.logger.info(f"TTS音声を変更しました: {voice}")


def main():
    """テスト用のメイン関数"""
    import argparse
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='顔表情付き音声会話システムテスト')
    parser.add_argument('--auto', action='store_true', help='自動音声検出モード')
    parser.add_argument('--audio-file', help='処理する音声ファイルのパス')
    parser.add_argument('--voice', default='alloy', help='TTS音声の種類')
    parser.add_argument('--fullscreen', action='store_true', help='フルスクリーンモード')
    parser.add_argument('--width', type=int, default=800, help='画面幅')
    parser.add_argument('--height', type=int, default=600, help='画面高さ')
    
    args = parser.parse_args()
    
    try:
        # 顔表情付き音声会話システムを作成
        conversation = FaceVoiceConversation(
            tts_voice=args.voice,
            screen_width=args.width,
            screen_height=args.height,
            fullscreen=args.fullscreen
        )
        
        # コールバック関数を設定
        def on_user_speech(text):
            print(f"🎤 ユーザー: {text}")
        
        def on_ai_response(text):
            print(f"🤖 AI: {text}")
        
        def on_error(error):
            print(f"❌ エラー: {error}")
        
        conversation.on_user_speech = on_user_speech
        conversation.on_ai_response = on_ai_response
        conversation.on_error = on_error
        
        if args.audio_file:
            # 単発の音声ファイル処理
            print(f"音声ファイルを処理中: {args.audio_file}")
            response = conversation.process_audio_file(args.audio_file)
            print(f"AI応答: {response}")
            conversation.speak_response(response)
        
        elif args.auto:
            # 自動音声検出モード
            print("顔表情付き自動音声検出モードを開始します。Ctrl+Cで終了...")
            conversation.start_conversation(auto_mode=True)
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                conversation.stop_conversation()
        
        else:
            print("使用方法:")
            print("  --auto: 顔表情付き自動音声検出モード")
            print("  --audio-file <path>: 音声ファイルを処理")
            print("  --fullscreen: フルスクリーンモード")
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
