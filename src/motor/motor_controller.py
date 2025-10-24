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
        
        # GPIO設定 - 4チャンネル制御
        # モーターA (左モーター)
        self.motor_a_pin1 = 17  # IN1
        self.motor_a_pin2 = 22  # IN2
        self.motor_a_pwm = 18   # ENA (PWM)
        
        # モーターB (右モーター)
        self.motor_b_pin1 = 23  # IN3
        self.motor_b_pin2 = 24  # IN4
        self.motor_b_pwm = 25   # ENB (PWM)
        
        # モーター制御用変数
        self.pwm_a = None
        self.pwm_b = None
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
            
            # モーターA (左モーター) のGPIO設定
            GPIO.setup(self.motor_a_pin1, GPIO.OUT)
            GPIO.setup(self.motor_a_pin2, GPIO.OUT)
            GPIO.setup(self.motor_a_pwm, GPIO.OUT)
            
            # モーターB (右モーター) のGPIO設定
            GPIO.setup(self.motor_b_pin1, GPIO.OUT)
            GPIO.setup(self.motor_b_pin2, GPIO.OUT)
            GPIO.setup(self.motor_b_pwm, GPIO.OUT)
            
            # PWM初期化
            self.pwm_a = GPIO.PWM(self.motor_a_pwm, 1000)  # 1kHz
            self.pwm_b = GPIO.PWM(self.motor_b_pwm, 1000)  # 1kHz
            self.pwm_a.start(0)  # 0%で開始
            self.pwm_b.start(0)  # 0%で開始
            
            self.is_initialized = True
            self.logger.info("4チャンネルGPIO初期化完了")
            
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
        motor = command.get("motor", "both")  # "left", "right", "both"
        
        self.logger.info(f"コマンド実行: {action}, 速度: {speed}%, 時間: {duration}秒, モーター: {motor}")
        
        try:
            if action == "move_forward":
                self._move_forward(speed, duration, motor)
            elif action == "move_backward":
                self._move_backward(speed, duration, motor)
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
    
    def _move_forward(self, speed: int, duration: float, motor: str = "both"):
        """前進"""
        self.logger.info(f"前進: 速度{speed}%, {duration}秒, モーター: {motor}")
        
        if motor in ["left", "both"]:
            # 左モーター (モーターA) 前進
            GPIO.output(self.motor_a_pin1, GPIO.LOW)
            GPIO.output(self.motor_a_pin2, GPIO.HIGH)
            self.pwm_a.ChangeDutyCycle(speed)
        
        if motor in ["right", "both"]:
            # 右モーター (モーターB) 前進
            GPIO.output(self.motor_b_pin1, GPIO.LOW)
            GPIO.output(self.motor_b_pin2, GPIO.HIGH)
            self.pwm_b.ChangeDutyCycle(speed)
        
        time.sleep(duration)
        self._stop()
    
    def _move_backward(self, speed: int, duration: float, motor: str = "both"):
        """後退"""
        self.logger.info(f"後退: 速度{speed}%, {duration}秒, モーター: {motor}")
        
        if motor in ["left", "both"]:
            # 左モーター (モーターA) 後退
            GPIO.output(self.motor_a_pin1, GPIO.HIGH)
            GPIO.output(self.motor_a_pin2, GPIO.LOW)
            self.pwm_a.ChangeDutyCycle(speed)
        
        if motor in ["right", "both"]:
            # 右モーター (モーターB) 後退
            GPIO.output(self.motor_b_pin1, GPIO.HIGH)
            GPIO.output(self.motor_b_pin2, GPIO.LOW)
            self.pwm_b.ChangeDutyCycle(speed)
        
        time.sleep(duration)
        self._stop()
    
    def _turn_left(self, speed: int, duration: float):
        """左回転（右モーター前進、左モーター後退）"""
        self.logger.info(f"左回転: 速度{speed}%, {duration}秒")
        
        # 左モーター (モーターA) 後退
        GPIO.output(self.motor_a_pin1, GPIO.HIGH)
        GPIO.output(self.motor_a_pin2, GPIO.LOW)
        self.pwm_a.ChangeDutyCycle(speed)
        
        # 右モーター (モーターB) 前進
        GPIO.output(self.motor_b_pin1, GPIO.LOW)
        GPIO.output(self.motor_b_pin2, GPIO.HIGH)
        self.pwm_b.ChangeDutyCycle(speed)
        
        time.sleep(duration)
        self._stop()
    
    def _turn_right(self, speed: int, duration: float):
        """右回転（左モーター前進、右モーター後退）"""
        self.logger.info(f"右回転: 速度{speed}%, {duration}秒")
        
        # 左モーター (モーターA) 前進
        GPIO.output(self.motor_a_pin1, GPIO.LOW)
        GPIO.output(self.motor_a_pin2, GPIO.HIGH)
        self.pwm_a.ChangeDutyCycle(speed)
        
        # 右モーター (モーターB) 後退
        GPIO.output(self.motor_b_pin1, GPIO.HIGH)
        GPIO.output(self.motor_b_pin2, GPIO.LOW)
        self.pwm_b.ChangeDutyCycle(speed)
        
        time.sleep(duration)
        self._stop()
    
    def _stop(self):
        """停止"""
        self.logger.info("停止")
        # 両方のモーターを停止
        GPIO.output(self.motor_a_pin1, GPIO.LOW)
        GPIO.output(self.motor_a_pin2, GPIO.LOW)
        GPIO.output(self.motor_b_pin1, GPIO.LOW)
        GPIO.output(self.motor_b_pin2, GPIO.LOW)
        self.pwm_a.ChangeDutyCycle(0)
        self.pwm_b.ChangeDutyCycle(0)
    
    def cleanup(self):
        """リソースのクリーンアップ"""
        try:
            if self.pwm_a:
                self.pwm_a.stop()
            if self.pwm_b:
                self.pwm_b.stop()
            GPIO.cleanup()
            self.logger.info("4チャンネルモーター制御システムをクリーンアップしました")
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
        
        # テストコマンド - 4チャンネル制御
        test_commands = [
            {"action": "move_forward", "speed": 50, "duration": 2.0, "motor": "both", "message": "両モーター前進テスト"},
            {"action": "stop", "speed": 0, "duration": 1.0, "message": "停止"},
            {"action": "move_forward", "speed": 40, "duration": 1.5, "motor": "left", "message": "左モーター前進テスト"},
            {"action": "stop", "speed": 0, "duration": 1.0, "message": "停止"},
            {"action": "move_forward", "speed": 40, "duration": 1.5, "motor": "right", "message": "右モーター前進テスト"},
            {"action": "stop", "speed": 0, "duration": 1.0, "message": "停止"},
            {"action": "turn_left", "speed": 60, "duration": 2.0, "message": "左回転テスト"},
            {"action": "stop", "speed": 0, "duration": 1.0, "message": "停止"},
            {"action": "turn_right", "speed": 60, "duration": 2.0, "message": "右回転テスト"},
            {"action": "stop", "speed": 0, "duration": 1.0, "message": "停止"},
            {"action": "move_backward", "speed": 30, "duration": 1.5, "motor": "both", "message": "両モーター後退テスト"},
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
