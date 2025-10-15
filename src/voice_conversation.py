#!/usr/bin/env python3
"""
音声会話システム統合モジュール
音声認識→AI対話→音声合成の一連の流れを管理する
"""

import os
import logging
import time
import threading
from typing import Optional, Callable
from pathlib import Path

from .speech_to_text import SpeechToText
from .ai_chat import AIChat
from .text_to_speech import TextToSpeech
from .audio_recorder import AudioRecorder
from .config import get_config


class VoiceConversation:
    """音声会話システムクラス"""
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 chat_model: str = "gpt-4o-mini",
                 tts_voice: str = "alloy",
                 tts_model: str = "tts-1",
                 whisper_model: str = "whisper-1",
                 system_prompt: Optional[str] = None):
        """
        初期化
        
        Args:
            api_key: OpenAI APIキー
            chat_model: ChatGPTモデル
            tts_voice: TTS音声の種類
            tts_model: TTSモデル
            whisper_model: Whisperモデル
            system_prompt: AIのシステムプロンプト
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI APIキーが設定されていません")
        
        self.logger = logging.getLogger(__name__)
        
        # 各モジュールを初期化
        self.speech_to_text = SpeechToText(api_key=self.api_key)
        self.ai_chat = AIChat(
            api_key=self.api_key,
            model=chat_model,
            system_prompt=system_prompt
        )
        self.text_to_speech = TextToSpeech(
            api_key=self.api_key,
            voice=tts_voice,
            model=tts_model
        )
        
        # 設定を読み込み
        config = get_config()
        self.audio_recorder = AudioRecorder(
            sample_rate=config.sample_rate,
            chunk_size=config.chunk_size
        )
        
        # 状態管理
        self.is_running = False
        self.conversation_thread = None
        self.recording_dir = Path("recordings")
        self.recording_dir.mkdir(exist_ok=True)
        
        # コールバック関数
        self.on_user_speech: Optional[Callable[[str], None]] = None
        self.on_ai_response: Optional[Callable[[str], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
    
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
        
        if auto_mode:
            # 自動音声検出モード
            self.logger.info("自動音声検出モードで会話を開始します")
            self.audio_recorder.start_continuous_recording(
                output_dir=str(self.recording_dir),
                max_duration=max_duration,
                silence_threshold=silence_threshold,
                silence_duration=silence_duration,
                callback=self._process_audio_file
            )
        else:
            # 手動モード（スレッドで待機）
            self.conversation_thread = threading.Thread(
                target=self._manual_conversation_loop
            )
            self.conversation_thread.start()
            self.logger.info("手動モードで会話を開始します")
    
    def stop_conversation(self):
        """音声会話を停止する"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # 録音を停止
        self.audio_recorder.stop_continuous_recording()
        
        # スレッドの終了を待機
        if self.conversation_thread:
            self.conversation_thread.join()
        
        self.logger.info("会話システムを停止しました")
    
    def _process_audio_file(self, audio_file_path: str):
        """
        録音された音声ファイルを処理する
        
        Args:
            audio_file_path: 録音された音声ファイルのパス
        """
        try:
            self.logger.info(f"音声ファイルを処理中: {audio_file_path}")
            
            # 音声を文字起こし
            user_text = self.speech_to_text.transcribe_audio_file(
                audio_file_path=audio_file_path,
                language="ja"  # 日本語を指定
            )
            
            if not user_text.strip():
                self.logger.info("音声からテキストが認識されませんでした")
                return
            
            self.logger.info(f"認識されたテキスト: {user_text}")
            
            # コールバック実行
            if self.on_user_speech:
                self.on_user_speech(user_text)
            
            # AI応答を生成
            ai_response = self.ai_chat.chat(user_text)
            
            self.logger.info(f"AI応答: {ai_response}")
            
            # コールバック実行
            if self.on_ai_response:
                self.on_ai_response(ai_response)
            
            # 音声合成して再生
            self.text_to_speech.speak_text(ai_response)
            
            # 録音ファイルを削除（プライバシー保護）
            try:
                Path(audio_file_path).unlink()
                self.logger.debug(f"録音ファイルを削除しました: {audio_file_path}")
            except Exception as e:
                self.logger.warning(f"録音ファイルの削除に失敗: {e}")
            
        except Exception as e:
            self.logger.error(f"音声処理エラー: {e}")
            if self.on_error:
                self.on_error(e)
    
    def _manual_conversation_loop(self):
        """手動モードの会話ループ"""
        self.logger.info("手動モード: 音声ファイルのパスを入力してください")
        
        while self.is_running:
            try:
                # ユーザー入力を待機（実際の実装では適切な入力方法を使用）
                time.sleep(1)  # プレースホルダー
                
                # ここで実際の入力処理を実装
                # 例: ファイルパス入力、ボタン押下検出など
                
            except Exception as e:
                self.logger.error(f"手動モードエラー: {e}")
                if self.on_error:
                    self.on_error(e)
                break
    
    def process_audio_file(self, audio_file_path: str) -> str:
        """
        指定された音声ファイルを処理してAI応答を返す
        
        Args:
            audio_file_path: 音声ファイルのパス
            
        Returns:
            AI応答のテキスト
        """
        try:
            # 音声を文字起こし
            user_text = self.speech_to_text.transcribe_audio_file(
                audio_file_path=audio_file_path,
                language="ja"
            )
            
            if not user_text.strip():
                return "音声からテキストが認識されませんでした。"
            
            # AI応答を生成
            ai_response = self.ai_chat.chat(user_text)
            
            return ai_response
            
        except Exception as e:
            self.logger.error(f"音声ファイル処理エラー: {e}")
            return f"エラーが発生しました: {str(e)}"
    
    def speak_response(self, text: str):
        """
        指定されたテキストを音声で再生する
        
        Args:
            text: 再生するテキスト
        """
        try:
            self.text_to_speech.speak_text(text)
        except Exception as e:
            self.logger.error(f"音声再生エラー: {e}")
            if self.on_error:
                self.on_error(e)
    
    def reset_conversation(self):
        """会話履歴をリセットする"""
        self.ai_chat.reset_conversation()
        self.logger.info("会話履歴をリセットしました")
    
    def set_system_prompt(self, prompt: str):
        """
        システムプロンプトを変更する
        
        Args:
            prompt: 新しいシステムプロンプト
        """
        self.ai_chat.set_system_prompt(prompt)
        self.logger.info("システムプロンプトを変更しました")
    
    def set_tts_voice(self, voice: str):
        """
        TTS音声を変更する
        
        Args:
            voice: 新しい音声の種類
        """
        self.text_to_speech.set_voice(voice)
        self.logger.info(f"TTS音声を変更しました: {voice}")
    
    def save_conversation(self, file_path: str):
        """
        会話履歴を保存する
        
        Args:
            file_path: 保存先ファイルパス
        """
        self.ai_chat.save_conversation(file_path)
    
    def load_conversation(self, file_path: str):
        """
        会話履歴を読み込む
        
        Args:
            file_path: 読み込み元ファイルパス
        """
        self.ai_chat.load_conversation(file_path)


def main():
    """テスト用のメイン関数"""
    import argparse
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='音声会話システムテスト')
    parser.add_argument('--auto', action='store_true', help='自動音声検出モード')
    parser.add_argument('--audio-file', help='処理する音声ファイルのパス')
    parser.add_argument('--voice', default='alloy', help='TTS音声の種類')
    
    args = parser.parse_args()
    
    try:
        # 音声会話システムを作成
        conversation = VoiceConversation(tts_voice=args.voice)
        
        # コールバック関数を設定
        def on_user_speech(text):
            print(f"ユーザー: {text}")
        
        def on_ai_response(text):
            print(f"AI: {text}")
        
        def on_error(error):
            print(f"エラー: {error}")
        
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
            print("自動音声検出モードを開始します。Ctrl+Cで終了...")
            conversation.start_conversation(auto_mode=True)
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                conversation.stop_conversation()
        
        else:
            print("使用方法:")
            print("  --auto: 自動音声検出モード")
            print("  --audio-file <path>: 音声ファイルを処理")
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
