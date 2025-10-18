#!/usr/bin/env python3
"""
音声認識システム（簡易版）
インポートエラーを回避した独立版
"""

import os
import sys
import time
import logging
import pyaudio
import numpy as np
import tempfile
import wave
import pygame
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
        
        # 音声合図用
        pygame.mixer.init()
        
        self.logger.info("音声認識システムを初期化しました")
    
    def _setup_logging(self):
        """ログ設定"""
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def play_sound(self, sound_type="start"):
        """
        音声合図を再生
        
        Args:
            sound_type: 音声の種類 ("start", "end", "error")
        """
        try:
            if sound_type == "start":
                # 開始音（ビープ音）
                frequency = 800
                duration = 0.2
            elif sound_type == "end":
                # 終了音（ビープ音）
                frequency = 600
                duration = 0.3
            elif sound_type == "error":
                # エラー音（ビープ音）
                frequency = 400
                duration = 0.5
            else:
                return
            
            # ビープ音を生成
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = np.zeros(frames)
            
            for i in range(frames):
                arr[i] = np.sin(2 * np.pi * frequency * i / sample_rate)
            
            # 音声を再生
            sound = pygame.sndarray.make_sound((arr * 32767).astype(np.int16))
            sound.play()
            pygame.time.wait(int(duration * 1000))
            
        except Exception as e:
            self.logger.warning(f"音声合図の再生に失敗: {e}")
    
    def wait_for_speech(self):
        """
        音声を待機（音声が検出されるまで待機）
        
        Returns:
            音声データ（バイト）
        """
        self.logger.info("音声を待機中...")
        print("🎤 音声を待機中... (話しかけてください)")
        
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
            speech_detected = False
            speech_started = False
            silent_frames = 0
            max_silent_frames = int(self.sample_rate / self.chunk_size * 1.5)  # 1.5秒間の無音
            
            while True:
                data = self.stream.read(self.chunk_size)
                audio_array = np.frombuffer(data, dtype=np.int16)
                max_amplitude = np.max(np.abs(audio_array))
                
                # 音声検出
                if max_amplitude > self.audio_threshold:
                    if not speech_started:
                        print("🎤 音声を検出しました！録音開始...")
                        self.play_sound("start")
                        speech_started = True
                        speech_detected = True
                    
                    frames.append(data)
                    silent_frames = 0
                    self.logger.debug(f"音声検出: レベル={max_amplitude}")
                else:
                    if speech_started:
                        silent_frames += 1
                        frames.append(data)  # 無音部分も録音
                        
                        # 無音が続いたら録音終了
                        if silent_frames > max_silent_frames:
                            print("🎤 音声録音完了")
                            self.play_sound("end")
                            break
                    else:
                        # 音声が検出される前は無音をスキップ
                        continue
            
            # ストリームを閉じる
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            
            if not speech_detected:
                self.logger.warning("音声が検出されませんでした")
                return None
            
            # 音声データを結合
            audio_data = b''.join(frames)
            self.logger.info(f"音声録音が完了しました（{len(frames)}フレーム）")
            return audio_data
            
        except Exception as e:
            self.logger.error(f"音声待機エラー: {e}")
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
