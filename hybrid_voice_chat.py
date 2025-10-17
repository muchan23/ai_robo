#!/usr/bin/env python3
"""
ハイブリッド音声会話システム - メインスクリプト
Whisper.cpp（ローカル音声認識）+ OpenAI（ChatGPT + TTS）
"""

import sys
import logging
import signal
import time
from pathlib import Path

# プロジェクトのsrcディレクトリをパスに追加
sys.path.append(str(Path(__file__).parent / 'src'))

from hybrid_voice_conversation import HybridVoiceConversation
from config import get_config


class HybridVoiceChatApp:
    """ハイブリッド音声会話アプリケーション"""
    
    def __init__(self):
        """初期化"""
        self.conversation = None
        self.is_running = False
        
        # ログ設定
        self._setup_logging()
        
        # シグナルハンドラーを設定
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logging(self):
        """ログ設定"""
        # 設定を読み込み
        config = get_config()
        config.setup_logging()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("ハイブリッド音声会話システムを初期化中...")
    
    def _signal_handler(self, signum, frame):
        """シグナルハンドラー（Ctrl+Cなど）"""
        self.logger.info(f"シグナル {signum} を受信しました。終了処理を開始...")
        self.stop()
    
    def start(self, auto_mode: bool = True, whisper_model_size: str = "small"):
        """
        ハイブリッド音声会話システムを開始する
        
        Args:
            auto_mode: 自動音声検出モードかどうか
            whisper_model_size: Whisper.cppモデルサイズ
        """
        try:
            # 設定の妥当性をチェック
            config = get_config()
            if not config.validate():
                self.logger.error("設定に問題があります。.envファイルを確認してください。")
                return False
            
            # ハイブリッド音声会話システムを作成
            self.conversation = HybridVoiceConversation(
                chat_model="gpt-4o-mini",
                tts_voice="alloy",
                tts_model="tts-1",
                whisper_model_size=whisper_model_size
            )
            
            # コールバック関数を設定
            self.conversation.on_user_speech = self._on_user_speech
            self.conversation.on_ai_response = self._on_ai_response
            self.conversation.on_error = self._on_error
            
            # 会話システムを開始
            self.conversation.start_conversation(auto_mode=auto_mode)
            self.is_running = True
            
            self.logger.info("ハイブリッド音声会話システムが開始されました")
            self._show_instructions()
            
            return True
            
        except Exception as e:
            self.logger.error(f"システム開始エラー: {e}")
            return False
    
    def stop(self):
        """ハイブリッド音声会話システムを停止する"""
        if self.conversation and self.is_running:
            self.logger.info("ハイブリッド音声会話システムを停止中...")
            self.conversation.stop_conversation()
            self.is_running = False
            self.logger.info("ハイブリッド音声会話システムが停止されました")
    
    def _on_user_speech(self, text: str):
        """ユーザーの音声認識結果のコールバック"""
        print(f"\n🎤 ユーザー: {text}")
    
    def _on_ai_response(self, text: str):
        """AI応答のコールバック"""
        print(f"🤖 AI: {text}")
    
    def _on_error(self, error: Exception):
        """エラーのコールバック"""
        print(f"❌ エラー: {error}")
        self.logger.error(f"システムエラー: {error}")
    
    def _show_instructions(self):
        """使用方法の説明を表示"""
        print("\n" + "="*60)
        print("🚀 ハイブリッド音声会話システム")
        print("="*60)
        print("🔧 システム構成:")
        print("• 音声認識: Whisper.cpp（ローカル・高速）")
        print("• AI対話: ChatGPT API（オンライン・高品質）")
        print("• 音声合成: OpenAI TTS API（オンライン・高品質）")
        print()
        print("✨ 特徴:")
        print("• 高速な音声認識（ファイル保存なし）")
        print("• 高品質なAI対話")
        print("• 自然な音声合成")
        print("• プライバシー保護（音声データはローカル処理）")
        print()
        print("📋 使用方法:")
        print("1. マイクに向かって話してください")
        print("2. 話し終わったら少し待ってください")
        print("3. AIが応答し、音声で返答します")
        print("4. Ctrl+C で終了します")
        print("="*60)
        print("準備完了！話しかけてください...\n")
    
    def run_interactive_mode(self, whisper_model_size: str = "small"):
        """対話モードで実行"""
        if not self.start(auto_mode=True, whisper_model_size=whisper_model_size):
            return 1
        
        try:
            # メインループ
            while self.is_running:
                time.sleep(1)
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
        
        return 0
    
    def run_file_mode(self, audio_file: str, whisper_model_size: str = "small"):
        """ファイルモードで実行"""
        if not self.start(auto_mode=False, whisper_model_size=whisper_model_size):
            return 1
        
        try:
            print(f"音声ファイルを処理中: {audio_file}")
            
            # 音声ファイルを処理
            response = self.conversation.process_audio_file(audio_file)
            print(f"AI応答: {response}")
            
            # 音声で再生
            self.conversation.speak_response(response)
            
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return 1
        finally:
            self.stop()
        
        return 0


def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='ハイブリッド音声会話システム（Whisper.cpp + OpenAI）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python hybrid_voice_chat.py                           # ハイブリッド自動音声検出モード
  python hybrid_voice_chat.py --file audio.wav          # 音声ファイル処理モード
  python hybrid_voice_chat.py --test                    # テストモード
  python hybrid_voice_chat.py --whisper-model small     # モデルサイズ指定
        """
    )
    
    parser.add_argument('--file', help='処理する音声ファイルのパス')
    parser.add_argument('--test', action='store_true', help='テストモード（設定確認）')
    parser.add_argument('--voice', default='alloy', help='TTS音声の種類')
    parser.add_argument('--model', default='gpt-4o-mini', help='ChatGPTモデル')
    parser.add_argument('--whisper-model', default='small', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper.cppモデルサイズ')
    
    args = parser.parse_args()
    
    # テストモード
    if args.test:
        print("=== ハイブリッドシステム設定テスト ===")
        try:
            config = get_config()
            config.setup_logging()
            
            if config.validate():
                print("✅ 設定は正常です")
                print(f"OpenAI APIキー: {'設定済み' if config.openai_api_key else '未設定'}")
                print(f"ChatGPTモデル: {args.model}")
                print(f"TTS音声: {args.voice}")
                print(f"Whisper.cppモデル: {args.whisper_model}")
                print("\n🚀 ハイブリッドシステム:")
                print("• 音声認識: Whisper.cpp（ローカル・高速）")
                print("• AI対話: ChatGPT API（オンライン・高品質）")
                print("• 音声合成: OpenAI TTS API（オンライン・高品質）")
                print("• ファイル保存: なし（高速化）")
                return 0
            else:
                print("❌ 設定に問題があります")
                return 1
                
        except Exception as e:
            print(f"❌ テストエラー: {e}")
            return 1
    
    # アプリケーションを作成・実行
    app = HybridVoiceChatApp()
    
    if args.file:
        # ファイルモード
        return app.run_file_mode(args.file, args.whisper_model)
    else:
        # 対話モード
        return app.run_interactive_mode(args.whisper_model)


if __name__ == "__main__":
    exit(main())
