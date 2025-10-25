#!/usr/bin/env python3
"""
高度なモーター制御システム
複数ステップの計画を実行し、柔軟なモーター制御を実現
"""

import sys
import os
import time
import logging
import RPi.GPIO as GPIO
from typing import Dict, List

# プロジェクトルートをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.motor.motor_controller import MotorController

class AdvancedMotorController:
    """高度なモーター制御クラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = self._setup_logging()
        
        # 基本モーター制御システムを初期化
        self.motor_controller = MotorController()
        
        # 実行状態管理
        self.is_executing = False
        self.current_step = 0
        self.total_steps = 0
        self.execution_plan = []
        
        self.logger.info("高度なモーター制御システムを初期化しました")
    
    def _setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def execute_complex_plan(self, plan: Dict) -> bool:
        """
        複雑な計画を実行
        
        Args:
            plan: 実行する計画
            
        Returns:
            実行成功の真偽値
        """
        if not plan or "plan" not in plan:
            self.logger.error("無効な計画です")
            return False
        
        self.execution_plan = plan["plan"]
        self.total_steps = len(self.execution_plan)
        self.current_step = 0
        self.is_executing = True
        
        self.logger.info(f"複雑な計画の実行を開始: {plan['summary']}")
        self.logger.info(f"総ステップ数: {self.total_steps}, 推定時間: {plan.get('estimated_time', 0)}秒")
        
        try:
            for step in self.execution_plan:
                if not self.is_executing:
                    self.logger.info("実行が中断されました")
                    break
                
                self.current_step += 1
                self._execute_step(step)
                
                # ステップ間の待機（必要に応じて）
                if self.current_step < self.total_steps:
                    time.sleep(0.2)  # 200msの間隔
            
            self.logger.info("複雑な計画の実行が完了しました")
            return True
            
        except Exception as e:
            self.logger.error(f"計画実行エラー: {e}")
            return False
        finally:
            self.is_executing = False
            self.current_step = 0
            self.total_steps = 0
            self.execution_plan = []
    
    def _execute_step(self, step: Dict):
        """
        個別ステップを実行
        
        Args:
            step: 実行するステップ
        """
        step_num = step.get("step", self.current_step)
        action = step.get("action", "stop")
        speed = step.get("speed", 0)
        duration = step.get("duration", 0)
        description = step.get("description", "")
        
        self.logger.info(f"ステップ {step_num}: {action} (速度:{speed}%, 時間:{duration}秒) - {description}")
        
        try:
            if action == "wait":
                # 待機処理
                self._wait(duration)
            elif action == "stop":
                # 停止処理
                self.motor_controller._stop()
            else:
                # 通常のモーター制御
                command = {
                    "action": action,
                    "speed": speed,
                    "duration": duration
                }
                self.motor_controller.execute_command(command)
                
        except Exception as e:
            self.logger.error(f"ステップ実行エラー: {e}")
            raise
    
    def _wait(self, duration: float):
        """
        待機処理
        
        Args:
            duration: 待機時間（秒）
        """
        if duration > 0:
            self.logger.info(f"待機中: {duration}秒")
            time.sleep(duration)
    
    def stop_execution(self):
        """実行を停止"""
        self.logger.info("実行を停止します")
        self.is_executing = False
        self.motor_controller._stop()
    
    def get_execution_status(self) -> Dict:
        """
        実行状態を取得
        
        Returns:
            実行状態の辞書
        """
        return {
            "is_executing": self.is_executing,
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "progress": (self.current_step / self.total_steps * 100) if self.total_steps > 0 else 0,
            "remaining_steps": self.total_steps - self.current_step
        }
    
    def cleanup(self):
        """リソースのクリーンアップ"""
        try:
            self.stop_execution()
            if hasattr(self.motor_controller, 'cleanup'):
                self.motor_controller.cleanup()
            self.logger.info("高度なモーター制御システムをクリーンアップしました")
        except Exception as e:
            self.logger.error(f"クリーンアップエラー: {e}")


def main():
    """テスト用のメイン関数"""
    print("🚗 高度なモーター制御システムテスト")
    print("=" * 50)
    
    try:
        # 高度なモーター制御システムを初期化
        advanced_controller = AdvancedMotorController()
        
        # テスト用の複雑な計画
        test_plan = {
            "plan": [
                {
                    "step": 1,
                    "action": "move_forward",
                    "speed": 50,
                    "duration": 2.0,
                    "description": "前進します"
                },
                {
                    "step": 2,
                    "action": "turn_right",
                    "speed": 85,
                    "duration": 1.0,
                    "description": "右に回転します"
                },
                {
                    "step": 3,
                    "action": "move_forward",
                    "speed": 60,
                    "duration": 1.5,
                    "description": "再び前進します"
                },
                {
                    "step": 4,
                    "action": "stop",
                    "speed": 0,
                    "duration": 0,
                    "description": "停止します"
                }
            ],
            "total_steps": 4,
            "estimated_time": 4.5,
            "summary": "前進→右回転→前進→停止のテスト計画"
        }
        
        print("🎯 複雑な計画の実行テストを開始します")
        print(f"📋 計画: {test_plan['summary']}")
        print(f"📊 総ステップ数: {test_plan['total_steps']}")
        print(f"⏱️  推定時間: {test_plan['estimated_time']}秒")
        
        input("\nEnterキーを押してテストを開始...")
        
        # 計画を実行
        success = advanced_controller.execute_complex_plan(test_plan)
        
        if success:
            print("\n✅ 計画の実行が完了しました")
        else:
            print("\n❌ 計画の実行に失敗しました")
        
        # 実行状態を表示
        status = advanced_controller.get_execution_status()
        print(f"\n📊 実行状態: {status}")
        
    except KeyboardInterrupt:
        print("\n⏹️ テストが中断されました")
    except Exception as e:
        print(f"❌ エラー: {e}")
        return 1
    finally:
        if 'advanced_controller' in locals():
            advanced_controller.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
