#!/usr/bin/env python3
"""
ラズパイ音声対話システム - GIF表示付きメインスクリプト
Tkinterのスレッド問題を回避した実装
"""

import sys
import os
import threading
import time
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 各モジュールを直接インポート
from src.ai.ai_chat import AIChat
from src.tts.tts_synthesis import TTSSynthesis
from src.audio.voice_recognition_simple import VoiceRecognition
from src.display.gif_player_ultra_simple import GIFPlayerUltraSimple

def run_voice_system(voice_recognition, ai_chat, tts):
    """音声システムを実行"""
    print("🎤 音声対話システムを開始します")
    
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
                    ai_response = ai_chat.chat(transcribed_text)
                    print(f"🤖 AI応答: {ai_response}")
                    
                    # 音声合成・再生
                    print("🔊 音声合成中...")
                    tts.speak_text(ai_response)
                    print("✅ 音声再生完了")
                    
                else:
                    print("❌ 音声が認識されませんでした")
                    voice_recognition.play_sound("error")
            else:
                print("❌ 音声が検出されませんでした")
                voice_recognition.play_sound("error")
                
        except KeyboardInterrupt:
            print("\n🛑 音声システムを終了します...")
            break
        except Exception as e:
            print(f"❌ 音声システムエラー: {e}")
            voice_recognition.play_sound("error")
            continue

def main():
    """メイン関数"""
    print("🎤 ラズパイ音声対話システム（GIF表示付き）")
    print("=" * 50)
    
    try:
        # 各システムを初期化
        voice_recognition = VoiceRecognition()
        ai_chat = AIChat()
        tts = TTSSynthesis()
        gif_player = GIFPlayerUltraSimple()
        
        print("🎯 音声対話を開始します")
        print("💡 話しかけてください...")
        print("⏹️  Ctrl+C で終了")
        
        # GIF表示を開始（音声対話開始時）
        print("🎬 GIF表示を開始します")
        gif_player.start_continuous_display()
        
        # 音声システムを別スレッドで実行
        voice_thread = threading.Thread(
            target=run_voice_system, 
            args=(voice_recognition, ai_chat, tts)
        )
        voice_thread.daemon = True
        voice_thread.start()
        
        # メインスレッドでウィンドウループを実行
        if gif_player.root:
            print("🎬 GIF表示ウィンドウを開始します")
            print("💡 操作方法:")
            print("   ESCキー: 終了")
            print("   F11キー: フルスクリーン切り替え")
            print("   スペースキー: GIF表示切り替え")
            print("   Hキー: GIF非表示")
            print("   Sキー: GIF表示")
            gif_player.root.mainloop()
        
        # 音声スレッドの終了を待機
        voice_thread.join()
        
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return 1
    finally:
        if 'voice_recognition' in locals():
            voice_recognition.cleanup()
        if 'tts' in locals():
            tts.cleanup()
        if 'gif_player' in locals():
            gif_player.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
