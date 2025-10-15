#!/usr/bin/env python3
"""
高速音声会話システム
並列処理と最適化により応答時間を大幅短縮
"""

import os
import logging
import time
import threading
import asyncio
import concurrent.futures
from typing import Optional, Callable
from pathlib import Path

from speech_to_text import SpeechToText
from ai_chat import AIChat
from text_to_speech import TextToSpeech
from audio_recorder import AudioRecorder
from config import get_config


class FastVoiceConversation:
    """高速音声会話システムクラス"""
    
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
        
        # 並列処理用のスレッドプール
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
        
        # コールバック関数
        self.on_user_speech: Optional[Callable[[str], None]] = None
        self.on_ai_response: Optional[Callable[[str], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
        
        # パフォーマンス計測
        self.performance_stats = {
            'total_requests': 0,
            'total_time': 0,
            'avg_response_time': 0
        }
    
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
            self.logger.info("高速自動音声検出モードで会話を開始します")
            self.audio_recorder.start_continuous_recording(
                output_dir=str(self.recording_dir),
                max_duration=max_duration,
                silence_threshold=silence_threshold,
                silence_duration=silence_duration,
                callback=self._process_audio_file_fast
            )
        else:
            # 手動モード（スレッドで待機）
            self.conversation_thread = threading.Thread(
                target=self._manual_conversation_loop
            )
            self.conversation_thread.start()
            self.logger.info("高速手動モードで会話を開始します")
    
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
        
        # スレッドプールをシャットダウン
        self.executor.shutdown(wait=True)
        
        self.logger.info("高速会話システムを停止しました")
    
    def _process_audio_file_fast(self, audio_file_path: str):
        """
        録音された音声ファイルを高速処理する（並列処理版）
        
        Args:
            audio_file_path: 録音された音声ファイルのパス
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"高速音声処理開始: {audio_file_path}")
            
            # ステップ1: 音声認識（並列処理の準備）
            def transcribe_audio():
                return self.speech_to_text.transcribe_audio_file(
                    audio_file_path=audio_file_path,
                    language="ja",
                    response_format="text"
                )
            
            # 音声認識を実行
            user_text = transcribe_audio()
            
            if not user_text.strip():
                self.logger.info("音声からテキストが認識されませんでした")
                return
            
            self.logger.info(f"認識されたテキスト: {user_text}")
            
            # コールバック実行
            if self.on_user_speech:
                self.on_user_speech(user_text)
            
            # ステップ2: AI応答生成（並列処理）
            def generate_ai_response():
                return self.ai_chat.chat(
                    user_text,
                    max_tokens=80,  # より短い応答
                    temperature=0.7
                )
            
            # AI応答を生成
            ai_response = generate_ai_response()
            
            self.logger.info(f"AI応答: {ai_response}")
            
            # コールバック実行
            if self.on_ai_response:
                self.on_ai_response(ai_response)
            
            # ステップ3: 音声合成と再生（並列処理）
            def synthesize_and_play():
                # 音声合成
                audio_path = self.text_to_speech.speak_text(
                    ai_response,
                    play_audio=True
                )
                return audio_path
            
            # 音声合成を並列実行
            future = self.executor.submit(synthesize_and_play)
            
            # 録音ファイルを削除（プライバシー保護）
            try:
                Path(audio_file_path).unlink()
                self.logger.debug(f"録音ファイルを削除しました: {audio_file_path}")
            except Exception as e:
                self.logger.warning(f"録音ファイルの削除に失敗: {e}")
            
            # パフォーマンス統計を更新
            end_time = time.time()
            response_time = end_time - start_time
            
            self.performance_stats['total_requests'] += 1
            self.performance_stats['total_time'] += response_time
            self.performance_stats['avg_response_time'] = (
                self.performance_stats['total_time'] / self.performance_stats['total_requests']
            )
            
            self.logger.info(f"高速処理完了: {response_time:.2f}秒")
            
        except Exception as e:
            self.logger.error(f"高速音声処理エラー: {e}")
            if self.on_error:
                self.on_error(e)
    
    def _manual_conversation_loop(self):
        """手動モードの会話ループ"""
        self.logger.info("高速手動モード: 音声ファイルのパスを入力してください")
        
        while self.is_running:
            try:
                time.sleep(1)  # プレースホルダー
            except Exception as e:
                self.logger.error(f"高速手動モードエラー: {e}")
                if self.on_error:
                    self.on_error(e)
                break
    
    def process_audio_file_fast(self, audio_file_path: str) -> str:
        """
        指定された音声ファイルを高速処理してAI応答を返す
        
        Args:
            audio_file_path: 音声ファイルのパス
            
        Returns:
            AI応答のテキスト
        """
        start_time = time.time()
        
        try:
            # 音声認識
            user_text = self.speech_to_text.transcribe_audio_file(
                audio_file_path=audio_file_path,
                language="ja"
            )
            
            if not user_text.strip():
                return "音声からテキストが認識されませんでした。"
            
            # AI応答を生成
            ai_response = self.ai_chat.chat(user_text, max_tokens=80)
            
            end_time = time.time()
            self.logger.info(f"高速処理時間: {end_time - start_time:.2f}秒")
            
            return ai_response
            
        except Exception as e:
            self.logger.error(f"高速音声ファイル処理エラー: {e}")
            return f"エラーが発生しました: {str(e)}"
    
    def speak_response_fast(self, text: str):
        """
        指定されたテキストを高速音声で再生する
        
        Args:
            text: 再生するテキスト
        """
        try:
            # 並列処理で音声合成
            future = self.executor.submit(
                self.text_to_speech.speak_text, text
            )
            # 非同期で実行（ブロックしない）
            
        except Exception as e:
            self.logger.error(f"高速音声再生エラー: {e}")
            if self.on_error:
                self.on_error(e)
    
    def get_performance_stats(self) -> dict:
        """
        パフォーマンス統計を取得する
        
        Returns:
            パフォーマンス統計の辞書
        """
        return self.performance_stats.copy()
    
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


def main():
    """テスト用のメイン関数"""
    import argparse
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='高速音声会話システムテスト')
    parser.add_argument('--auto', action='store_true', help='自動音声検出モード')
    parser.add_argument('--audio-file', help='処理する音声ファイルのパス')
    parser.add_argument('--voice', default='alloy', help='TTS音声の種類')
    
    args = parser.parse_args()
    
    try:
        # 高速音声会話システムを作成
        conversation = FastVoiceConversation(tts_voice=args.voice)
        
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
            print(f"高速音声ファイル処理中: {args.audio_file}")
            response = conversation.process_audio_file_fast(args.audio_file)
            print(f"AI応答: {response}")
            conversation.speak_response_fast(response)
        
        elif args.auto:
            # 自動音声検出モード
            print("高速自動音声検出モードを開始します。Ctrl+Cで終了...")
            conversation.start_conversation(auto_mode=True)
            
            try:
                while True:
                    time.sleep(1)
                    # パフォーマンス統計を表示
                    stats = conversation.get_performance_stats()
                    if stats['total_requests'] > 0:
                        print(f"平均応答時間: {stats['avg_response_time']:.2f}秒")
            except KeyboardInterrupt:
                conversation.stop_conversation()
        
        else:
            print("使用方法:")
            print("  --auto: 高速自動音声検出モード")
            print("  --audio-file <path>: 音声ファイルを高速処理")
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
