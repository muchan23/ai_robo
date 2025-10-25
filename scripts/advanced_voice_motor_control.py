#!/usr/bin/env python3
"""
高度な音声制御ロボットシステム
複数ステップの指示を解析し、LLMが柔軟にモーター制御計画を実行
"""

import sys
import os
import time
import logging

# プロジェクトルートをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.audio.voice_recognition import VoiceRecognition
from src.ai.advanced_motor_ai import AdvancedMotorAI
from src.motor.advanced_motor_controller import AdvancedMotorController

def main():
    """メイン関数"""
    print("🤖 高度な音声制御ロボットシステム")
    print("=" * 50)
    print("🎯 複数ステップの指示に対応した柔軟なロボット制御")
    print("💡 例: 'まっすぐ行って、右に曲がって'")
    print("💡 例: '左に回って、前に進んで、止まって'")
    print("=" * 50)
    
    try:
        # 各システムを初期化
        print("🔧 システムを初期化中...")
        
        # 音声認識システム
        voice_recognition = VoiceRecognition()
        print("✅ 音声認識システム初期化完了")
        
        # 高度なモーター制御AI
        advanced_ai = AdvancedMotorAI()
        print("✅ 高度なモーター制御AI初期化完了")
        
        # 高度なモーター制御システム
        advanced_controller = AdvancedMotorController()
        print("✅ 高度なモーター制御システム初期化完了")
        
        print("\n🎯 高度な音声制御ロボットを開始します")
        print("💡 複雑な音声指示をしてください")
        print("💡 例: 'まっすぐ行って、右に曲がって'")
        print("💡 例: '左に回って、前に進んで、止まって'")
        print("⏹️  Ctrl+C で終了")
        
        while True:
            try:
                # 音声を待機（音声が検出されるまで待機）
                print("\n🎤 音声を待機中...")
                audio_data = voice_recognition.wait_for_speech()
                
                if audio_data:
                    # 文字起こし実行
                    print("📝 文字起こし中...")
                    transcribed_text = voice_recognition.transcribe_audio(audio_data)
                    
                    if transcribed_text:
                        print(f"📝 認識結果: {transcribed_text}")
                        
                        # 高度なAI解析実行
                        print("🤖 高度なAI解析中...")
                        plan = advanced_ai.analyze_complex_command(transcribed_text)
                        print(f"🤖 解析結果: {plan['summary']}")
                        print(f"📊 総ステップ数: {plan['total_steps']}")
                        print(f"⏱️  推定時間: {plan['estimated_time']}秒")
                        
                        # 計画の妥当性を検証
                        if advanced_ai.validate_plan(plan):
                            # 実行計画を表示
                            print("\n🚗 実行計画:")
                            for i, step in enumerate(plan['plan'], 1):
                                print(f"  {i}. {step['action']} (速度:{step['speed']}%, 時間:{step['duration']}秒) - {step['description']}")
                            
                            # 実行確認
                            print("\n⏳ 計画を実行しますか？ (Enter: 実行, Ctrl+C: キャンセル)")
                            try:
                                input()
                            except KeyboardInterrupt:
                                print("❌ 実行をキャンセルしました")
                                continue
                            
                            # 高度なモーター制御実行
                            print("🚗 高度なモーター制御実行中...")
                            success = advanced_controller.execute_complex_plan(plan)
                            
                            if success:
                                print("✅ 高度なモーター制御完了")
                                
                                # 実行状態を表示
                                status = advanced_controller.get_execution_status()
                                print(f"📊 実行状態: 完了")
                            else:
                                print("❌ 高度なモーター制御に失敗しました")
                                voice_recognition.play_sound("error")
                        else:
                            print("❌ 無効な計画です")
                            voice_recognition.play_sound("error")
                        
                    else:
                        print("❌ 音声が認識されませんでした")
                        voice_recognition.play_sound("error")
                else:
                    print("❌ 音声が検出されませんでした")
                    voice_recognition.play_sound("error")
                    
            except KeyboardInterrupt:
                print("\n🛑 終了します...")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")
                voice_recognition.play_sound("error")
                continue
        
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return 1
    finally:
        # リソースのクリーンアップ
        if 'voice_recognition' in locals():
            voice_recognition.cleanup()
        if 'advanced_controller' in locals():
            advanced_controller.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
