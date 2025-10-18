#!/usr/bin/env python3
"""
音声合成システム
OpenAI TTS APIを使用した音声合成機能
"""

import os
import logging
import tempfile
import pygame
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

class TTSSynthesis:
    """音声合成クラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = self._setup_logging()
        
        # OpenAI API設定
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEYが設定されていません。.envファイルを確認してください。")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # TTS設定
        self.voice = os.getenv('TTS_VOICE', 'alloy')
        self.model = os.getenv('TTS_MODEL', 'tts-1')
        self.speed = float(os.getenv('TTS_SPEED', '1.0'))
        
        # 音声再生用
        pygame.mixer.init()
        
        self.logger.info("音声合成システムを初期化しました")
    
    def _setup_logging(self):
        """ログ設定"""
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def synthesize_speech(self, text: str) -> str:
        """
        テキストを音声に合成
        
        Args:
            text: 音声合成するテキスト
            
        Returns:
            音声ファイルのパス
        """
        self.logger.info(f"音声合成開始: {text[:50]}...")
        
        try:
            # OpenAI TTS APIで音声合成
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text,
                speed=self.speed
            )
            
            # 一時ファイルに保存
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_file.write(response.content)
                audio_file_path = temp_file.name
            
            self.logger.info(f"音声合成完了: {audio_file_path}")
            return audio_file_path
            
        except Exception as e:
            self.logger.error(f"音声合成エラー: {e}")
            raise
    
    def play_audio(self, audio_file_path: str):
        """
        音声ファイルを再生
        
        Args:
            audio_file_path: 音声ファイルのパス
        """
        self.logger.info(f"音声再生開始: {audio_file_path}")
        
        try:
            # 音声ファイルを再生
            pygame.mixer.music.load(audio_file_path)
            pygame.mixer.music.play()
            
            # 再生完了まで待機
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            self.logger.info("音声再生完了")
            
        except Exception as e:
            self.logger.error(f"音声再生エラー: {e}")
            raise
    
    def speak_text(self, text: str):
        """
        テキストを音声合成して再生
        
        Args:
            text: 音声合成するテキスト
        """
        try:
            # 音声合成
            audio_file_path = self.synthesize_speech(text)
            
            # 音声再生
            self.play_audio(audio_file_path)
            
            # 一時ファイルを削除
            os.unlink(audio_file_path)
            
        except Exception as e:
            self.logger.error(f"音声合成・再生エラー: {e}")
            raise
    
    def set_voice(self, voice: str):
        """
        音声を変更
        
        Args:
            voice: 音声の種類 (alloy, echo, fable, onyx, nova, shimmer)
        """
        if voice in ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']:
            self.voice = voice
            self.logger.info(f"音声を変更しました: {voice}")
        else:
            self.logger.warning(f"無効な音声: {voice}")
    
    def set_speed(self, speed: float):
        """
        音声速度を変更
        
        Args:
            speed: 音声速度 (0.25 - 4.0)
        """
        if 0.25 <= speed <= 4.0:
            self.speed = speed
            self.logger.info(f"音声速度を変更しました: {speed}")
        else:
            self.logger.warning(f"無効な音声速度: {speed}")
    
    def cleanup(self):
        """リソースのクリーンアップ"""
        pygame.mixer.quit()
        self.logger.info("音声合成システムをクリーンアップしました")


def main():
    """テスト用のメイン関数"""
    print("🔊 音声合成システムテスト")
    print("=" * 50)
    
    try:
        # 音声合成システムを初期化
        tts = TTSSynthesis()
        
        print("🎯 音声合成を開始します")
        print("💡 テキストを入力してください")
        print("⏹️  'quit' で終了")
        
        while True:
            try:
                # ユーザー入力
                user_input = input("\n📝 テキスト: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '終了']:
                    print("👋 音声合成を終了します")
                    break
                
                if not user_input:
                    continue
                
                # 音声合成・再生
                print("🔊 音声合成中...")
                tts.speak_text(user_input)
                print("✅ 音声再生完了")
                
            except KeyboardInterrupt:
                print("\n🛑 終了します...")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")
                continue
        
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return 1
    finally:
        if 'tts' in locals():
            tts.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
