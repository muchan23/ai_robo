#!/usr/bin/env python3
"""
音声録音モジュール
ラズパイのマイクから音声を録音する
"""

import pyaudio
import wave
import logging
import threading
import time
from typing import Optional, Callable
from pathlib import Path


class AudioRecorder:
    """音声録音クラス"""
    
    def __init__(self, 
                 sample_rate: int = 16000,
                 chunk_size: int = 1024,
                 channels: int = 1,
                 format: int = pyaudio.paInt16,
                 input_device_index: Optional[int] = None):
        """
        初期化
        
        Args:
            sample_rate: サンプルレート（Hz）
            chunk_size: チャンクサイズ
            channels: チャンネル数（1=モノラル, 2=ステレオ）
            format: 音声フォーマット
            input_device_index: 入力デバイスのインデックス
        """
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.format = format
        self.input_device_index = input_device_index
        
        self.audio = pyaudio.PyAudio()
        self.logger = logging.getLogger(__name__)
        self.is_recording = False
        self.recording_thread = None
        
        # 音声デバイス情報を表示
        self._show_audio_devices()
    
    def _show_audio_devices(self):
        """利用可能な音声デバイスを表示"""
        self.logger.info("利用可能な音声デバイス:")
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                self.logger.info(f"  {i}: {info['name']} (入力チャンネル: {info['maxInputChannels']})")
    
    def record_audio(self, duration: float, output_path: str) -> bool:
        """
        指定時間音声を録音する
        
        Args:
            duration: 録音時間（秒）
            output_path: 出力ファイルパス
            
        Returns:
            録音成功の場合True
        """
        try:
            self.logger.info(f"音声録音開始: {duration}秒")
            
            # 音声ストリームを開く
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.input_device_index,
                frames_per_buffer=self.chunk_size
            )
            
            frames = []
            
            # 録音実行
            for _ in range(0, int(self.sample_rate / self.chunk_size * duration)):
                data = stream.read(self.chunk_size)
                frames.append(data)
            
            # ストリームを閉じる
            stream.stop_stream()
            stream.close()
            
            # WAVファイルとして保存
            with wave.open(output_path, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(frames))
            
            self.logger.info(f"音声録音完了: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"音声録音エラー: {e}")
            return False
    
    def start_continuous_recording(self, 
                                 output_dir: str = "recordings",
                                 max_duration: float = 30.0,
                                 silence_threshold: float = 0.01,
                                 silence_duration: float = 2.0,
                                 callback: Optional[Callable[[str], None]] = None):
        """
        連続録音を開始する（音声検出による自動録音）
        
        Args:
            output_dir: 録音ファイルの保存ディレクトリ
            max_duration: 最大録音時間（秒）
            silence_threshold: 無音判定の閾値
            silence_duration: 無音継続時間（秒）
            callback: 録音完了時のコールバック関数
        """
        if self.is_recording:
            self.logger.warning("既に録音中です")
            return
        
        self.is_recording = True
        self.recording_thread = threading.Thread(
            target=self._continuous_recording_worker,
            args=(output_dir, max_duration, silence_threshold, silence_duration, callback)
        )
        self.recording_thread.start()
        self.logger.info("連続録音を開始しました")
    
    def stop_continuous_recording(self):
        """連続録音を停止する"""
        if not self.is_recording:
            return
        
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join()
        self.logger.info("連続録音を停止しました")
    
    def _continuous_recording_worker(self, 
                                   output_dir: str,
                                   max_duration: float,
                                   silence_threshold: float,
                                   silence_duration: float,
                                   callback: Optional[Callable[[str], None]]):
        """連続録音のワーカースレッド"""
        try:
            # 出力ディレクトリを作成
            Path(output_dir).mkdir(exist_ok=True)
            
            # 音声ストリームを開く
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.input_device_index,
                frames_per_buffer=self.chunk_size
            )
            
            while self.is_recording:
                # 音声検出
                if self._detect_sound(stream, silence_threshold):
                    # 音声を検出したら録音開始
                    timestamp = int(time.time())
                    output_path = Path(output_dir) / f"recording_{timestamp}.wav"
                    
                    self.logger.info("音声を検出しました。録音開始...")
                    
                    # 録音実行
                    frames = []
                    silence_count = 0
                    max_silence_frames = int(silence_duration * self.sample_rate / self.chunk_size)
                    max_frames = int(max_duration * self.sample_rate / self.chunk_size)
                    
                    for frame_count in range(max_frames):
                        if not self.is_recording:
                            break
                        
                        data = stream.read(self.chunk_size)
                        frames.append(data)
                        
                        # 無音検出
                        if self._is_silence(data, silence_threshold):
                            silence_count += 1
                            if silence_count >= max_silence_frames:
                                self.logger.info("無音を検出しました。録音終了...")
                                break
                        else:
                            silence_count = 0
                    
                    # 録音時間が短すぎる場合はスキップ
                    if len(frames) < int(0.5 * self.sample_rate / self.chunk_size):
                        self.logger.info("録音時間が短すぎます。スキップします。")
                        continue
                    
                    # WAVファイルとして保存
                    with wave.open(str(output_path), 'wb') as wf:
                        wf.setnchannels(self.channels)
                        wf.setsampwidth(self.audio.get_sample_size(self.format))
                        wf.setframerate(self.sample_rate)
                        wf.writeframes(b''.join(frames))
                    
                    self.logger.info(f"録音完了: {output_path}")
                    
                    # コールバック実行
                    if callback:
                        callback(str(output_path))
                
                time.sleep(0.1)  # CPU使用率を下げる
            
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            self.logger.error(f"連続録音エラー: {e}")
    
    def _detect_sound(self, stream, threshold: float) -> bool:
        """音声を検出する"""
        try:
            data = stream.read(self.chunk_size, exception_on_overflow=False)
            return not self._is_silence(data, threshold)
        except:
            return False
    
    def _is_silence(self, data: bytes, threshold: float) -> bool:
        """データが無音かどうかを判定する"""
        import struct
        
        # 16bit PCMとして解析
        samples = struct.unpack(f'{len(data)//2}h', data)
        max_amplitude = max(abs(sample) for sample in samples)
        normalized_amplitude = max_amplitude / 32768.0  # 16bitの最大値で正規化
        
        return normalized_amplitude < threshold
    
    def __del__(self):
        """デストラクタ"""
        if hasattr(self, 'audio'):
            self.audio.terminate()


def main():
    """テスト用のメイン関数"""
    import argparse
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='音声録音テスト')
    parser.add_argument('--duration', type=float, default=5.0, help='録音時間（秒）')
    parser.add_argument('--output', default='test_recording.wav', help='出力ファイル名')
    parser.add_argument('--continuous', action='store_true', help='連続録音モード')
    
    args = parser.parse_args()
    
    try:
        recorder = AudioRecorder()
        
        if args.continuous:
            print("連続録音モード。Ctrl+Cで終了...")
            recorder.start_continuous_recording()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                recorder.stop_continuous_recording()
        else:
            success = recorder.record_audio(args.duration, args.output)
            if success:
                print(f"録音完了: {args.output}")
            else:
                print("録音に失敗しました")
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
