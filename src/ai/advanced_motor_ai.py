#!/usr/bin/env python3
"""
高度なモーター制御AIシステム
複数ステップの指示を解析し、LLMが柔軟にモーター制御計画を生成
"""

import os
import json
import logging
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

class AdvancedMotorAI:
    """高度なモーター制御AIクラス"""
    
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
        
        # 高度なモーター制御用システムプロンプト
        self.system_prompt = """
あなたは高度なロボット制御システムです。
ユーザーの複雑な音声指示を解析し、段階的なモーター制御計画を生成してください。

## 制御可能な基本動作
- **前進**: move_forward (速度: 30-100%, 時間: 0.5-5.0秒)
- **後退**: move_backward (速度: 30-100%, 時間: 0.5-5.0秒)
- **左回転**: turn_left (速度: 70-95%, 時間: 0.8-2.0秒)
- **右回転**: turn_right (速度: 70-95%, 時間: 0.8-2.0秒)
- **停止**: stop (速度: 0%, 時間: 0秒)
- **待機**: wait (時間: 0.5-3.0秒)

## 複雑な指示の例
- "まっすぐ行って、右に曲がって" → [前進, 右回転]
- "左に回って、前に進んで、止まって" → [左回転, 前進, 停止]
- "後ろに下がって、左に回って、前に進んで" → [後退, 左回転, 前進]
- "右に回って、速く前に進んで、左に回って" → [右回転, 高速前進, 左回転]

## 応答形式（JSON）
{
    "plan": [
        {
            "step": 1,
            "action": "move_forward|move_backward|turn_left|turn_right|stop|wait",
            "speed": 0-100,
            "duration": 秒数（0.1-10.0）,
            "description": "このステップの説明"
        }
    ],
    "total_steps": ステップ数,
    "estimated_time": 総実行時間（秒）,
    "summary": "実行計画の概要"
}

## 速度設定の指針
- 前進・後退: 標準50%、高速80%、低速30%
- 回転: 標準85%、高速95%、低速70%
- 待機: 0.5-3.0秒で適切な間隔を設定

必ずJSON形式で応答し、複数ステップの計画を生成してください。
"""
        
        self.logger.info("高度なモーター制御AIシステムを初期化しました")
    
    def _setup_logging(self):
        """ログ設定"""
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def analyze_complex_command(self, user_message: str) -> Dict:
        """
        複雑な音声指示を解析して段階的なモーター制御計画を生成
        
        Args:
            user_message: ユーザーの音声指示
            
        Returns:
            モーター制御計画の辞書
        """
        self.logger.info(f"複雑な指示を解析中: {user_message}")
        
        try:
            # OpenAI APIで応答を生成
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.3  # 低い温度で一貫性のある出力
            )
            
            # AI応答を取得
            ai_response = response.choices[0].message.content.strip()
            self.logger.info(f"AI応答: {ai_response}")
            
            # JSON形式でパース
            try:
                plan = json.loads(ai_response)
                self.logger.info(f"生成された計画: {plan}")
                return plan
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON解析エラー: {e}")
                # デフォルトの停止計画を返す
                return {
                    "plan": [{
                        "step": 1,
                        "action": "stop",
                        "speed": 0,
                        "duration": 0,
                        "description": "コマンドを理解できませんでした"
                    }],
                    "total_steps": 1,
                    "estimated_time": 0,
                    "summary": "エラー: コマンドを理解できませんでした"
                }
            
        except Exception as e:
            self.logger.error(f"AI解析エラー: {e}")
            return {
                "plan": [{
                    "step": 1,
                    "action": "stop",
                    "speed": 0,
                    "duration": 0,
                    "description": f"エラーが発生しました: {str(e)}"
                }],
                "total_steps": 1,
                "estimated_time": 0,
                "summary": f"エラー: {str(e)}"
            }
    
    def validate_plan(self, plan: Dict) -> bool:
        """
        生成された計画の妥当性を検証
        
        Args:
            plan: 検証する計画
            
        Returns:
            妥当性の真偽値
        """
        required_keys = ["plan", "total_steps", "estimated_time", "summary"]
        
        # 必須キーの存在確認
        if not all(key in plan for key in required_keys):
            self.logger.error("必須キーが不足しています")
            return False
        
        # 計画の妥当性確認
        if not isinstance(plan["plan"], list) or len(plan["plan"]) == 0:
            self.logger.error("計画が空です")
            return False
        
        # 各ステップの妥当性確認
        valid_actions = ["move_forward", "move_backward", "turn_left", "turn_right", "stop", "wait"]
        
        for step in plan["plan"]:
            if not isinstance(step, dict):
                self.logger.error("ステップが辞書形式ではありません")
                return False
            
            required_step_keys = ["step", "action", "speed", "duration", "description"]
            if not all(key in step for key in required_step_keys):
                self.logger.error("ステップの必須キーが不足しています")
                return False
            
            if step["action"] not in valid_actions:
                self.logger.error(f"無効なアクション: {step['action']}")
                return False
            
            if not (0 <= step["speed"] <= 100):
                self.logger.error(f"無効な速度: {step['speed']}")
                return False
            
            if not (0 <= step["duration"] <= 10):
                self.logger.error(f"無効な時間: {step['duration']}")
                return False
        
        return True
    
    def get_execution_plan(self, plan: Dict) -> List[Dict]:
        """
        実行可能なモーター制御コマンドのリストを取得
        
        Args:
            plan: 生成された計画
            
        Returns:
            実行可能なコマンドのリスト
        """
        if not self.validate_plan(plan):
            self.logger.error("無効な計画です")
            return []
        
        execution_commands = []
        
        for step in plan["plan"]:
            # 待機コマンドの場合は特別処理
            if step["action"] == "wait":
                execution_commands.append({
                    "action": "wait",
                    "speed": 0,
                    "duration": step["duration"],
                    "description": step["description"]
                })
            else:
                # 通常のモーター制御コマンド
                execution_commands.append({
                    "action": step["action"],
                    "speed": step["speed"],
                    "duration": step["duration"],
                    "description": step["description"]
                })
        
        return execution_commands


