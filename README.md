# AI Robot プロジェクト

OpenAI Whisper APIを使用した自律型ロボット制御システムの開発プロジェクトです。

## 概要

このプロジェクトは、ラズパイで動作する音声会話システムを構築します。マイクで音声を認識し、AI（ChatGPT）と対話して、スピーカーから音声で応答を返す完全な音声会話システムです。

### 📱 システム構成
**OpenAI API（Whisper + ChatGPT + TTS）**
- シンプルな構成
- 高品質な音声認識・対話・合成

## 機能

### 🎙️ 音声認識
- **リアルタイム音声検出**: マイクからの音声を自動検出
- **高精度文字起こし**: OpenAI Whisper APIを使用した高精度な音声認識
- **日本語対応**: 日本語音声の認識に最適化

### 🤖 AI対話
- **ChatGPT連携**: OpenAI ChatGPT APIを使用した自然な対話
- **会話履歴管理**: 文脈を理解した継続的な会話
- **カスタマイズ可能**: システムプロンプトでAIの性格を設定

### 🔊 音声合成
- **高品質TTS**: OpenAI TTS APIを使用した自然な音声合成
- **複数音声対応**: 6種類の音声から選択可能
- **自動再生**: 生成された音声を自動でスピーカーから再生

### ⚙️ システム機能
- **設定管理**: 環境変数による柔軟な設定
- **エラーハンドリング**: 堅牢なエラー処理とログ機能
- **ラズパイ最適化**: Raspberry Piでの動作を考慮した設計


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

### 4. ラズパイでの音声デバイス設定

```bash
# 音声デバイスの確認
arecord -l  # マイク一覧
aplay -l    # スピーカー一覧

# デフォルトデバイスの設定（必要に応じて）
sudo raspi-config
# Advanced Options > Audio > 適切なデバイスを選択
```

## 使用方法

### 📱 システム

**OpenAI API（Whisper + ChatGPT + TTS）**

#### 1. 自動音声検出モード
```bash
python voice_chat.py
```
- マイクに向かって話すと自動で音声を検出
- 話し終わったら少し待つとAIが応答
- Ctrl+Cで終了

#### 2. 音声ファイル処理モード
```bash
python voice_chat.py --file path/to/audio.wav
```
- 指定された音声ファイルを処理
- AI応答を音声で再生

#### 3. テストモード
```bash
python voice_chat.py --test
```
- 設定の妥当性をチェック
- システムの動作確認


### 高度な使用方法

#### システム
```bash
# 音声の種類を変更
python voice_chat.py --voice nova  # 女性の声
python voice_chat.py --voice onyx  # 男性の声

# ChatGPTモデルを変更
python voice_chat.py --model gpt-4o  # GPT-4oを使用（より高精度）
```

### プログラムからの使用

#### システム
```python
from src.voice_system.conversation import VoiceConversation

# 音声会話システムを作成
conversation = VoiceConversation()

# 自動音声検出モードで開始
conversation.start_conversation(auto_mode=True)

# 手動で音声ファイルを処理
response = conversation.process_audio_file("audio.wav")
conversation.speak_response(response)
```

## 対応音声形式

### 入力（音声認識）
- WAV
- MP3
- M4A
- FLAC
- その他Whisper APIがサポートする形式

### 出力（音声合成）
- MP3（OpenAI TTS API）
- 自動でスピーカーから再生

## 設定オプション

### 環境変数

| 変数名 | デフォルト値 | 説明 |
|--------|-------------|------|
| `OPENAI_API_KEY` | - | OpenAI APIキー（必須） |
| `WHISPER_MODEL` | `whisper-1` | 使用するWhisperモデル |
| `DEFAULT_LANGUAGE` | `ja` | デフォルト言語 |
| `LOG_LEVEL` | `INFO` | ログレベル |
| `SAMPLE_RATE` | `16000` | サンプルレート |
| `CHUNK_SIZE` | `1024` | チャンクサイズ |
| `MAX_AUDIO_DURATION` | `30` | 最大録音時間（秒） |

### 音声設定

| パラメータ | デフォルト値 | 説明 |
|-----------|-------------|------|
| `--voice` | `alloy` | TTS音声の種類 |
| `--model` | `gpt-4o-mini` | ChatGPTモデル |

## プロジェクト構造

```
ai_robo/
├── src/                           # ソースコード
│   ├── __init__.py
│   ├── config.py                  # 設定管理モジュール
│   ├── voice_system/              # 音声システム（メイン）
│   │   ├── __init__.py
│   │   ├── conversation.py        # 統合会話システム
│   │   ├── audio/                 # 音声処理関連
│   │   │   ├── __init__.py
│   │   │   └── recorder.py        # 音声録音モジュール
│   │   ├── speech/                # 音声認識・合成
│   │   │   ├── __init__.py
│   │   │   ├── recognition.py    # 音声認識モジュール（OpenAI API）
│   │   │   └── synthesis.py      # 音声合成モジュール
│   │   └── ai/                    # AI対話関連
│   │       ├── __init__.py
│   │       └── chat.py           # AI対話モジュール
├── config/                        # 設定ファイル
│   └── env.example               # 環境変数設定例
├── docs/                          # ドキュメント
├── recordings/                    # 録音ファイル（一時）
├── requirements.txt               # 依存関係
├── voice_chat.py                 # メインスクリプト
├── example_usage.py              # 使用例
└── README.md                     # このファイル
```

## トラブルシューティング

### よくある問題

#### 1. APIキーエラー
```
ValueError: OpenAI APIキーが設定されていません
```
**解決方法**: `.env`ファイルに正しいAPIキーが設定されているか確認

#### 2. 音声デバイスエラー
```
OSError: [Errno -9996] Invalid input device
```
**解決方法**: 
```bash
# 音声デバイスを確認
arecord -l
# 適切なデバイスを選択
```

#### 4. 音声再生エラー
```
音声再生に失敗しました。適切なプレイヤーがインストールされていません。
```
**解決方法**:
```bash
# 音声再生ソフトをインストール
sudo apt update
sudo apt install mpg123
```

#### 5. 権限エラー
```
PermissionError: [Errno 13] Permission denied
```
**解決方法**:
```bash
# ユーザーをaudioグループに追加
sudo usermod -a -G audio $USER
# 再ログインが必要
```

### デバッグ方法

#### ログレベルの変更
```bash
# .envファイルで設定
LOG_LEVEL=DEBUG
```

#### 音声デバイスのテスト
```bash
# マイクテスト
arecord -d 5 test.wav
aplay test.wav

# スピーカーテスト
speaker-test -t wav -c 2
```

## 開発方針

詳細な開発方針については、[docs/development_policy.md](docs/development_policy.md)を参照してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

プルリクエストやイシューの報告を歓迎します。詳細は[開発方針](docs/development_policy.md)を参照してください。

## 更新履歴

### v1.0.0 (2024-10-15)
- **システム改善**
  - 音声認識・対話・合成の統合システム
  - 高品質な音声処理
  - 安定した動作

### v0.2.0 (2024-10-15)
- **最新モデル対応**
  - GPT-4o-miniをデフォルトに変更
  - 最新のOpenAI API機能を活用
- **インポートエラーの修正**
  - 相対インポートを絶対インポートに変更

### v0.1.0 (2024-10-15)
- 基本的な音声会話システムの実装
- OpenAI Whisper API連携
- OpenAI ChatGPT API連携
- OpenAI TTS API連携
- ラズパイ対応