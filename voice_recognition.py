#!/usr/bin/env python3
"""
ラズパイ音声認識システム
マイク音声入力から音声認識まで
"""

import os
import sys
import time
import logging
import pyaudio
import numpy as np
import tempfile
import wave
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# 環境変数を読み込み
load_dotenv()

class VoiceRecognition:
    """音声認識クラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = self._setup_logging()
        
        # OpenAI API設定
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEYが設定されていません。.envファイルを確認してください。")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # 音声設定
        self.sample_rate = int(os.getenv('SAMPLE_RATE', '16000'))
        self.chunk_size = int(os.getenv('CHUNK_SIZE', '1024'))
        self.audio_threshold = int(os.getenv('AUDIO_THRESHOLD', '1000'))
        
        # 音声ストリーム
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        
        self.logger.info("音声認識システムを初期化しました")
    
    def _setup_logging(self):
        """ログ設定"""
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def start_recording(self, duration=5):
        """
        音声録音を開始
        
        Args:
            duration: 録音時間（秒）
        """
        self.logger.info(f"音声録音を開始します（{duration}秒間）")
        
        try:
            # 音声ストリームを開く
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            # 音声データを収集
            frames = []
            for _ in range(0, int(self.sample_rate / self.chunk_size * duration)):
                data = self.stream.read(self.chunk_size)
                frames.append(data)
            
            # ストリームを閉じる
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            
            # 音声データを結合
            audio_data = b''.join(frames)
            
            self.logger.info("音声録音が完了しました")
            return audio_data
            
        except Exception as e:
            self.logger.error(f"音声録音エラー: {e}")
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            raise
    
    def detect_speech(self, duration=3):
        """
        音声検出録音（音声が検出されるまで録音）
        
        Args:
            duration: 最大録音時間（秒）
        """
        self.logger.info("音声検出録音を開始します")
        
        try:
            # 音声ストリームを開く
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            frames = []
            silent_frames = 0
            max_silent_frames = int(self.sample_rate / self.chunk_size * 2)  # 2秒間の無音
            max_frames = int(self.sample_rate / self.chunk_size * duration)
            
            for i in range(max_frames):
                data = self.stream.read(self.chunk_size)
                frames.append(data)
                
                # 音声レベルをチェック
                audio_array = np.frombuffer(data, dtype=np.int16)
                max_amplitude = np.max(np.abs(audio_array))
                
                if max_amplitude > self.audio_threshold:
                    silent_frames = 0
                    self.logger.debug(f"音声検出: レベル={max_amplitude}")
                else:
                    silent_frames += 1
                
                # 無音が続いたら録音終了
                if silent_frames > max_silent_frames and len(frames) > int(self.sample_rate / self.chunk_size * 1):
                    self.logger.info("無音検出により録音を終了します")
                    break
            
            # ストリームを閉じる
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            
            # 音声データを結合
            audio_data = b''.join(frames)
            
            self.logger.info(f"音声検出録音が完了しました（{len(frames)}フレーム）")
            return audio_data
            
        except Exception as e:
            self.logger.error(f"音声検出録音エラー: {e}")
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            raise
    
    def transcribe_audio(self, audio_data):
        """
        音声データを文字起こし
        
        Args:
            audio_data: 音声データ（バイト）
            
        Returns:
            文字起こしされたテキスト
        """
        self.logger.info("音声を文字起こし中...")
        
        try:
            # 一時ファイルを作成
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                # WAVファイルとして保存
                with wave.open(temp_file.name, 'wb') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)  # 16bit
                    wav_file.setframerate(self.sample_rate)
                    wav_file.writeframes(audio_data)
                
                # OpenAI Whisper APIで文字起こし
                with open(temp_file.name, 'rb') as audio_file:
                    transcript = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="ja"
                    )
                
                # 一時ファイルを削除
                os.unlink(temp_file.name)
                
                result = transcript.text.strip()
                self.logger.info(f"文字起こし完了: {result}")
                return result
                
        except Exception as e:
            self.logger.error(f"文字起こしエラー: {e}")
            raise
    
    def cleanup(self):
        """リソースのクリーンアップ"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        self.logger.info("リソースをクリーンアップしました")


def main():
    """メイン関数"""
    print("🎤 ラズパイ音声認識システム")
    print("=" * 50)
    
    try:
        # 音声認識システムを初期化
        voice_recognition = VoiceRecognition()
        
        print("🎯 音声認識を開始します")
        print("💡 話しかけてください...")
        print("⏹️  Ctrl+C で終了")
        
        while True:
            try:
                # 音声検出録音
                print("\n🎤 音声を検出中...")
                audio_data = voice_recognition.detect_speech(duration=10)
                
                if len(audio_data) > 0:
                    # 文字起こし実行
                    result = voice_recognition.transcribe_audio(audio_data)
                    
                    if result:
                        print(f"📝 認識結果: {result}")
                    else:
                        print("❌ 音声が認識されませんでした")
                else:
                    print("❌ 音声が検出されませんでした")
                    
            except KeyboardInterrupt:
                print("\n🛑 終了します...")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")
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
