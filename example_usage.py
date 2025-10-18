#!/usr/bin/env python3
"""
音声文字起こしの使用例
"""

import sys
import logging
from pathlib import Path

# プロジェクトのsrcディレクトリをパスに追加
sys.path.append(str(Path(__file__).parent / 'src'))

from src.voice_system.speech.recognition import SpeechToText
from src.config import get_config


def main():
    """使用例のメイン関数"""
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # 設定を読み込み
        config = get_config()
        config.setup_logging()
        
        # 設定の妥当性をチェック
        if not config.validate():
            print("設定に問題があります。.envファイルを確認してください。")
            return 1
        
        # SpeechToTextインスタンスを作成
        stt = SpeechToText(api_key=config.openai_api_key)
        
        print("=== 音声文字起こしシステム ===")
        print("使用方法:")
        print("1. 音声ファイルのパスを入力してください")
        print("2. 言語を指定する場合は、言語コードを入力してください（例: ja, en）")
        print("3. 'quit' と入力すると終了します")
        print()
        
        while True:
            # 音声ファイルのパスを取得
            audio_file = input("音声ファイルのパス: ").strip()
            
            if audio_file.lower() == 'quit':
                print("終了します。")
                break
            
            if not audio_file:
                print("ファイルパスを入力してください。")
                continue
            
            # ファイルの存在確認
            if not Path(audio_file).exists():
                print(f"ファイルが見つかりません: {audio_file}")
                continue
            
            # 言語の指定（オプション）
            language = input("言語コード（オプション、例: ja, en）: ").strip()
            if not language:
                language = None
            
            try:
                # 文字起こし実行
                print("文字起こし中...")
                result = stt.transcribe_audio_file(
                    audio_file_path=audio_file,
                    language=language
                )
                
                print(f"\n文字起こし結果:")
                print(f"'{result}'\n")
                
            except Exception as e:
                print(f"エラーが発生しました: {e}\n")
    
    except KeyboardInterrupt:
        print("\n\n中断されました。")
        return 1
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
