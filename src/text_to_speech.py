#!/usr/bin/env python3
"""
音声合成モジュール
テキストを音声に変換してスピーカーから出力する
"""

import os
import logging
import tempfile
from typing import Optional, Union
from pathlib import Path
import openai
from openai import OpenAI


class TextToSpeech:
    """音声合成クラス"""
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 voice: str = "alloy",
                 model: str = "tts-1",
                 output_device_index: Optional[int] = None):
        """
        初期化
        
        Args:
            api_key: OpenAI APIキー。Noneの場合は環境変数OPENAI_API_KEYを使用
            voice: 音声の種類（alloy, echo, fable, onyx, nova, shimmer）
            model: 使用するTTSモデル（tts-1, tts-1-hd）
            output_device_index: 出力デバイスのインデックス
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI APIキーが設定されていません。環境変数OPENAI_API_KEYを設定するか、api_key引数を指定してください。")
        
        self.client = OpenAI(api_key=self.api_key)
        self.voice = voice
        self.model = model
        self.output_device_index = output_device_index
        self.logger = logging.getLogger(__name__)
        
        # 利用可能な音声を表示
        self._show_available_voices()
    
    def _show_available_voices(self):
        """利用可能な音声を表示"""
        voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        self.logger.info(f"利用可能な音声: {', '.join(voices)}")
        self.logger.info(f"現在の音声: {self.voice}")
    
    def speak_text(self, text: str, 
                   output_path: Optional[str] = None,
                   play_audio: bool = True) -> str:
        """
        テキストを音声に変換して再生する
        
        Args:
            text: 音声化するテキスト
            output_path: 音声ファイルの保存パス。Noneの場合は一時ファイル
            play_audio: 音声を再生するかどうか
            
        Returns:
            生成された音声ファイルのパス
            
        Raises:
            openai.OpenAIError: API呼び出しでエラーが発生した場合
        """
        if not text.strip():
            self.logger.warning("空のテキストが渡されました")
            return ""
        
        self.logger.info(f"音声合成開始: {text[:50]}...")
        
        try:
            # 音声ファイルのパスを決定
            if output_path is None:
                # 一時ファイルを作成
                temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
                output_path = temp_file.name
                temp_file.close()
            
            # OpenAI TTS APIを呼び出し
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text
            )
            
            # 音声データをファイルに保存
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            self.logger.info(f"音声合成完了: {output_path}")
            
            # 音声を再生
            if play_audio:
                self._play_audio(output_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"音声合成エラー: {e}")
            raise
    
    def _play_audio(self, audio_path: str):
        """
        音声ファイルを再生する
        
        Args:
            audio_path: 再生する音声ファイルのパス
        """
        try:
            # ファイル拡張子に応じて再生方法を選択
            audio_path = Path(audio_path)
            
            if audio_path.suffix.lower() == '.mp3':
                # MP3ファイルの場合
                self._play_mp3(audio_path)
            else:
                # その他の場合はpygameを使用
                self._play_with_pygame(audio_path)
                
        except Exception as e:
            self.logger.error(f"音声再生エラー: {e}")
            # フォールバック: システムコマンドを使用
            self._play_with_system_command(audio_path)
    
    def _play_mp3(self, audio_path: Path):
        """MP3ファイルを再生（mpg123を使用）"""
        import subprocess
        
        try:
            # mpg123がインストールされているかチェック
            subprocess.run(['which', 'mpg123'], check=True, capture_output=True)
            
            # mpg123で再生
            cmd = ['mpg123', '-q', str(audio_path)]
            if self.output_device_index is not None:
                cmd.extend(['-a', str(self.output_device_index)])
            
            subprocess.run(cmd, check=True)
            self.logger.info("音声再生完了（mpg123）")
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            # mpg123がない場合は他の方法を試す
            self._play_with_pygame(audio_path)
    
    def _play_with_pygame(self, audio_path: Path):
        """pygameを使用して音声を再生"""
        try:
            import pygame
            
            # pygameを初期化
            pygame.mixer.init()
            
            # 音声ファイルを読み込み
            pygame.mixer.music.load(str(audio_path))
            
            # 再生
            pygame.mixer.music.play()
            
            # 再生完了まで待機
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            self.logger.info("音声再生完了（pygame）")
            
        except ImportError:
            self.logger.warning("pygameがインストールされていません。システムコマンドを使用します。")
            self._play_with_system_command(audio_path)
        except Exception as e:
            self.logger.error(f"pygame再生エラー: {e}")
            self._play_with_system_command(audio_path)
    
    def _play_with_system_command(self, audio_path: Path):
        """システムコマンドを使用して音声を再生"""
        import subprocess
        import platform
        
        try:
            system = platform.system().lower()
            
            if system == "linux":
                # Linux（ラズパイ）の場合
                commands = [
                    ['aplay', str(audio_path)],  # ALSA
                    ['paplay', str(audio_path)],  # PulseAudio
                    ['mpv', str(audio_path)],     # mpv
                    ['vlc', str(audio_path)]      # VLC
                ]
            elif system == "darwin":
                # macOSの場合
                commands = [
                    ['afplay', str(audio_path)]
                ]
            elif system == "windows":
                # Windowsの場合
                commands = [
                    ['powershell', '-c', f'(New-Object Media.SoundPlayer "{audio_path}").PlaySync()']
                ]
            else:
                self.logger.error(f"サポートされていないOS: {system}")
                return
            
            # 利用可能なコマンドを試す
            for cmd in commands:
                try:
                    subprocess.run(cmd, check=True, capture_output=True)
                    self.logger.info(f"音声再生完了（{cmd[0]}）")
                    return
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            self.logger.error("音声再生に失敗しました。適切なプレイヤーがインストールされていません。")
            
        except Exception as e:
            self.logger.error(f"システムコマンド再生エラー: {e}")
    
    def set_voice(self, voice: str):
        """
        音声の種類を変更する
        
        Args:
            voice: 新しい音声の種類
        """
        valid_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        if voice not in valid_voices:
            raise ValueError(f"無効な音声です。利用可能な音声: {valid_voices}")
        
        self.voice = voice
        self.logger.info(f"音声を変更しました: {voice}")
    
    def set_model(self, model: str):
        """
        TTSモデルを変更する
        
        Args:
            model: 新しいTTSモデル
        """
        valid_models = ["tts-1", "tts-1-hd"]
        if model not in valid_models:
            raise ValueError(f"無効なモデルです。利用可能なモデル: {valid_models}")
        
        self.model = model
        self.logger.info(f"TTSモデルを変更しました: {model}")


def main():
    """テスト用のメイン関数"""
    import argparse
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='音声合成テスト')
    parser.add_argument('text', help='音声化するテキスト')
    parser.add_argument('--voice', default='alloy', help='音声の種類')
    parser.add_argument('--model', default='tts-1', help='TTSモデル')
    parser.add_argument('--output', help='出力ファイルパス')
    parser.add_argument('--no-play', action='store_true', help='音声を再生しない')
    
    args = parser.parse_args()
    
    try:
        # TextToSpeechインスタンスを作成
        tts = TextToSpeech(voice=args.voice, model=args.model)
        
        # 音声合成実行
        output_path = tts.speak_text(
            text=args.text,
            output_path=args.output,
            play_audio=not args.no_play
        )
        
        print(f"音声合成完了: {output_path}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
