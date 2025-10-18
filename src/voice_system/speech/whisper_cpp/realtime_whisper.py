#!/usr/bin/env python3
"""
Whisper.cppリアルタイム音声認識モジュール
マイクからの音声をリアルタイムで文字起こし
"""

import pyaudio
import logging
import threading
import time
import numpy as np
from typing import Optional, Callable
from .whisper_cpp_stt import WhisperCppSTT


class RealtimeWhisper:
    """リアルタイム音声認識クラス"""
    
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
        
        # WhisperCppSTTを初期化
        self.stt = WhisperCppSTT(model_size=model_size)
        
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
            # WhisperCppSTTの内部メソッドを使用
            return self.stt._transcribe_audio_array(
                audio_array, 
                self.sample_rate, 
                "ja"
            )
        except Exception as e:
            self.logger.error(f"音声チャンク文字起こしエラー: {e}")
            return ""


def main():
    """テスト用のメイン関数"""
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🎤 Whisper.cppリアルタイム音声認識テスト")
    print("=" * 50)
    print("💡 注意: このファイルを直接実行する場合は、プロジェクトルートから実行してください")
    print("   推奨: python test_realtime_mic.py")
    
    def on_transcription(text: str):
        print(f"🎤 認識結果: {text}")
    
    def on_error(error: Exception):
        print(f"❌ エラー: {error}")
    
    try:
        # RealtimeWhisperインスタンスを作成
        realtime_whisper = RealtimeWhisper(model_size="small")
        
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
            
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    # プロジェクトルートをパスに追加
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))
    
    exit(main())
