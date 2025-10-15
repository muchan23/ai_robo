# AI Robot プロジェクト

OpenAI Whisper APIを使用した自律型ロボット制御システムの開発プロジェクトです。

## 概要

このプロジェクトは、ラズパイで動作する音声認識システムを構築します。OpenAIのWhisper APIを使用して音声をテキストに変換し、将来的にはロボット制御との連携を予定しています。

## 機能

- **音声文字起こし**: OpenAI Whisper APIを使用した高精度な音声認識
- **設定管理**: 環境変数による柔軟な設定
- **エラーハンドリング**: 堅牢なエラー処理とログ機能
- **ラズパイ対応**: Raspberry Piでの動作を考慮した設計

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`config/env.example`を参考に、`.env`ファイルを作成してください：

```bash
cp config/env.example .env
```

`.env`ファイルを編集して、OpenAI APIキーを設定してください：

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. OpenAI APIキーの取得

1. [OpenAI Platform](https://platform.openai.com/)にアクセス
2. アカウントを作成またはログイン
3. API Keysセクションで新しいAPIキーを作成
4. 作成したAPIキーを`.env`ファイルに設定

## 使用方法

### 基本的な使用方法

```python
from src.speech_to_text import SpeechToText

# SpeechToTextインスタンスを作成
stt = SpeechToText()

# 音声ファイルを文字起こし
result = stt.transcribe_audio_file("path/to/audio.wav")
print(result)
```

### コマンドラインからの使用

```bash
python src/speech_to_text.py path/to/audio.wav --language ja
```

### 対話的な使用例

```bash
python example_usage.py
```

## 対応音声形式

- WAV
- MP3
- M4A
- FLAC
- その他Whisper APIがサポートする形式

## 設定オプション

### 環境変数

| 変数名 | デフォルト値 | 説明 |
|--------|-------------|------|
| `OPENAI_API_KEY` | - | OpenAI APIキー（必須） |
| `WHISPER_MODEL` | `whisper-1` | 使用するWhisperモデル |
| `DEFAULT_LANGUAGE` | `ja` | デフォルト言語 |
| `LOG_LEVEL` | `INFO` | ログレベル |
| `SAMPLE_RATE` | `16000` | サンプルレート |
| `MAX_AUDIO_DURATION` | `30` | 最大録音時間（秒） |

## プロジェクト構造

```
ai_robo/
├── src/                    # ソースコード
│   ├── __init__.py
│   ├── speech_to_text.py   # 音声文字起こしモジュール
│   └── config.py          # 設定管理モジュール
├── config/                # 設定ファイル
│   └── env.example        # 環境変数設定例
├── docs/                  # ドキュメント
├── requirements.txt       # 依存関係
├── example_usage.py       # 使用例
└── README.md             # このファイル
```

## 開発方針

詳細な開発方針については、[docs/development_policy.md](docs/development_policy.md)を参照してください。

## トラブルシューティング

### よくある問題

1. **APIキーエラー**
   - `.env`ファイルに正しいAPIキーが設定されているか確認
   - APIキーに十分なクレジットがあるか確認

2. **音声ファイルエラー**
   - ファイルパスが正しいか確認
   - 音声ファイルが破損していないか確認
   - サポートされている音声形式か確認

3. **ネットワークエラー**
   - インターネット接続を確認
   - ファイアウォール設定を確認

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

プルリクエストやイシューの報告を歓迎します。詳細は[開発方針](docs/development_policy.md)を参照してください。