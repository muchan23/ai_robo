#!/usr/bin/env python3
"""
ラズパイ音声対話システム - メインスクリプト
統合された音声対話システムのエントリーポイント
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 音声認識システムをインポート
from src.audio.voice_recognition import VoiceRecognition

def main():
    """メイン関数"""
    print("🎤 ラズパイ音声対話システム")
    print("=" * 50)
    
    try:
        # 音声認識システムを初期化
        voice_recognition = VoiceRecognition()
        
        print("🎯 音声対話を開始します")
        print("💡 話しかけてください...")
        print("⏹️  Ctrl+C で終了")
        
        while True:
            try:
                # 音声を待機（音声が検出されるまで待機）
                audio_data = voice_recognition.wait_for_speech()
                
                if audio_data:
                    # 文字起こし実行
                    print("📝 文字起こし中...")
                    transcribed_text = voice_recognition.transcribe_audio(audio_data)
                    
                    if transcribed_text:
                        print(f"📝 認識結果: {transcribed_text}")
                        
                        # AI対話実行
                        print("🤖 AI応答を生成中...")
                        ai_response = voice_recognition.ai_chat.chat(transcribed_text)
                        print(f"🤖 AI応答: {ai_response}")
                        
                        # 音声合成・再生
                        print("🔊 音声合成中...")
                        voice_recognition.tts.speak_text(ai_response)
                        print("✅ 音声再生完了")
                        
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
        if 'voice_recognition' in locals():
            voice_recognition.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
