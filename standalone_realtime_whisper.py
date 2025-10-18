#!/usr/bin/env python3
"""
独立実行可能なWhisper.cppリアルタイム音声認識スクリプト
ラズパイ用
"""

import sys
import os
import logging
import threading
import time
import numpy as np
import pyaudio
import tempfile
import wave
from pathlib import Path
from typing import Optional, Callable

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

try:
    from faster_whisper import WhisperModel
    FASTER_WHISPER_AVAILABLE = True
except ImportError:
    FASTER_WHISPER_AVAILABLE = False
    WhisperModel = None


class StandaloneRealtimeWhisper:
    """独立実行可能なリアルタイム音声認識クラス"""
    
    def __init__(self, 
                 model_size: str = "small",
                 sample_rate: int = 16000,
                 chunk_size: int = 1024,
                 channels: int = 1):
        """
        初期化
        
        Args:
            model_size: モデルサイズ
            sample_rate: サンプルレート
            chunk_size: チャンクサイズ
            channels: チャンネル数
        """
        self.logger = logging.getLogger(__name__)
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.model_size = model_size
        
        if not FASTER_WHISPER_AVAILABLE:
            raise ImportError("faster-whisperがインストールされていません。pip install faster-whisper を実行してください。")
        
        # faster-whisperモデルを初期化
        try:
            self.whisper = WhisperModel(model_size, device="cpu", compute_type="int8")
            self.logger.info(f"faster-whisperモデル（{model_size}）の初期化が完了しました")
        except Exception as e:
            self.logger.error(f"faster-whisperモデルの初期化に失敗: {e}")
            raise
        
        # 音声ストリーム
        self.audio_stream = None
        self.is_recording = False
        self.recording_thread = None
        
        # コールバック関数
        self.on_transcription: Optional[Callable[[str], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
    
    def start_listening(self, 
                       on_transcription: Callable[[str], None],
                       on_error: Optional[Callable[[Exception], None]] = None):
        """
        音声認識を開始する
        
        Args:
            on_transcription: 文字起こし結果のコールバック関数
            on_error: エラーのコールバック関数
        """
        if self.is_recording:
            self.logger.warning("既に音声認識が動作中です")
            return
        
        self.on_transcription = on_transcription
        self.on_error = on_error
        
        try:
            # 音声ストリームを初期化
            self.audio_stream = pyaudio.PyAudio().open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            # 録音スレッドを開始
            self.is_recording = True
            self.recording_thread = threading.Thread(target=self._recording_loop)
            self.recording_thread.start()
            
            self.logger.info("リアルタイム音声認識を開始しました")
            
        except Exception as e:
            self.logger.error(f"音声認識開始エラー: {e}")
            if self.on_error:
                self.on_error(e)
            raise
    
    def stop_listening(self):
        """音声認識を停止する"""
        if not self.is_recording:
            return
        
        self.is_recording = False
        
        # 録音スレッドの終了を待機
        if self.recording_thread:
            self.recording_thread.join()
        
        # 音声ストリームを停止
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_stream = None
        
        self.logger.info("リアルタイム音声認識を停止しました")
    
    def _recording_loop(self):
        """録音ループ"""
        audio_buffer = []
        buffer_duration = 2.0  # 2秒間のバッファ
        buffer_size = int(self.sample_rate * buffer_duration)
        
        try:
            while self.is_recording:
                # 音声データを読み取り
                audio_data = self.audio_stream.read(self.chunk_size, exception_on_overflow=False)
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                
                # バッファに追加
                audio_buffer.extend(audio_array)
                
                # バッファが十分な長さになったら文字起こし
                if len(audio_buffer) >= buffer_size:
                    # バッファから音声データを取得
                    chunk_audio = np.array(audio_buffer[:buffer_size], dtype=np.int16)
                    audio_buffer = audio_buffer[buffer_size:]
                    
                    # 音声レベルをチェック（無音の場合はスキップ）
                    if np.max(np.abs(chunk_audio)) > 100:  # 閾値
                        # 文字起こし実行
                        result = self._transcribe_audio_chunk(chunk_audio)
                        
                        if result.strip() and self.on_transcription:
                            self.on_transcription(result)
                            
        except Exception as e:
            self.logger.error(f"録音ループエラー: {e}")
            if self.on_error:
                self.on_error(e)
    
    def _transcribe_audio_chunk(self, audio_array: np.ndarray) -> str:
        """
        音声チャンクを文字起こしする
        
        Args:
            audio_array: 音声データのnumpy配列
            
        Returns:
            文字起こしされたテキスト
        """
        try:
            # 一時ファイルを作成
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                # WAVファイルとして保存
                with wave.open(temp_file.name, 'wb') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)  # 16bit
                    wav_file.setframerate(self.sample_rate)
                    wav_file.writeframes(audio_array.tobytes())
                
                # 文字起こし実行
                segments, info = self.whisper.transcribe(temp_file.name, language="ja")
                
                # セグメントを結合
                text_parts = []
                for segment in segments:
                    text_parts.append(segment.text.strip())
                
                result = " ".join(text_parts)
                
                # 一時ファイルを削除
                os.unlink(temp_file.name)
                
                return result
                
        except Exception as e:
            self.logger.error(f"音声チャンク文字起こしエラー: {e}")
            return ""


def main():
    """メイン関数"""
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🎤 独立実行Whisper.cppリアルタイム音声認識")
    print("=" * 60)
    
    def on_transcription(text: str):
        print(f"🎤 認識結果: {text}")
    
    def on_error(error: Exception):
        print(f"❌ エラー: {error}")
    
    try:
        # StandaloneRealtimeWhisperインスタンスを作成
        print("📦 StandaloneRealtimeWhisperを初期化中...")
        realtime_whisper = StandaloneRealtimeWhisper(model_size="small")
        
        print("🎯 マイクからの音声認識を開始します")
        print("💡 話しかけてください...")
        print("⏹️  Ctrl+C で停止")
        
        # 音声認識を開始
        realtime_whisper.start_listening(
            on_transcription=on_transcription,
            on_error=on_error
        )
        
        # メインループ
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n🛑 停止中...")
            realtime_whisper.stop_listening()
            print("✅ テストを停止しました")
            
    except ImportError as e:
        print(f"❌ 依存関係エラー: {e}")
        print("💡 解決方法:")
        print("   pip install faster-whisper numpy pyaudio")
        return 1
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
