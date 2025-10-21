#!/usr/bin/env python3
"""
モーター制御システム
AI解釈されたコマンドを実際のモーター制御に変換
"""

import time
import logging
import RPi.GPIO as GPIO
from typing import Dict

class MotorController:
    """モーター制御クラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = self._setup_logging()
        
        # GPIO設定
        self.motor_pin1 = 17  # IN1
        self.motor_pin2 = 22  # IN2
        self.pwm_pin = 18     # PWM
        
        # モーター制御用変数
        self.pwm = None
        self.is_initialized = False
        
        self._initialize_gpio()
        self.logger.info("モーター制御システムを初期化しました")
    
    def _setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def _initialize_gpio(self):
        """GPIO初期化"""
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.motor_pin1, GPIO.OUT)
            GPIO.setup(self.motor_pin2, GPIO.OUT)
            GPIO.setup(self.pwm_pin, GPIO.OUT)
            
            # PWM初期化
            self.pwm = GPIO.PWM(self.pwm_pin, 100)  # 100Hz
            self.pwm.start(0)  # 0%で開始
            
            self.is_initialized = True
            self.logger.info("GPIO初期化完了")
            
        except Exception as e:
            self.logger.error(f"GPIO初期化エラー: {e}")
            raise
    
    def execute_command(self, command: Dict):
        """
        AI解釈されたコマンドを実行
        
        Args:
            command: モーター制御コマンド
        """
        if not self.is_initialized:
            self.logger.error("モーター制御システムが初期化されていません")
            return
        
        action = command.get("action", "stop")
        speed = command.get("speed", 0)
        duration = command.get("duration", 0)
        
        self.logger.info(f"コマンド実行: {action}, 速度: {speed}%, 時間: {duration}秒")
        
        try:
            if action == "move_forward":
                self._move_forward(speed, duration)
            elif action == "move_backward":
                self._move_backward(speed, duration)
            elif action == "turn_left":
                self._turn_left(speed, duration)
            elif action == "turn_right":
                self._turn_right(speed, duration)
            elif action == "stop":
                self._stop()
            else:
                self.logger.error(f"未知のアクション: {action}")
                
        except Exception as e:
            self.logger.error(f"コマンド実行エラー: {e}")
    
    def _move_forward(self, speed: int, duration: float):
        """前進"""
        self.logger.info(f"前進: 速度{speed}%, {duration}秒")
        GPIO.output(self.motor_pin1, GPIO.LOW)
        GPIO.output(self.motor_pin2, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(speed)
        time.sleep(duration)
        self._stop()
    
    def _move_backward(self, speed: int, duration: float):
        """後退"""
        self.logger.info(f"後退: 速度{speed}%, {duration}秒")
        GPIO.output(self.motor_pin1, GPIO.HIGH)
        GPIO.output(self.motor_pin2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(speed)
        time.sleep(duration)
        self._stop()
    
    def _turn_left(self, speed: int, duration: float):
        """左回転"""
        self.logger.info(f"左回転: 速度{speed}%, {duration}秒")
        # 左回転の実装（モーターの接続に応じて調整）
        GPIO.output(self.motor_pin1, GPIO.LOW)
        GPIO.output(self.motor_pin2, GPIO.LOW)  # ブレーキ
        self.pwm.ChangeDutyCycle(speed)
        time.sleep(duration)
        self._stop()
    
    def _turn_right(self, speed: int, duration: float):
        """右回転"""
        self.logger.info(f"右回転: 速度{speed}%, {duration}秒")
        # 右回転の実装（モーターの接続に応じて調整）
        GPIO.output(self.motor_pin1, GPIO.HIGH)
        GPIO.output(self.motor_pin2, GPIO.HIGH)  # ブレーキ
        self.pwm.ChangeDutyCycle(speed)
        time.sleep(duration)
        self._stop()
    
    def _stop(self):
        """停止"""
        self.logger.info("停止")
        GPIO.output(self.motor_pin1, GPIO.LOW)
        GPIO.output(self.motor_pin2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)
    
    def cleanup(self):
        """リソースのクリーンアップ"""
        try:
            if self.pwm:
                self.pwm.stop()
            GPIO.cleanup()
            self.logger.info("モーター制御システムをクリーンアップしました")
        except Exception as e:
            self.logger.error(f"クリーンアップエラー: {e}")


def main():
    """テスト用のメイン関数"""
    print("🚗 モーター制御システムテスト")
    print("=" * 50)
    
    try:
        # モーター制御システムを初期化
        motor_controller = MotorController()
        
        print("🎯 モーター制御テストを開始します")
        print("💡 テストコマンドを実行します")
        
        # テストコマンド
        test_commands = [
            {"action": "move_forward", "speed": 50, "duration": 2.0, "message": "前進テスト"},
            {"action": "stop", "speed": 0, "duration": 1.0, "message": "停止"},
            {"action": "move_backward", "speed": 30, "duration": 1.5, "message": "後退テスト"},
            {"action": "stop", "speed": 0, "duration": 1.0, "message": "停止"},
        ]
        
        for i, command in enumerate(test_commands, 1):
            print(f"\nテスト {i}: {command['message']}")
            motor_controller.execute_command(command)
            time.sleep(0.5)
        
        print("\n✅ テスト完了")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return 1
    finally:
        if 'motor_controller' in locals():
            motor_controller.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
