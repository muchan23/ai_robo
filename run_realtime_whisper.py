#!/usr/bin/env python3
"""
ラズパイ用Whisper.cppリアルタイム音声認識実行スクリプト
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

# 環境変数を設定（ラズパイ用）
os.environ['PYTHONPATH'] = f"{project_root}:{project_root / 'src'}:{os.environ.get('PYTHONPATH', '')}"

# メインスクリプトを実行
if __name__ == "__main__":
    # モジュールとして実行
    import subprocess
    import sys
    
    try:
        # プロジェクトルートからモジュールを実行
        result = subprocess.run([
            sys.executable, '-m', 'src.voice_system.speech.whisper_cpp.realtime_whisper'
        ], cwd=str(project_root))
        sys.exit(result.returncode)
    except Exception as e:
        print(f"❌ 実行エラー: {e}")
        print("💡 代替方法:")
        print("   python test_realtime_mic.py")
        sys.exit(1)
