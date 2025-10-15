#!/usr/bin/env python3
"""
音声文字起こしモジュール
OpenAI Whisper APIを使用して音声をテキストに変換する
"""

import os
import logging
from typing import Optional, Union
from pathlib import Path
import openai
from openai import OpenAI


class SpeechToText:
    """音声文字起こしクラス"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初期化
        
        Args:
            api_key: OpenAI APIキー。Noneの場合は環境変数OPENAI_API_KEYを使用
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI APIキーが設定されていません。環境変数OPENAI_API_KEYを設定するか、api_key引数を指定してください。")
        
        self.client = OpenAI(api_key=self.api_key)
        self.logger = logging.getLogger(__name__)
        
    def transcribe_audio_file(self, audio_file_path: Union[str, Path], 
                            model: str = "whisper-1", 
                            language: Optional[str] = None,
                            prompt: Optional[str] = None) -> str:
        """
        音声ファイルを文字起こしする
        
        Args:
            audio_file_path: 音声ファイルのパス
            model: 使用するWhisperモデル（デフォルト: whisper-1）
            language: 音声の言語コード（例: 'ja', 'en'）。Noneの場合は自動検出
            prompt: コンテキストを提供するプロンプト（オプション）
            
        Returns:
            文字起こしされたテキスト
            
        Raises:
            FileNotFoundError: 音声ファイルが見つからない場合
            openai.OpenAIError: API呼び出しでエラーが発生した場合
        """
        audio_path = Path(audio_file_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"音声ファイルが見つかりません: {audio_path}")
        
        self.logger.info(f"音声ファイルを文字起こし中: {audio_path}")
        
        try:
            with open(audio_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=model,
                    file=audio_file,
                    language=language,
                    prompt=prompt
                )
            
            result = transcript.text
            self.logger.info(f"文字起こし完了: {result[:50]}...")
            return result
            
        except openai.OpenAIError as e:
            self.logger.error(f"OpenAI API エラー: {e}")
            raise
        except Exception as e:
            self.logger.error(f"予期しないエラー: {e}")
            raise
    
    def transcribe_audio_data(self, audio_data: bytes,
                            filename: str = "audio.wav",
                            model: str = "whisper-1",
                            language: Optional[str] = None,
                            prompt: Optional[str] = None) -> str:
        """
        音声データ（バイト）を文字起こしする
        
        Args:
            audio_data: 音声データのバイト列
            filename: ファイル名（APIに送信する際の識別用）
            model: 使用するWhisperモデル（デフォルト: whisper-1）
            language: 音声の言語コード（例: 'ja', 'en'）。Noneの場合は自動検出
            prompt: コンテキストを提供するプロンプト（オプション）
            
        Returns:
            文字起こしされたテキスト
            
        Raises:
            openai.OpenAIError: API呼び出しでエラーが発生した場合
        """
        self.logger.info("音声データを文字起こし中...")
        
        try:
            # バイトデータをファイルライクオブジェクトとして扱う
            import io
            audio_file = io.BytesIO(audio_data)
            audio_file.name = filename
            
            transcript = self.client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                language=language,
                prompt=prompt
            )
            
            result = transcript.text
            self.logger.info(f"文字起こし完了: {result[:50]}...")
            return result
            
        except openai.OpenAIError as e:
            self.logger.error(f"OpenAI API エラー: {e}")
            raise
        except Exception as e:
            self.logger.error(f"予期しないエラー: {e}")
            raise


def main():
    """テスト用のメイン関数"""
    import argparse
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='音声ファイルを文字起こしする')
    parser.add_argument('audio_file', help='文字起こしする音声ファイルのパス')
    parser.add_argument('--language', help='音声の言語コード（例: ja, en）')
    parser.add_argument('--prompt', help='コンテキストを提供するプロンプト')
    parser.add_argument('--model', default='whisper-1', help='使用するWhisperモデル')
    
    args = parser.parse_args()
    
    try:
        # SpeechToTextインスタンスを作成
        stt = SpeechToText()
        
        # 文字起こし実行
        result = stt.transcribe_audio_file(
            audio_file_path=args.audio_file,
            model=args.model,
            language=args.language,
            prompt=args.prompt
        )
        
        print(f"文字起こし結果: {result}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
