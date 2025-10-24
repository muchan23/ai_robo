#!/usr/bin/env python3
"""
車輪前進テストスクリプト
左右のモーターを同時に前進させて、ロボットが直進することを確認
"""

import time
import sys
import os

# パスを追加してモーター制御クラスをインポート
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motor.motor_controller import MotorController

def test_forward_movement():
    """前進テストのメイン関数"""
    print("🚗 車輪前進テスト")
    print("=" * 60)
    print("このテストは左右のモーターを同時に前進させて、")
    print("ロボットが直進することを確認します")
    print()
    print("⚠️  注意事項:")
    print("  - ロボットを安全な場所に置いてください")
    print("  - 十分なスペースを確保してください")
    print("  - 障害物がないことを確認してください")
    print()
    
    input("Enterキーを押してテストを開始...")
    
    try:
        # モーター制御システムを初期化
        motor_controller = MotorController()
        
        print("\n🔄 前進テストシーケンス")
        print("=" * 50)
        
        # テスト1: 低速前進
        print("\n🚗 テスト1: 低速前進 (40%, 3秒)")
        print("   → ロボットがゆっくりと前進するはずです")
        motor_controller.execute_command({
            "action": "move_forward",
            "speed": 40,
            "duration": 3.0,
            "motor": "both"
        })
        time.sleep(1)
        
        # テスト2: 中速前進
        print("\n🚗 テスト2: 中速前進 (60%, 3秒)")
        print("   → ロボットが中程度の速度で前進するはずです")
        motor_controller.execute_command({
            "action": "move_forward",
            "speed": 60,
            "duration": 3.0,
            "motor": "both"
        })
        time.sleep(1)
        
        # テスト3: 高速前進
        print("\n🚗 テスト3: 高速前進 (80%, 3秒)")
        print("   → ロボットが高速で前進するはずです")
        motor_controller.execute_command({
            "action": "move_forward",
            "speed": 80,
            "duration": 3.0,
            "motor": "both"
        })
        time.sleep(1)
        
        # テスト4: 後退テスト
        print("\n🚗 テスト4: 後退テスト (50%, 3秒)")
        print("   → ロボットが後退するはずです")
        motor_controller.execute_command({
            "action": "move_backward",
            "speed": 50,
            "duration": 3.0,
            "motor": "both"
        })
        time.sleep(1)
        
        # テスト5: 直進性確認
        print("\n🚗 テスト5: 直進性確認 (60%, 5秒)")
        print("   → ロボットが真っ直ぐ前進することを確認してください")
        print("   → 左右に曲がらないことを確認してください")
        motor_controller.execute_command({
            "action": "move_forward",
            "speed": 60,
            "duration": 5.0,
            "motor": "both"
        })
        
        print("\n✅ 前進テスト完了")
        print("📊 結果確認:")
        print("  - ロボットは前進しましたか？")
        print("  - 速度の違いが分かりましたか？")
        print("  - 直進性は良好でしたか？")
        print("  - 後退も正常に動作しましたか？")
        print()
        print("❌ 問題がある場合:")
        print("  - 左右の速度が違う → speed_calibration_test.pyを実行")
        print("  - 回転方向が逆 → rotation_direction_test.pyを実行")
        print("  - 動かない → 配線と電源を確認")
        
    except KeyboardInterrupt:
        print("\n⏹️ テストが中断されました")
    except Exception as e:
        print(f"❌ エラー: {e}")
        return 1
    finally:
        if 'motor_controller' in locals():
            motor_controller.cleanup()
    
    return 0


def test_individual_motor_forward():
    """個別モーター前進テスト"""
    print("\n🔧 個別モーター前進テスト")
    print("=" * 50)
    print("左右のモーターを個別に動かして、")
    print("それぞれが正常に前進することを確認します")
    print()
    
    try:
        motor_controller = MotorController()
        
        # 左モーター前進テスト
        print("🔄 左モーター (モーターA) 前進テスト")
        print("   → 左タイヤのみが回転するはずです")
        motor_controller.execute_command({
            "action": "move_forward",
            "speed": 50,
            "duration": 3.0,
            "motor": "left"
        })
        time.sleep(1)
        
        # 右モーター前進テスト
        print("🔄 右モーター (モーターB) 前進テスト")
        print("   → 右タイヤのみが回転するはずです")
        motor_controller.execute_command({
            "action": "move_forward",
            "speed": 50,
            "duration": 3.0,
            "motor": "right"
        })
        time.sleep(1)
        
        print("\n✅ 個別モーターテスト完了")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return 1
    finally:
        if 'motor_controller' in locals():
            motor_controller.cleanup()
    
    return 0


def main():
    """メイン関数"""
    print("🚗 車輪前進テストシステム")
    print("=" * 60)
    print("このシステムは以下のテストを実行します:")
    print("  1. 両モーター同時前進テスト")
    print("  2. 個別モーター前進テスト")
    print()
    
    choice = input("テストを選択してください (1: 両モーター, 2: 個別モーター, 3: 両方): ").strip()
    
    if choice == "1":
        return test_forward_movement()
    elif choice == "2":
        return test_individual_motor_forward()
    elif choice == "3":
        print("\n🔄 両方のテストを実行します")
        result1 = test_forward_movement()
        if result1 == 0:
            result2 = test_individual_motor_forward()
            return result2
        return result1
    else:
        print("❌ 無効な選択です")
        return 1


if __name__ == "__main__":
    exit(main())
