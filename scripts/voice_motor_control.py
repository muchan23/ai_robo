#!/usr/bin/env python3
"""
音声制御ロボットシステム
音声認識 + AI解釈 + モーター制御の統合システム
"""

import sys
import os
import time
import logging

# プロジェクトルートをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.audio.voice_recognition import VoiceRecognition
from src.ai.motor_ai_chat import MotorAIChat
from src.motor.motor_controller import MotorController

def main():
    """メイン関数"""
    print("🤖 音声制御ロボットシステム")
    print("=" * 50)
    
    try:
        # 各システムを初期化
        print("🔧 システムを初期化中...")
        
        # 音声認識システム
        voice_recognition = VoiceRecognition()
        print("✅ 音声認識システム初期化完了")
        
        # モーター制御AI
        motor_ai = MotorAIChat()
        print("✅ モーター制御AI初期化完了")
        
        # モーター制御システム
        motor_controller = MotorController()
        print("✅ モーター制御システム初期化完了")
        
        print("\n🎯 音声制御ロボットを開始します")
        print("💡 音声で指示してください（例：前に進んで、右に回って、止まって）")
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
                        
                        # AI解釈実行
                        print("🤖 AI解釈中...")
                        command = motor_ai.interpret_command(transcribed_text)
                        print(f"🤖 解釈結果: {command['message']}")
                        
                        # コマンドの妥当性を検証
                        if motor_ai.validate_command(command):
                            # モーター制御実行
                            print("🚗 モーター制御実行中...")
                            motor_controller.execute_command(command)
                            print("✅ モーター制御完了")
                        else:
                            print("❌ 無効なコマンドです")
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
        if 'motor_controller' in locals():
            motor_controller.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
