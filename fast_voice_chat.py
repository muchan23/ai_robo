#!/usr/bin/env python3
"""
高速音声会話システム - メインスクリプト
並列処理と最適化により応答時間を大幅短縮
"""

import sys
import logging
import signal
import time
from pathlib import Path

# プロジェクトのsrcディレクトリをパスに追加
sys.path.append(str(Path(__file__).parent / 'src'))

from fast_voice_conversation import FastVoiceConversation
from config import get_config


class FastVoiceChatApp:
    """高速音声会話アプリケーション"""
    
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
        self.logger.info("高速音声会話システムを初期化中...")
    
    def _signal_handler(self, signum, frame):
        """シグナルハンドラー（Ctrl+Cなど）"""
        self.logger.info(f"シグナル {signum} を受信しました。終了処理を開始...")
        self.stop()
    
    def start(self, auto_mode: bool = True):
        """
        高速音声会話システムを開始する
        
        Args:
            auto_mode: 自動音声検出モードかどうか
        """
        try:
            # 設定の妥当性をチェック
            config = get_config()
            if not config.validate():
                self.logger.error("設定に問題があります。.envファイルを確認してください。")
                return False
            
            # 高速音声会話システムを作成
            self.conversation = FastVoiceConversation(
                chat_model="gpt-4o-mini",
                tts_voice="alloy",
                tts_model="tts-1",
                whisper_model="whisper-1"
            )
            
            # コールバック関数を設定
            self.conversation.on_user_speech = self._on_user_speech
            self.conversation.on_ai_response = self._on_ai_response
            self.conversation.on_error = self._on_error
            
            # 会話システムを開始
            self.conversation.start_conversation(auto_mode=auto_mode)
            self.is_running = True
            
            self.logger.info("高速音声会話システムが開始されました")
            self._show_instructions()
            
            return True
            
        except Exception as e:
            self.logger.error(f"システム開始エラー: {e}")
            return False
    
    def stop(self):
        """高速音声会話システムを停止する"""
        if self.conversation and self.is_running:
            self.logger.info("高速音声会話システムを停止中...")
            self.conversation.stop_conversation()
            self.is_running = False
            self.logger.info("高速音声会話システムが停止されました")
    
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
        print("\n" + "="*50)
        print("🚀 高速音声会話システム")
        print("="*50)
        print("最適化機能:")
        print("• 並列処理による高速化")
        print("• 短縮されたAI応答")
        print("• 最適化された音声処理")
        print("• リアルタイムパフォーマンス監視")
        print()
        print("使用方法:")
        print("1. マイクに向かって話してください")
        print("2. 話し終わったら少し待ってください")
        print("3. AIが高速で応答を音声で返します")
        print("4. Ctrl+C で終了します")
        print("="*50)
        print("準備完了！話しかけてください...\n")
    
    def run_interactive_mode(self):
        """対話モードで実行"""
        if not self.start(auto_mode=True):
            return 1
        
        try:
            # メインループ（パフォーマンス監視付き）
            last_stats_time = time.time()
            
            while self.is_running:
                time.sleep(1)
                
                # 5秒ごとにパフォーマンス統計を表示
                current_time = time.time()
                if current_time - last_stats_time >= 5:
                    stats = self.conversation.get_performance_stats()
                    if stats['total_requests'] > 0:
                        print(f"📊 平均応答時間: {stats['avg_response_time']:.2f}秒 (処理回数: {stats['total_requests']})")
                    last_stats_time = current_time
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
            
            # 最終統計を表示
            stats = self.conversation.get_performance_stats()
            if stats['total_requests'] > 0:
                print(f"\n📈 最終統計:")
                print(f"   総処理回数: {stats['total_requests']}")
                print(f"   平均応答時間: {stats['avg_response_time']:.2f}秒")
                print(f"   総処理時間: {stats['total_time']:.2f}秒")
        
        return 0
    
    def run_file_mode(self, audio_file: str):
        """ファイルモードで実行"""
        if not self.start(auto_mode=False):
            return 1
        
        try:
            print(f"高速音声ファイル処理中: {audio_file}")
            
            # 音声ファイルを高速処理
            response = self.conversation.process_audio_file_fast(audio_file)
            print(f"AI応答: {response}")
            
            # 音声で再生
            self.conversation.speak_response_fast(response)
            
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
        description='高速ラズパイ音声会話システム',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python fast_voice_chat.py                    # 高速自動音声検出モード
  python fast_voice_chat.py --file audio.wav   # 高速音声ファイル処理モード
  python fast_voice_chat.py --test             # テストモード
        """
    )
    
    parser.add_argument('--file', help='処理する音声ファイルのパス')
    parser.add_argument('--test', action='store_true', help='テストモード（設定確認）')
    parser.add_argument('--voice', default='alloy', help='TTS音声の種類')
    parser.add_argument('--model', default='gpt-4o-mini', help='ChatGPTモデル')
    
    args = parser.parse_args()
    
    # テストモード
    if args.test:
        print("=== 高速システム設定テスト ===")
        try:
            config = get_config()
            config.setup_logging()
            
            if config.validate():
                print("✅ 設定は正常です")
                print(f"OpenAI APIキー: {'設定済み' if config.openai_api_key else '未設定'}")
                print(f"Whisperモデル: {config.whisper_model}")
                print(f"ChatGPTモデル: {config.chat_model}")
                print(f"TTS音声: {config.tts_voice}")
                print(f"デフォルト言語: {config.default_language}")
                print(f"サンプルレート: {config.sample_rate}")
                print("\n🚀 高速最適化設定:")
                print("• 並列処理: 有効")
                print("• 短縮応答: 有効")
                print("• パフォーマンス監視: 有効")
                return 0
            else:
                print("❌ 設定に問題があります")
                return 1
                
        except Exception as e:
            print(f"❌ テストエラー: {e}")
            return 1
    
    # アプリケーションを作成・実行
    app = FastVoiceChatApp()
    
    if args.file:
        # ファイルモード
        return app.run_file_mode(args.file)
    else:
        # 対話モード
        return app.run_interactive_mode()


if __name__ == "__main__":
    exit(main())