def main():
    """テスト用のメイン関数"""
    print("🤖 高度なモーター制御AIシステムテスト")
    print("=" * 50)
    
    try:
        # AI対話システムを初期化
        advanced_ai = AdvancedMotorAI()
        
        print("🎯 複雑な指示の解析テストを開始します")
        print("💡 複雑な音声指示を入力してください")
        print("⏹️  'quit' で終了")
        
        # テスト用の複雑な指示
        test_commands = [
            "まっすぐ行って、右に曲がって",
            "左に回って、前に進んで、止まって",
            "後ろに下がって、左に回って、前に進んで",
            "右に回って、速く前に進んで、左に回って"
        ]
        
        for i, test_command in enumerate(test_commands, 1):
            print(f"\nテスト {i}: {test_command}")
            print("-" * 30)
            
            # 計画を生成
            plan = advanced_ai.analyze_complex_command(test_command)
            
            # 計画の妥当性を検証
            if advanced_ai.validate_plan(plan):
                print(f"✅ 有効な計画: {plan['summary']}")
                print(f"📊 総ステップ数: {plan['total_steps']}")
                print(f"⏱️  推定時間: {plan['estimated_time']}秒")
                
                # 実行計画を取得
                execution_commands = advanced_ai.get_execution_plan(plan)
                print(f"🚗 実行コマンド数: {len(execution_commands)}")
                
                for j, cmd in enumerate(execution_commands, 1):
                    print(f"  {j}. {cmd['action']} (速度:{cmd['speed']}%, 時間:{cmd['duration']}秒) - {cmd['description']}")
            else:
                print(f"❌ 無効な計画: {plan}")
        
        print("\n✅ 全テスト完了")
        
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
