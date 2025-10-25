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
        
        # モーターB (右モーター) - クロストーク回避のためピンを変更
        self.motor_b_pin1 = 19  # IN3 (GPIO 23 → 19に変更)
        self.motor_b_pin2 = 26  # IN4 (GPIO 24 → 26に変更)
        self.motor_b_pwm = 13   # ENB (GPIO 25 → 13に変更)
        
        # モーター制御用変数
        self.pwm_a = None
        self.pwm_b = None
        self.is_initialized = False
        
        # 速度調整係数（モーターの個体差を補正）
        self.speed_correction_a = 1.0  # モーターAの補正係数
        self.speed_correction_b = 1.0  # モーターBの補正係数
        
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
            
            # PWM初期化 - モーターに最適化された周波数
            self.pwm_a = GPIO.PWM(self.motor_a_pwm, 500)   # 500Hz (モーターA用)
            self.pwm_b = GPIO.PWM(self.motor_b_pwm, 500)   # 500Hz (モーターB用)
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
    
    def test_rotation_direction(self, speed: int = 30, duration: float = 3.0):
        """
        タイヤの回転方向テスト
        左右のモーターが同じ方向に回転するかを確認
        
        Args:
            speed: テスト速度 (0-100)
            duration: テスト時間 (秒)
        """
        self.logger.info("タイヤ回転方向テスト開始")
        print("🔄 タイヤ回転方向テスト")
        print("=" * 50)
        print("⚠️  注意: 左右のタイヤが同じ方向に回転することを確認してください")
        print()
        
        # テスト1: 左モーター前進
        print("🔄 テスト1: 左モーター (モーターA) 前進")
        print("   → 左タイヤが時計回りに回転するはずです")
        self._move_forward(speed, duration, "left")
        time.sleep(1)
        
        # テスト2: 右モーター前進
        print("🔄 テスト2: 右モーター (モーターB) 前進")
        print("   → 右タイヤが時計回りに回転するはずです")
        self._move_forward(speed, duration, "right")
        time.sleep(1)
        
        # テスト3: 両モーター前進
        print("🔄 テスト3: 両モーター前進")
        print("   → 両方のタイヤが同じ方向（時計回り）に回転するはずです")
        self._move_forward(speed, duration, "both")
        time.sleep(1)
        
        # テスト4: 左モーター後退
        print("🔄 テスト4: 左モーター (モーターA) 後退")
        print("   → 左タイヤが反時計回りに回転するはずです")
        self._move_backward(speed, duration, "left")
        time.sleep(1)
        
        # テスト5: 右モーター後退
        print("🔄 テスト5: 右モーター (モーターB) 後退")
        print("   → 右タイヤが反時計回りに回転するはずです")
        self._move_backward(speed, duration, "right")
        time.sleep(1)
        
        # テスト6: 両モーター後退
        print("🔄 テスト6: 両モーター後退")
        print("   → 両方のタイヤが同じ方向（反時計回り）に回転するはずです")
        self._move_backward(speed, duration, "both")
        
        print("\n✅ 回転方向テスト完了")
        print("📋 確認事項:")
        print("   - テスト1と2で同じ方向に回転したか？")
        print("   - テスト3で両方のタイヤが同じ方向に回転したか？")
        print("   - テスト4と5で同じ方向に回転したか？")
        print("   - テスト6で両方のタイヤが同じ方向に回転したか？")
        print()
        print("❌ もし逆方向に回転している場合は、配線を確認してください")
    
    def set_speed_correction(self, motor_a_correction: float = 1.0, motor_b_correction: float = 1.0):
        """
        モーター速度調整係数を設定
        
        Args:
            motor_a_correction: モーターAの補正係数 (0.5-2.0)
            motor_b_correction: モーターBの補正係数 (0.5-2.0)
        """
        self.speed_correction_a = max(0.1, min(2.0, motor_a_correction))
        self.speed_correction_b = max(0.1, min(2.0, motor_b_correction))
        self.logger.info(f"速度調整係数設定: モーターA={self.speed_correction_a:.2f}, モーターB={self.speed_correction_b:.2f}")
    
    def _apply_speed_correction(self, speed: int, motor: str) -> int:
        """
        速度に補正係数を適用
        
        Args:
            speed: 元の速度 (0-100)
            motor: モーター指定 ("left", "right", "both")
            
        Returns:
            補正後の速度 (0-100)
        """
        if motor == "left" or motor == "both":
            corrected_speed = int(speed * self.speed_correction_a)
        elif motor == "right":
            corrected_speed = int(speed * self.speed_correction_b)
        else:
            corrected_speed = speed
        
        # 最低動作速度を30%に設定（モーターの特性に応じて調整）
        corrected_speed = max(30, min(100, corrected_speed))
        
        return corrected_speed
    
    def _move_forward(self, speed: int, duration: float, motor: str = "both"):
        """前進"""
        self.logger.info(f"前進: 速度{speed}%, {duration}秒, モーター: {motor}")
        
        if motor in ["left", "both"]:
            # 左モーター (モーターA) 前進
            corrected_speed_a = self._apply_speed_correction(speed, "left")
            GPIO.output(self.motor_a_pin1, GPIO.LOW)
            GPIO.output(self.motor_a_pin2, GPIO.HIGH)
            self.pwm_a.ChangeDutyCycle(corrected_speed_a)
            self.logger.debug(f"モーターA: 元速度{speed}% → 補正後{corrected_speed_a}%")
        
        if motor in ["right", "both"]:
            # 右モーター (モーターB) 前進
            corrected_speed_b = self._apply_speed_correction(speed, "right")
            GPIO.output(self.motor_b_pin1, GPIO.LOW)
            GPIO.output(self.motor_b_pin2, GPIO.HIGH)
            self.pwm_b.ChangeDutyCycle(corrected_speed_b)
            self.logger.debug(f"モーターB: 元速度{speed}% → 補正後{corrected_speed_b}%")
        
        time.sleep(duration)
        self._stop()
    
    def _move_backward(self, speed: int, duration: float, motor: str = "both"):
        """後退"""
        self.logger.info(f"後退: 速度{speed}%, {duration}秒, モーター: {motor}")
        
        if motor in ["left", "both"]:
            # 左モーター (モーターA) 後退
            corrected_speed_a = self._apply_speed_correction(speed, "left")
            GPIO.output(self.motor_a_pin1, GPIO.HIGH)
            GPIO.output(self.motor_a_pin2, GPIO.LOW)
            self.pwm_a.ChangeDutyCycle(corrected_speed_a)
            self.logger.debug(f"モーターA: 元速度{speed}% → 補正後{corrected_speed_a}%")
        
        if motor in ["right", "both"]:
            # 右モーター (モーターB) 後退
            corrected_speed_b = self._apply_speed_correction(speed, "right")
            GPIO.output(self.motor_b_pin1, GPIO.HIGH)
            GPIO.output(self.motor_b_pin2, GPIO.LOW)
            self.pwm_b.ChangeDutyCycle(corrected_speed_b)
            self.logger.debug(f"モーターB: 元速度{speed}% → 補正後{corrected_speed_b}%")
        
        time.sleep(duration)
        self._stop()
    
    def _turn_left(self, speed: int, duration: float):
        """左回転（右モーター前進、左モーター後退）"""
        self.logger.info(f"左回転: 速度{speed}%, {duration}秒")
        
        # 左モーター (モーターA) 後退
        corrected_speed_a = self._apply_speed_correction(speed, "left")
        GPIO.output(self.motor_a_pin1, GPIO.HIGH)
        GPIO.output(self.motor_a_pin2, GPIO.LOW)
        self.pwm_a.ChangeDutyCycle(corrected_speed_a)
        self.logger.debug(f"左回転 - モーターA: 元速度{speed}% → 補正後{corrected_speed_a}%")
        
        # 右モーター (モーターB) 前進
        corrected_speed_b = self._apply_speed_correction(speed, "right")
        GPIO.output(self.motor_b_pin1, GPIO.LOW)
        GPIO.output(self.motor_b_pin2, GPIO.HIGH)
        self.pwm_b.ChangeDutyCycle(corrected_speed_b)
        self.logger.debug(f"左回転 - モーターB: 元速度{speed}% → 補正後{corrected_speed_b}%")
        
        time.sleep(duration)
        self._stop()
    
    def _turn_right(self, speed: int, duration: float):
        """右回転（左モーター前進、右モーター後退）"""
        self.logger.info(f"右回転: 速度{speed}%, {duration}秒")
        
        # 左モーター (モーターA) 前進
        corrected_speed_a = self._apply_speed_correction(speed, "left")
        GPIO.output(self.motor_a_pin1, GPIO.LOW)
        GPIO.output(self.motor_a_pin2, GPIO.HIGH)
        self.pwm_a.ChangeDutyCycle(corrected_speed_a)
        self.logger.debug(f"右回転 - モーターA: 元速度{speed}% → 補正後{corrected_speed_a}%")
        
        # 右モーター (モーターB) 後退
        corrected_speed_b = self._apply_speed_correction(speed, "right")
        GPIO.output(self.motor_b_pin1, GPIO.HIGH)
        GPIO.output(self.motor_b_pin2, GPIO.LOW)
        self.pwm_b.ChangeDutyCycle(corrected_speed_b)
        self.logger.debug(f"右回転 - モーターB: 元速度{speed}% → 補正後{corrected_speed_b}%")
        
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
        
        # 回転方向テストを最初に実行
        print("🔄 タイヤ回転方向テストを実行します")
        motor_controller.test_rotation_direction(speed=50, duration=2.0)
        
        input("\nEnterキーを押して基本テストを開始...")
        
        # テストコマンド - 4チャンネル制御
        test_commands = [
            {"action": "move_forward", "speed": 50, "duration": 2.0, "motor": "both", "message": "両モーター前進テスト"},
            {"action": "stop", "speed": 0, "duration": 1.0, "message": "停止"},
            {"action": "move_forward", "speed": 40, "duration": 1.5, "motor": "left", "message": "左モーター前進テスト"},
            {"action": "stop", "speed": 0, "duration": 1.0, "message": "停止"},
            {"action": "move_forward", "speed": 40, "duration": 1.5, "motor": "right", "message": "右モーター前進テスト"},
            {"action": "stop", "speed": 0, "duration": 1.0, "message": "停止"},
            {"action": "turn_left", "speed": 85, "duration": 1.0, "message": "左回転テスト"},
            {"action": "stop", "speed": 0, "duration": 1.0, "message": "停止"},
            {"action": "turn_right", "speed": 85, "duration": 1.0, "message": "右回転テスト"},
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
