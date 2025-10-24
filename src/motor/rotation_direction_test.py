#!/usr/bin/env python3
"""
タイヤ回転方向テストスクリプト
左右のモーターが同じ方向に回転するかを確認する専用テスト
"""

import time
import sys
import os

# パスを追加してモーター制御クラスをインポート
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motor.motor_controller import MotorController

def main():
    """タイヤ回転方向テストのメイン関数"""
    print("🔄 タイヤ回転方向テスト")
    print("=" * 60)
    print("このテストは左右のタイヤが同じ方向に回転するかを確認します")
    print()
    print("📋 テスト内容:")
    print("  1. 左モーター (モーターA) 前進")
    print("  2. 右モーター (モーターB) 前進")
    print("  3. 両モーター前進")
    print("  4. 左モーター (モーターA) 後退")
    print("  5. 右モーター (モーターB) 後退")
    print("  6. 両モーター後退")
    print()
    print("⚠️  注意事項:")
    print("  - ロボットを安全な場所に置いてください")
    print("  - タイヤが回転する方向をよく観察してください")
    print("  - 左右のタイヤが同じ方向に回転することを確認してください")
    print()
    
    input("Enterキーを押してテストを開始...")
    
    try:
        # モーター制御システムを初期化
        motor_controller = MotorController()
        
        # 回転方向テストを実行
        motor_controller.test_rotation_direction(speed=30, duration=3.0)
        
        print("\n🎯 追加テスト: 速度を変えてテスト")
        print("=" * 50)
        
        # 異なる速度でのテスト
        test_speeds = [20, 50, 80]
        for speed in test_speeds:
            print(f"\n🚗 速度{speed}%でのテスト")
            motor_controller.execute_command({
                "action": "move_forward",
                "speed": speed,
                "duration": 2.0,
                "motor": "both"
            })
            time.sleep(1)
        
        print("\n✅ 全テスト完了")
        print("📊 結果確認:")
        print("  - 左右のタイヤが同じ方向に回転しましたか？")
        print("  - 速度を変えても同じ方向に回転しましたか？")
        print()
        print("❌ もし逆方向に回転している場合:")
        print("  1. モーターの配線を確認してください")
        print("  2. L298Nドライバーの接続を確認してください")
        print("  3. 必要に応じて配線を交換してください")
        
    except KeyboardInterrupt:
        print("\n⏹️ テストが中断されました")
    except Exception as e:
        print(f"❌ エラー: {e}")
        return 1
    finally:
        if 'motor_controller' in locals():
            motor_controller.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
