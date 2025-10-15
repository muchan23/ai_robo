# AI Robot プロジェクト

OpenAI Whisper APIを使用した自律型ロボット制御システムの開発プロジェクトです。

## 概要

このプロジェクトは、ラズパイで動作する音声会話システムを構築します。マイクで音声を認識し、AI（ChatGPT）と対話して、スピーカーから音声で応答を返す完全な音声会話システムです。

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

### 🎭 顔表情機能
- **8種類の感情表現**: 中性、喜び、悲しみ、怒り、驚き、思考、聞いている、話している
- **リアルタイム表情変化**: 音声会話に連動した表情の自動更新
- **感情分析**: AI応答内容から自動で感情を判定
- **アニメーション**: スムーズな表情変化（0.5秒のイージング）
- **フルスクリーン対応**: モニター全体を顔として使用可能


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

### 基本的な使用方法

#### 1. 自動音声検出モード（推奨）
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

### 🎭 顔表情付き音声会話システム

音声会話に表情表示を統合したシステムも利用できます：

#### 1. 顔表情付き自動音声検出モード
```bash
python face_voice_chat.py
```
- **音声認識とAI対話**
- **リアルタイム表情変化**
- **感情分析による自動表情**
- **アニメーション付き表情切り替え**

#### 2. フルスクリーンモード（推奨）
```bash
python face_voice_chat.py --fullscreen
```
- モニター全体を顔として使用
- より大きな表情表示
- 没入感のある対話体験

#### 3. 顔表情付き音声ファイル処理モード
```bash
python face_voice_chat.py --file path/to/audio.wav
```
- 音声ファイルの処理と表情表示
- 感情分析による表情変化

#### 4. 顔表情システムテストモード
```bash
python face_voice_chat.py --test
```
- 顔表情機能の設定確認
- 表情システムの動作テスト

#### 5. 表情のみのテスト
```bash
python src/face_display.py
```
- 表情システムのみのテスト
- キーボード操作で表情を手動切り替え
- キー操作: 0=中性, 1=喜び, 2=悲しみ, 3=怒り, 4=驚き, ESC=終了


### 高度な使用方法

#### 音声の種類を変更
```bash
# 通常版
python voice_chat.py --voice nova  # 女性の声
python voice_chat.py --voice onyx  # 男性の声

# 顔表情付き版
python face_voice_chat.py --voice nova  # 女性の声
python face_voice_chat.py --voice onyx  # 男性の声
```

#### ChatGPTモデルを変更
```bash
# 通常版
python voice_chat.py --model gpt-4o  # GPT-4oを使用（より高精度）

# 顔表情付き版
python face_voice_chat.py --model gpt-4o  # GPT-4oを使用（より高精度）
```

#### 画面サイズの調整
```bash
# カスタム画面サイズ
python face_voice_chat.py --width 1024 --height 768

# フルスクリーンモード
python face_voice_chat.py --fullscreen
```

### プログラムからの使用

#### 通常版
```python
from src.voice_conversation import VoiceConversation

# 音声会話システムを作成
conversation = VoiceConversation()

# 自動音声検出モードで開始
conversation.start_conversation(auto_mode=True)

# 手動で音声ファイルを処理
response = conversation.process_audio_file("audio.wav")
conversation.speak_response(response)
```

#### 顔表情付き版
```python
from src.face_voice_conversation import FaceVoiceConversation
from src.face_display import Emotion

# 顔表情付き音声会話システムを作成
conversation = FaceVoiceConversation(fullscreen=True)

# 自動音声検出モードで開始
conversation.start_conversation(auto_mode=True)

# 手動で音声ファイルを処理
response = conversation.process_audio_file("audio.wav")
conversation.speak_response(response)

# 手動で表情を設定
conversation.set_emotion(Emotion.HAPPY)
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
│   ├── speech_to_text.py         # 音声文字起こしモジュール
│   ├── audio_recorder.py         # 音声録音モジュール
│   ├── ai_chat.py               # AI対話モジュール
│   ├── text_to_speech.py        # 音声合成モジュール
│   ├── voice_conversation.py    # 会話システム統合モジュール
│   ├── face_display.py          # 顔表情表示モジュール
│   ├── face_voice_conversation.py # 顔表情付き会話システム統合モジュール
│   └── config.py                # 設定管理モジュール
├── config/                       # 設定ファイル
│   └── env.example              # 環境変数設定例
├── docs/                         # ドキュメント
├── recordings/                   # 録音ファイル（一時）
├── requirements.txt              # 依存関係
├── voice_chat.py                # メインスクリプト（通常版）
├── face_voice_chat.py           # メインスクリプト（顔表情付き版）
├── example_usage.py             # 使用例
└── README.md                    # このファイル
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

#### 3. 音声再生エラー
```
音声再生に失敗しました。適切なプレイヤーがインストールされていません。
```
**解決方法**:
```bash
# 音声再生ソフトをインストール
sudo apt update
sudo apt install mpg123 pygame
```

#### 4. 顔表情が表示されない
```
pygame.error: No available video device
```
**解決方法**:
- pygame が正しくインストールされているか確認
- ディスプレイが接続されているか確認
- フルスクリーンモードで問題が解決するか確認

#### 5. 表情の切り替えが遅い
**解決方法**:
- システムのリソース使用量を確認
- 他のアプリケーションを終了
- 画面サイズを小さくしてテスト

#### 6. 権限エラー
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

### v1.1.0 (2024-10-15)
- **顔表情機能追加**
  - 8種類の感情表現（中性、喜び、悲しみ、怒り、驚き、思考、聞いている、話している）
  - リアルタイム表情変化
  - 感情分析による自動表情判定
  - フルスクリーン対応
  - アニメーション付き表情切り替え
  - 音声会話と表情の統合システム

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