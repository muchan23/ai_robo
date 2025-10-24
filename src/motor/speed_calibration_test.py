#!/usr/bin/env python3
"""
モーター速度調整テストスクリプト
左右のモーターの速度差を測定し、最適な補正係数を決定
"""

import time
import logging
import RPi.GPIO as GPIO
from motor_controller import MotorController

class SpeedCalibrationTest:
    """モーター速度調整テストクラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = self._setup_logging()
        self.motor_controller = MotorController()
        
    def _setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.DEBUG,  # デバッグレベルで詳細ログを表示
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def test_individual_motor_speeds(self):
        """個別モーター速度テスト"""
        print("🔧 個別モーター速度テスト")
        print("=" * 50)
        
        test_speeds = [30, 50, 70, 90]
        duration = 3.0
        
        for speed in test_speeds:
            print(f"\n📊 速度{speed}%でのテスト")
            
            # 左モーター（モーターA）テスト
            print(f"  🔄 左モーター (モーターA) 前進: {speed}%")
            self.motor_controller.execute_command({
                "action": "move_forward",
                "speed": speed,
                "duration": duration,
                "motor": "left"
            })
            time.sleep(1)
            
            # 右モーター（モーターB）テスト
            print(f"  🔄 右モーター (モーターB) 前進: {speed}%")
            self.motor_controller.execute_command({
                "action": "move_forward",
                "speed": speed,
                "duration": duration,
                "motor": "right"
            })
            time.sleep(1)
    
    def test_speed_difference(self):
        """速度差テスト"""
        print("\n📈 速度差テスト")
        print("=" * 50)
        print("両モーターを同時に動かして、直進性を確認します")
        
        test_commands = [
            {"speed": 50, "duration": 5.0, "message": "中速直進テスト"},
            {"speed": 70, "duration": 5.0, "message": "高速直進テスト"},
            {"speed": 30, "duration": 5.0, "message": "低速直進テスト"},
        ]
        
        for command in test_commands:
            print(f"\n🚗 {command['message']}")
            self.motor_controller.execute_command({
                "action": "move_forward",
                "speed": command["speed"],
                "duration": command["duration"],
                "motor": "both"
            })
            time.sleep(1)
    
    def test_turn_consistency(self):
        """回転一貫性テスト"""
        print("\n🔄 回転一貫性テスト")
        print("=" * 50)
        
        test_commands = [
            {"action": "turn_left", "speed": 60, "duration": 3.0, "message": "左回転テスト"},
            {"action": "turn_right", "speed": 60, "duration": 3.0, "message": "右回転テスト"},
        ]
        
        for command in test_commands:
            print(f"\n🔄 {command['message']}")
            self.motor_controller.execute_command(command)
            time.sleep(1)
    
    def interactive_speed_calibration(self):
        """インタラクティブ速度調整"""
        print("\n🎛️ インタラクティブ速度調整")
        print("=" * 50)
        print("左右のモーターの速度を手動で調整できます")
        print("現在の補正係数:")
        print(f"  モーターA (左): {self.motor_controller.speed_correction_a:.2f}")
        print(f"  モーターB (右): {self.motor_controller.speed_correction_b:.2f}")
        
        while True:
            print("\n調整オプション:")
            print("1. モーターA (左) の補正係数を変更")
            print("2. モーターB (右) の補正係数を変更")
            print("3. 現在の設定でテスト実行")
            print("4. 終了")
            
            choice = input("選択してください (1-4): ").strip()
            
            if choice == "1":
                try:
                    new_value = float(input("モーターA (左) の補正係数を入力 (0.5-2.0): "))
                    self.motor_controller.set_speed_correction(
                        motor_a_correction=new_value,
                        motor_b_correction=self.motor_controller.speed_correction_b
                    )
                except ValueError:
                    print("❌ 無効な値です")
            
            elif choice == "2":
                try:
                    new_value = float(input("モーターB (右) の補正係数を入力 (0.5-2.0): "))
                    self.motor_controller.set_speed_correction(
                        motor_a_correction=self.motor_controller.speed_correction_a,
                        motor_b_correction=new_value
                    )
                except ValueError:
                    print("❌ 無効な値です")
            
            elif choice == "3":
                print("\n🧪 テスト実行中...")
                self.motor_controller.execute_command({
                    "action": "move_forward",
                    "speed": 50,
                    "duration": 3.0,
                    "motor": "both"
                })
                print("直進性を確認してください")
            
            elif choice == "4":
                break
            
            else:
                print("❌ 無効な選択です")
    
    def auto_calibration_suggestion(self):
        """自動調整提案"""
        print("\n🤖 自動調整提案")
        print("=" * 50)
        print("以下の手順で最適な補正係数を見つけてください:")
        print()
        print("1. 両モーターを同じ速度で前進させます")
        print("2. ロボットが右に曲がる場合:")
        print("   - モーターA (左) の補正係数を上げる (例: 1.1)")
        print("   - または モーターB (右) の補正係数を下げる (例: 0.9)")
        print()
        print("3. ロボットが左に曲がる場合:")
        print("   - モーターA (左) の補正係数を下げる (例: 0.9)")
        print("   - または モーターB (右) の補正係数を上げる (例: 1.1)")
        print()
        print("4. 直進するまで調整を繰り返します")
        print()
        print("💡 推奨開始値:")
        print("   - モーターA: 1.0")
        print("   - モーターB: 1.0")
        print("   - 0.05刻みで調整してください")
    
    def run_full_calibration(self):
        """完全調整テスト"""
        print("🚗 モーター速度調整テスト開始")
        print("=" * 60)
        
        try:
            # 1. 個別モーター速度テスト
            self.test_individual_motor_speeds()
            
            # 2. 速度差テスト
            self.test_speed_difference()
            
            # 3. 回転一貫性テスト
            self.test_turn_consistency()
            
            # 4. 自動調整提案
            self.auto_calibration_suggestion()
            
            # 5. インタラクティブ調整
            self.interactive_speed_calibration()
            
            print("\n✅ 調整テスト完了")
            print(f"最終補正係数:")
            print(f"  モーターA (左): {self.motor_controller.speed_correction_a:.2f}")
            print(f"  モーターB (右): {self.motor_controller.speed_correction_b:.2f}")
            
        except KeyboardInterrupt:
            print("\n⏹️ テストが中断されました")
        except Exception as e:
            print(f"❌ エラー: {e}")
        finally:
            self.motor_controller.cleanup()


def main():
    """メイン関数"""
    print("🔧 モーター速度調整テスト")
    print("=" * 60)
    print("このテストは左右のモーターの速度差を測定し、")
    print("最適な補正係数を見つけるのに役立ちます。")
    print()
    print("⚠️  注意: モーターが接続されていることを確認してください")
    print("⚠️  安全な場所でテストを実行してください")
    print()
    
    input("Enterキーを押してテストを開始...")
    
    calibration_test = SpeedCalibrationTest()
    calibration_test.run_full_calibration()


if __name__ == "__main__":
    main()
