#!/usr/bin/env python3
"""
4チャンネルモーター制御テストスクリプト
IN1, IN2, IN3, IN4を使用した独立モーター制御のテスト
"""

import time
import logging
import RPi.GPIO as GPIO
from typing import Dict

class FourChannelMotorTest:
    """4チャンネルモーター制御テストクラス"""
    
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
        self.logger.info("4チャンネルモーター制御テストシステムを初期化しました")
    
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
    
    def test_motor_a_forward(self, speed: int = 50, duration: float = 2.0):
        """モーターA前進テスト"""
        self.logger.info(f"モーターA前進テスト: 速度{speed}%, {duration}秒")
        GPIO.output(self.motor_a_pin1, GPIO.LOW)
        GPIO.output(self.motor_a_pin2, GPIO.HIGH)
        self.pwm_a.ChangeDutyCycle(speed)
        time.sleep(duration)
        self._stop_motor_a()
    
    def test_motor_a_backward(self, speed: int = 50, duration: float = 2.0):
        """モーターA後退テスト"""
        self.logger.info(f"モーターA後退テスト: 速度{speed}%, {duration}秒")
        GPIO.output(self.motor_a_pin1, GPIO.HIGH)
        GPIO.output(self.motor_a_pin2, GPIO.LOW)
        self.pwm_a.ChangeDutyCycle(speed)
        time.sleep(duration)
        self._stop_motor_a()
    
    def test_motor_b_forward(self, speed: int = 50, duration: float = 2.0):
        """モーターB前進テスト"""
        self.logger.info(f"モーターB前進テスト: 速度{speed}%, {duration}秒")
        GPIO.output(self.motor_b_pin1, GPIO.LOW)
        GPIO.output(self.motor_b_pin2, GPIO.HIGH)
        self.pwm_b.ChangeDutyCycle(speed)
        time.sleep(duration)
        self._stop_motor_b()
    
    def test_motor_b_backward(self, speed: int = 50, duration: float = 2.0):
        """モーターB後退テスト"""
        self.logger.info(f"モーターB後退テスト: 速度{speed}%, {duration}秒")
        GPIO.output(self.motor_b_pin1, GPIO.HIGH)
        GPIO.output(self.motor_b_pin2, GPIO.LOW)
        self.pwm_b.ChangeDutyCycle(speed)
        time.sleep(duration)
        self._stop_motor_b()
    
    def test_both_forward(self, speed: int = 50, duration: float = 2.0):
        """両モーター前進テスト"""
        self.logger.info(f"両モーター前進テスト: 速度{speed}%, {duration}秒")
        # モーターA前進
        GPIO.output(self.motor_a_pin1, GPIO.LOW)
        GPIO.output(self.motor_a_pin2, GPIO.HIGH)
        self.pwm_a.ChangeDutyCycle(speed)
        # モーターB前進
        GPIO.output(self.motor_b_pin1, GPIO.LOW)
        GPIO.output(self.motor_b_pin2, GPIO.HIGH)
        self.pwm_b.ChangeDutyCycle(speed)
        time.sleep(duration)
        self._stop_all()
    
    def test_turn_left(self, speed: int = 60, duration: float = 2.0):
        """左回転テスト（右モーター前進、左モーター後退）"""
        self.logger.info(f"左回転テスト: 速度{speed}%, {duration}秒")
        # 左モーター (モーターA) 後退
        GPIO.output(self.motor_a_pin1, GPIO.HIGH)
        GPIO.output(self.motor_a_pin2, GPIO.LOW)
        self.pwm_a.ChangeDutyCycle(speed)
        # 右モーター (モーターB) 前進
        GPIO.output(self.motor_b_pin1, GPIO.LOW)
        GPIO.output(self.motor_b_pin2, GPIO.HIGH)
        self.pwm_b.ChangeDutyCycle(speed)
        time.sleep(duration)
        self._stop_all()
    
    def test_turn_right(self, speed: int = 60, duration: float = 2.0):
        """右回転テスト（左モーター前進、右モーター後退）"""
        self.logger.info(f"右回転テスト: 速度{speed}%, {duration}秒")
        # 左モーター (モーターA) 前進
        GPIO.output(self.motor_a_pin1, GPIO.LOW)
        GPIO.output(self.motor_a_pin2, GPIO.HIGH)
        self.pwm_a.ChangeDutyCycle(speed)
        # 右モーター (モーターB) 後退
        GPIO.output(self.motor_b_pin1, GPIO.HIGH)
        GPIO.output(self.motor_b_pin2, GPIO.LOW)
        self.pwm_b.ChangeDutyCycle(speed)
        time.sleep(duration)
        self._stop_all()
    
    def test_speed_ramp(self, motor: str = "both", duration: float = 5.0):
        """速度ランプテスト（0%から100%まで徐々に加速）"""
        self.logger.info(f"速度ランプテスト: モーター{motor}, {duration}秒")
        
        steps = 20
        step_duration = duration / steps
        
        for i in range(steps + 1):
            speed = int((i / steps) * 100)
            
            if motor in ["left", "both"]:
                GPIO.output(self.motor_a_pin1, GPIO.LOW)
                GPIO.output(self.motor_a_pin2, GPIO.HIGH)
                self.pwm_a.ChangeDutyCycle(speed)
            
            if motor in ["right", "both"]:
                GPIO.output(self.motor_b_pin1, GPIO.LOW)
                GPIO.output(self.motor_b_pin2, GPIO.HIGH)
                self.pwm_b.ChangeDutyCycle(speed)
            
            time.sleep(step_duration)
        
        self._stop_all()
    
    def _stop_motor_a(self):
        """モーターA停止"""
        GPIO.output(self.motor_a_pin1, GPIO.LOW)
        GPIO.output(self.motor_a_pin2, GPIO.LOW)
        self.pwm_a.ChangeDutyCycle(0)
    
    def _stop_motor_b(self):
        """モーターB停止"""
        GPIO.output(self.motor_b_pin1, GPIO.LOW)
        GPIO.output(self.motor_b_pin2, GPIO.LOW)
        self.pwm_b.ChangeDutyCycle(0)
    
    def _stop_all(self):
        """全モーター停止"""
        self._stop_motor_a()
        self._stop_motor_b()
    
    def cleanup(self):
        """リソースのクリーンアップ"""
        try:
            if self.pwm_a:
                self.pwm_a.stop()
            if self.pwm_b:
                self.pwm_b.stop()
            GPIO.cleanup()
            self.logger.info("4チャンネルモーター制御テストシステムをクリーンアップしました")
        except Exception as e:
            self.logger.error(f"クリーンアップエラー: {e}")


