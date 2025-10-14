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
│   ├── main.py             # メイン実行ファイル
│   ├── audio/              # 音声処理モジュール
│   │   ├── __init__.py
│   │   ├── recorder.py     # 音声録音
│   │   ├── player.py       # 音声再生
│   │   └── processor.py    # 音声前処理
│   ├── speech/             # 音声認識・合成モジュール
│   │   ├── __init__.py
│   │   ├── recognition.py  # OpenAI Whisper API
│   │   ├── synthesis.py    # 音声合成
│   │   └── conversation.py # 対話処理
│   ├── robot/              # ロボット制御モジュール（将来）
│   │   ├── __init__.py
│   │   ├── controller.py   # ハードウェア制御
│   │   └── sensors.py      # センサー制御
│   └── utils/              # ユーティリティ
│       ├── __init__.py
│       ├── config.py       # 設定管理
│       ├── logger.py       # ログ管理
│       └── helpers.py      # ヘルパー関数
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

### src/audio/
音声の入出力と前処理を担当
- **recorder.py**: マイクからの音声録音
- **player.py**: スピーカーへの音声再生
- **processor.py**: ノイズ除去、音量調整等

### src/speech/
音声認識と音声合成を担当
- **recognition.py**: OpenAI Whisper API連携
- **synthesis.py**: テキストから音声への変換
- **conversation.py**: 対話ロジックの処理

### src/robot/
ロボットのハードウェア制御を担当（将来実装）
- **controller.py**: モーター、センサー制御
- **sensors.py**: 環境センサーの読み取り

### src/utils/
共通のユーティリティ機能
- **config.py**: 設定ファイルの読み込み
- **logger.py**: ログ出力の管理
- **helpers.py**: 共通のヘルパー関数

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
