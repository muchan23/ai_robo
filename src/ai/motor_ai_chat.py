#!/usr/bin/env python3
"""
モーター制御用AI対話システム
音声指示を解釈してモーター制御コマンドを生成
"""

import os
import json
import logging
from typing import Dict, Optional, Tuple
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

class MotorAIChat:
    """モーター制御用AI対話クラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = self._setup_logging()
        
        # OpenAI API設定
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEYが設定されていません。.envファイルを確認してください。")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # 対話設定
        self.model = os.getenv('CHAT_MODEL', 'gpt-4o-mini')
        
        # モーター制御用システムプロンプト
        self.system_prompt = """
あなたはロボットのモーター制御システムです。
ユーザーの音声指示を解釈して、具体的なモーター制御コマンドを生成してください。

制御可能な動作:
- 前進・後退・左回転・右回転
- 速度制御（0-100%）
- 時間制御（秒単位）

速度設定の指針:
- 前進・後退: 標準50%、高速80%、低速30%
- 回転: 標準85%、高速95%、低速70%（回転にはより高い速度が必要）
- 回転時間は通常0.8-1.0秒で短めに設定（素早い回転を実現）

応答形式（JSON）:
{
    "action": "move_forward|move_backward|turn_left|turn_right|stop",
    "speed": 0-100,
    "duration": 秒数（0.1-10.0）,
    "message": "実行する動作の説明"
}

例:
- "前に進んで" → {"action": "move_forward", "speed": 50, "duration": 2.0, "message": "前進します"}
- "右に回って" → {"action": "turn_right", "speed": 85, "duration": 1.0, "message": "右回転します"}
- "左に回って" → {"action": "turn_left", "speed": 85, "duration": 1.0, "message": "左回転します"}
- "速く右に回って" → {"action": "turn_right", "speed": 95, "duration": 0.8, "message": "高速右回転します"}
- "速く左に回って" → {"action": "turn_left", "speed": 95, "duration": 0.8, "message": "高速左回転します"}
- "止まって" → {"action": "stop", "speed": 0, "duration": 0, "message": "停止します"}

必ずJSON形式で応答してください。
"""
        
        self.logger.info("モーター制御用AI対話システムを初期化しました")
    
    def _setup_logging(self):
        """ログ設定"""
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def interpret_command(self, user_message: str) -> Dict:
        """
        ユーザーの音声指示を解釈してモーター制御コマンドを生成
        
        Args:
            user_message: ユーザーの音声指示
            
        Returns:
            モーター制御コマンドの辞書
        """
        self.logger.info(f"音声指示を解釈中: {user_message}")
        
        try:
            # OpenAI APIで応答を生成
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=200,
                temperature=0.3  # 低い温度で一貫性のある出力
            )
            
            # AI応答を取得
            ai_response = response.choices[0].message.content.strip()
            self.logger.info(f"AI応答: {ai_response}")
            
            # JSON形式でパース
            try:
                command = json.loads(ai_response)
                self.logger.info(f"解釈されたコマンド: {command}")
                return command
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON解析エラー: {e}")
                # デフォルトの停止コマンドを返す
                return {
                    "action": "stop",
                    "speed": 0,
                    "duration": 0,
                    "message": "コマンドを理解できませんでした"
                }
            
        except Exception as e:
            self.logger.error(f"AI解釈エラー: {e}")
            return {
                "action": "stop",
                "speed": 0,
                "duration": 0,
                "message": f"エラーが発生しました: {str(e)}"
            }
    
    def validate_command(self, command: Dict) -> bool:
        """
        コマンドの妥当性を検証
        
        Args:
            command: 検証するコマンド
            
        Returns:
            妥当性の真偽値
        """
        required_keys = ["action", "speed", "duration", "message"]
        
        # 必須キーの存在確認
        if not all(key in command for key in required_keys):
            self.logger.error("必須キーが不足しています")
            return False
        
        # アクションの妥当性確認
        valid_actions = ["move_forward", "move_backward", "turn_left", "turn_right", "stop"]
        if command["action"] not in valid_actions:
            self.logger.error(f"無効なアクション: {command['action']}")
            return False
        
        # 速度の妥当性確認
        if not (0 <= command["speed"] <= 100):
            self.logger.error(f"無効な速度: {command['speed']}")
            return False
        
        # 時間の妥当性確認
        if not (0 <= command["duration"] <= 10):
            self.logger.error(f"無効な時間: {command['duration']}")
            return False
        
        return True


def main():
    """テスト用のメイン関数"""
    print("🤖 モーター制御用AI対話システムテスト")
    print("=" * 50)
    
    try:
        # AI対話システムを初期化
        motor_ai = MotorAIChat()
        
        print("🎯 モーター制御AI対話を開始します")
        print("💡 音声指示を入力してください")
        print("⏹️  'quit' で終了")
        
        while True:
            try:
                # ユーザー入力
                user_input = input("\n👤 音声指示: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '終了']:
                    print("👋 対話を終了します")
                    break
                
                if not user_input:
                    continue
                
                # コマンドを解釈
                print("🤖 AI: 解釈中...")
                command = motor_ai.interpret_command(user_input)
                
                # コマンドの妥当性を検証
                if motor_ai.validate_command(command):
                    print(f"✅ 有効なコマンド: {command}")
                else:
                    print(f"❌ 無効なコマンド: {command}")
                
            except KeyboardInterrupt:
                print("\n🛑 終了します...")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")
                continue
        
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
