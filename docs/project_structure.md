# プロジェクト構造

## フォルダ構成

```
ai_robo/
├── README.md                 # プロジェクト概要
├── requirements.txt          # Python依存関係
├── .env.example             # 環境変数テンプレート
├── .gitignore               # Git除外設定
│
├── src/                     # ソースコード
│   ├── __init__.py
│   ├── config.py            # 設定管理モジュール
│   ├── voice_system/        # 音声システム（メイン）
│   │   ├── __init__.py
│   │   ├── conversation.py  # 統合会話システム
│   │   ├── audio/           # 音声処理関連
│   │   │   ├── __init__.py
│   │   │   └── recorder.py  # 音声録音
│   │   ├── speech/          # 音声認識・合成
│   │   │   ├── __init__.py
│   │   │   ├── recognition.py # OpenAI Whisper API
│   │   │   └── synthesis.py # 音声合成
│   │   └── ai/              # AI対話関連
│   │       ├── __init__.py
│   │       └── chat.py      # AI対話
│
├── config/                 # 設定ファイル
│   ├── audio_config.yaml   # 音声設定
│   ├── api_config.yaml     # API設定
│   └── robot_config.yaml   # ロボット設定（将来）
│
├── docs/                   # ドキュメント
│   ├── development_policy.md # 開発方針
│   ├── project_structure.md  # プロジェクト構造
│   ├── api_reference.md      # API仕様
│   └── user_guide.md         # ユーザーガイド
│
├── tests/                  # テストファイル
│   ├── __init__.py
│   ├── test_audio.py       # 音声処理テスト
│   ├── test_speech.py      # 音声認識テスト
│   └── test_integration.py # 統合テスト
│
├── scripts/                # スクリプト
│   ├── setup.sh           # 環境構築スクリプト
│   ├── install_deps.sh    # 依存関係インストール
│   └── test_hardware.py   # ハードウェアテスト
│
└── data/                   # データファイル
    ├── audio/              # 音声ファイル
    │   ├── input/          # 入力音声
    │   └── output/         # 出力音声
    ├── logs/               # ログファイル
    └── cache/              # キャッシュファイル
```

## モジュール説明

### src/voice_system/
音声システムのメインモジュール
- **conversation.py**: 統合会話システム（音声認識→AI対話→音声合成）

### src/voice_system/audio/
音声の入出力と前処理を担当
- **recorder.py**: マイクからの音声録音

### src/voice_system/speech/
音声認識と音声合成を担当
- **recognition.py**: OpenAI Whisper API連携
- **synthesis.py**: テキストから音声への変換

### src/voice_system/ai/
AI対話機能を担当
- **chat.py**: ChatGPT API連携と対話管理


## 設定ファイル

### config/audio_config.yaml
```yaml
microphone:
  device_id: 3
  sample_rate: 44100
  channels: 1
  chunk_size: 1024

speaker:
  device_id: 4
  sample_rate: 44100
  channels: 2

recording:
  duration: 5
  format: "wav"
  quality: "high"
```

### config/api_config.yaml
```yaml
openai:
  api_key: "${OPENAI_API_KEY}"
  model: "whisper-1"
  language: "ja"
  response_format: "text"

tts:
  engine: "pyttsx3"
  voice: "japanese"
  rate: 150
  volume: 0.8
```

## 環境変数

### .env.example
```bash
# OpenAI API設定
OPENAI_API_KEY=your_api_key_here

# 音声デバイス設定
MICROPHONE_DEVICE_ID=3
SPEAKER_DEVICE_ID=4

# ログ設定
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# その他設定
DEBUG_MODE=false
CACHE_ENABLED=true
```

## 開発時の注意点

### 1. 依存関係管理
- `requirements.txt`でPythonパッケージを管理
- 仮想環境の使用を推奨
- 定期的な依存関係の更新

### 2. 設定管理
- 機密情報は環境変数で管理
- 設定ファイルはYAML形式で統一
- デフォルト値の設定

### 3. ログ管理
- 適切なログレベルの設定
- ログファイルのローテーション
- 個人情報の除外

### 4. テスト
- 各モジュールの単体テスト
- 統合テストの実装
- ハードウェアテストの自動化

### 5. ドキュメント
- コードのdocstring記述
- API仕様の文書化
- ユーザーガイドの整備