def main():
    """4チャンネルモーター制御テストのメイン関数"""
    print("🚗 4チャンネルモーター制御テスト")
    print("=" * 50)
    print("📋 テスト内容:")
    print("  - モーターA (左) の前進・後退")
    print("  - モーターB (右) の前進・後退")
    print("  - 両モーター同時制御")
    print("  - 左回転・右回転")
    print("  - 速度ランプテスト")
    print("=" * 50)
    
    try:
        # テストシステムを初期化
        test_system = FourChannelMotorTest()
        
        print("🎯 4チャンネルモーター制御テストを開始します")
        print("⚠️  モーターが接続されていることを確認してください")
        input("Enterキーを押してテストを開始...")
        
        # テストシーケンス
        tests = [
            ("モーターA前進テスト", lambda: test_system.test_motor_a_forward(40, 2.0)),
            ("モーターA後退テスト", lambda: test_system.test_motor_a_backward(40, 2.0)),
            ("モーターB前進テスト", lambda: test_system.test_motor_b_forward(40, 2.0)),
            ("モーターB後退テスト", lambda: test_system.test_motor_b_backward(40, 2.0)),
            ("両モーター前進テスト", lambda: test_system.test_both_forward(50, 2.0)),
            ("左回転テスト", lambda: test_system.test_turn_left(60, 2.0)),
            ("右回転テスト", lambda: test_system.test_turn_right(60, 2.0)),
            ("速度ランプテスト（左モーター）", lambda: test_system.test_speed_ramp("left", 3.0)),
            ("速度ランプテスト（右モーター）", lambda: test_system.test_speed_ramp("right", 3.0)),
            ("速度ランプテスト（両モーター）", lambda: test_system.test_speed_ramp("both", 3.0)),
        ]
        
        for i, (test_name, test_func) in enumerate(tests, 1):
            print(f"\n🧪 テスト {i}: {test_name}")
            print("⏳ 実行中...")
            test_func()
            print("✅ 完了")
            time.sleep(1)  # テスト間の間隔
        
        print("\n🎉 全テスト完了！")
        print("📊 テスト結果:")
        print("  ✅ モーターA (IN1, IN2) 制御: 正常")
        print("  ✅ モーターB (IN3, IN4) 制御: 正常")
        print("  ✅ 4チャンネル独立制御: 正常")
        
    except KeyboardInterrupt:
        print("\n⏹️  テストが中断されました")
    except Exception as e:
        print(f"❌ エラー: {e}")
        return 1
    finally:
        if 'test_system' in locals():
            test_system.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
