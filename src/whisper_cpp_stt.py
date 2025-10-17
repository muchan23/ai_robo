#!/usr/bin/env python3
"""
Whisper.cpp音声認識モジュール
ローカル環境で高速な音声認識を提供
"""

import os
import logging
import io
import wave
import tempfile
from typing import List, Optional, Union
from pathlib import Path

try:
    from faster_whisper import WhisperModel
    FASTER_WHISPER_AVAILABLE = True
except ImportError:
    FASTER_WHISPER_AVAILABLE = False
    WhisperModel = None


class WhisperCppSTT:
    """Whisper.cpp音声認識クラス"""
    
    def __init__(self, 
                 model_path: Optional[str] = None,
                 model_size: str = "small"):
        """
        初期化
        
        Args:
            model_path: モデルファイルのパス
            model_size: モデルサイズ（tiny, base, small, medium, large）
        """
        self.logger = logging.getLogger(__name__)
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
    
    
    def transcribe_audio_file(self, audio_file_path: Union[str, Path]) -> str:
        """
        音声ファイルを文字起こしする
        
        Args:
            audio_file_path: 音声ファイルのパス
            
        Returns:
            文字起こしされたテキスト
        """
        audio_path = Path(audio_file_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"音声ファイルが見つかりません: {audio_path}")
        
        self.logger.info(f"音声ファイルを文字起こし中: {audio_path}")
        
        try:
            # faster-whisperで文字起こし
            segments, info = self.whisper.transcribe(str(audio_path), language="ja")
            
            # 結果からテキストを抽出
            text = ""
            for segment in segments:
                text += segment.text
            
            self.logger.info(f"文字起こし完了: {text[:50]}...")
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"faster-whisper文字起こしエラー: {e}")
            raise
    
    def transcribe_audio_data(self, audio_frames: List[bytes], 
                            sample_rate: int = 16000,
                            channels: int = 1) -> str:
        """
        音声データ（バイト列）を文字起こしする
        
        Args:
            audio_frames: 音声フレームのリスト
            sample_rate: サンプルレート
            channels: チャンネル数
            
        Returns:
            文字起こしされたテキスト
        """
        self.logger.info("音声データを文字起こし中...")
        
        try:
            # メモリ内でWAVファイルを作成
            wav_buffer = self._create_wav_buffer(audio_frames, sample_rate, channels)
            
            # 一時ファイルに保存
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(wav_buffer.getvalue())
                temp_path = temp_file.name
            
            try:
                # faster-whisperで文字起こし
                segments, info = self.whisper.transcribe(temp_path, language="ja")
                
                # 結果からテキストを抽出
                text = ""
                for segment in segments:
                    text += segment.text
                
                self.logger.info(f"文字起こし完了: {text[:50]}...")
                return text.strip()
                
            finally:
                # 一時ファイルを削除
                try:
                    os.unlink(temp_path)
                except Exception as e:
                    self.logger.warning(f"一時ファイルの削除に失敗: {e}")
            
        except Exception as e:
            self.logger.error(f"faster-whisper文字起こしエラー: {e}")
            raise
    
    def _create_wav_buffer(self, audio_frames: List[bytes], 
                          sample_rate: int, channels: int) -> io.BytesIO:
        """音声フレームからWAVバッファを作成"""
        wav_buffer = io.BytesIO()
        
        with wave.open(wav_buffer, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 16bit
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(audio_frames))
        
        wav_buffer.seek(0)
        return wav_buffer
    
    def get_model_info(self) -> dict:
        """モデル情報を取得"""
        return {
            'model_size': self.model_size,
            'available': FASTER_WHISPER_AVAILABLE
        }


def main():
    """テスト用のメイン関数"""
    import argparse
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='Whisper.cpp音声認識テスト')
    parser.add_argument('audio_file', help='文字起こしする音声ファイルのパス')
    parser.add_argument('--model-size', default='small', help='モデルサイズ')
    parser.add_argument('--model-path', help='モデルファイルのパス')
    
    args = parser.parse_args()
    
    try:
        # WhisperCppSTTインスタンスを作成
        stt = WhisperCppSTT(
            model_path=args.model_path,
            model_size=args.model_size
        )
        
        # 文字起こし実行
        result = stt.transcribe_audio_file(args.audio_file)
        
        print(f"文字起こし結果: {result}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
