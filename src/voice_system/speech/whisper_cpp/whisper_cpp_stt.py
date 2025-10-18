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
            
            # セグメントを結合してテキストを作成
            text_parts = []
            for segment in segments:
                text_parts.append(segment.text.strip())
            
            result = " ".join(text_parts)
            
            self.logger.info(f"文字起こし完了: {result[:50]}...")
            return result
            
        except Exception as e:
            self.logger.error(f"文字起こしエラー: {e}")
            raise
    
    
    def transcribe_audio_data(self, audio_data: bytes,
                            sample_rate: int = 16000,
                            channels: int = 1) -> str:
        """
        音声データ（バイト）を文字起こしする
        
        Args:
            audio_data: 音声データのバイト列
            sample_rate: サンプルレート
            channels: チャンネル数
            
        Returns:
            文字起こしされたテキスト
        """
        self.logger.info("音声データを文字起こし中...")
        
        try:
            # 一時ファイルを作成
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                # WAVファイルとして保存
                with wave.open(temp_file.name, 'wb') as wav_file:
                    wav_file.setnchannels(channels)
                    wav_file.setsampwidth(2)  # 16bit
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(audio_data)
                
                # 文字起こし実行
                result = self.transcribe_audio_file(temp_file.name)
                
                # 一時ファイルを削除
                os.unlink(temp_file.name)
                
                return result
                
        except Exception as e:
            self.logger.error(f"音声データ文字起こしエラー: {e}")
            raise
    
    
    def get_model_info(self) -> dict:
        """
        モデル情報を取得する
        
        Returns:
            モデル情報の辞書
        """
        return {
            "model_size": self.model_size,
            "available": FASTER_WHISPER_AVAILABLE,
            "device": "cpu",
            "compute_type": "int8"
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
    parser.add_argument('--model-size', default='small', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='モデルサイズ')
    
    args = parser.parse_args()
    
    try:
        # WhisperCppSTTインスタンスを作成
        stt = WhisperCppSTT(model_size=args.model_size)
        
        # 文字起こし実行
        result = stt.transcribe_audio_file(args.audio_file)
        
        print(f"文字起こし結果: {result}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
