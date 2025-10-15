#!/usr/bin/env python3
"""
設定管理モジュール
環境変数と設定ファイルの管理を行う
"""

import os
import logging
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """設定管理クラス"""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        初期化
        
        Args:
            env_file: .envファイルのパス。Noneの場合は自動検出
        """
        # .envファイルを読み込み
        if env_file:
            env_path = Path(env_file)
        else:
            # プロジェクトルートから.envファイルを探す
            current_dir = Path(__file__).parent
            project_root = current_dir.parent
            env_path = project_root / '.env'
        
        if env_path.exists():
            load_dotenv(env_path)
            logging.info(f"環境変数ファイルを読み込みました: {env_path}")
        else:
            logging.warning(f"環境変数ファイルが見つかりません: {env_path}")
        
        # OpenAI API設定
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            logging.warning("OPENAI_API_KEYが設定されていません")
        
        # 音声認識設定
        self.whisper_model = os.getenv('WHISPER_MODEL', 'whisper-1')
        self.default_language = os.getenv('DEFAULT_LANGUAGE', 'ja')
        
        # AI対話設定
        self.chat_model = os.getenv('CHAT_MODEL', 'gpt-4o-mini')
        self.tts_voice = os.getenv('TTS_VOICE', 'alloy')
        self.tts_model = os.getenv('TTS_MODEL', 'tts-1')
        
        # ログ設定
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_format = os.getenv('LOG_FORMAT', 
                                  '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # 音声デバイス設定
        self.audio_input_device = os.getenv('AUDIO_INPUT_DEVICE', 'default')
        self.audio_output_device = os.getenv('AUDIO_OUTPUT_DEVICE', 'default')
        self.sample_rate = int(os.getenv('SAMPLE_RATE', '16000'))
        self.chunk_size = int(os.getenv('CHUNK_SIZE', '1024'))
        
        # パフォーマンス設定
        self.max_audio_duration = int(os.getenv('MAX_AUDIO_DURATION', '30'))
        self.timeout_seconds = int(os.getenv('TIMEOUT_SECONDS', '10'))
    
    def validate(self) -> bool:
        """
        設定の妥当性をチェックする
        
        Returns:
            設定が有効な場合True
        """
        if not self.openai_api_key:
            logging.error("OpenAI APIキーが設定されていません")
            return False
        
        if self.sample_rate <= 0:
            logging.error("サンプルレートが無効です")
            return False
        
        if self.chunk_size <= 0:
            logging.error("チャンクサイズが無効です")
            return False
        
        if self.max_audio_duration <= 0:
            logging.error("最大録音時間が無効です")
            return False
        
        logging.info("設定の妥当性チェック完了")
        return True
    
    def setup_logging(self):
        """ログ設定を適用する"""
        log_level = getattr(logging, self.log_level.upper(), logging.INFO)
        
        logging.basicConfig(
            level=log_level,
            format=self.log_format,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('ai_robo.log', encoding='utf-8')
            ]
        )
        
        logging.info(f"ログ設定を適用しました: レベル={self.log_level}")
    
    def get_audio_config(self) -> dict:
        """
        音声設定を辞書で取得する
        
        Returns:
            音声設定の辞書
        """
        return {
            'input_device': self.audio_input_device,
            'output_device': self.audio_output_device,
            'sample_rate': self.sample_rate,
            'chunk_size': self.chunk_size,
            'max_duration': self.max_audio_duration
        }
    
    def get_openai_config(self) -> dict:
        """
        OpenAI設定を辞書で取得する
        
        Returns:
            OpenAI設定の辞書
        """
        return {
            'api_key': self.openai_api_key,
            'whisper_model': self.whisper_model,
            'chat_model': self.chat_model,
            'tts_voice': self.tts_voice,
            'tts_model': self.tts_model,
            'language': self.default_language,
            'timeout': self.timeout_seconds
        }


# グローバル設定インスタンス
config = Config()


def get_config() -> Config:
    """
    グローバル設定インスタンスを取得する
    
    Returns:
        Configインスタンス
    """
    return config
