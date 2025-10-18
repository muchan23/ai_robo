# ラズパイ音声対話システム

OpenAI APIを使用した完全な音声対話システムです。

## 🚀 セットアップ

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. 環境設定
```bash
# 設定ファイルをコピー
cp env.example .env

# .envファイルを編集してAPIキーを設定
nano .env
```

`.env`ファイルの内容：
```
OPENAI_API_KEY=your_openai_api_key_here
CHAT_MODEL=gpt-4o-mini
TTS_MODEL=tts-1
TTS_VOICE=alloy
SAMPLE_RATE=16000
CHUNK_SIZE=1024
AUDIO_THRESHOLD=1000
LOG_LEVEL=INFO
```

### 3. アセットファイルの配置
```bash
# GIFファイルを配置
mkdir -p assets/gifs
# GIFファイルをassets/gifs/フォルダに配置
```

### 4. 音声デバイスの確認（ラズパイ）
```bash
# マイクデバイスを確認
arecord -l

# スピーカーデバイスを確認
aplay -l
```

## 📁 プロジェクト構造

```
ai_robo/
├── main.py                    # メインスクリプト
├── requirements.txt           # 依存関係
├── env.example               # 環境設定例
├── assets/                   # アセットファイル
│   └── gifs/                 # GIFアニメーション
│       └── *.gif
├── src/                      # ソースコード
│   ├── audio/                # 音声処理
│   ├── ai/                   # AI対話
│   ├── tts/                  # 音声合成
│   └── display/              # 表示機能
└── tests/                    # テスト
```

## 🎤 使用方法

### 基本的な実行
```bash
# 統合システム（推奨）
python main.py

# 個別テスト
python tests/test_audio.py    # 音声認識テスト
python tests/test_ai.py        # AI対話テスト
python tests/test_tts.py       # 音声合成テスト
python tests/test_gif.py       # GIF表示テスト
```

### 機能
- **音声検出録音**: 音声が検出されるまで録音
- **自動文字起こし**: OpenAI Whisper APIで音声をテキストに変換
- **AI対話**: OpenAI ChatGPT APIで自然な対話
- **音声合成**: OpenAI TTS APIで音声を生成
- **音声再生**: スピーカーから音声を再生
- **GIF表示**: 音声対話中にGIFアニメーションを表示
- **音声合図**: ビープ音で状態を通知
- **日本語対応**: 日本語音声の認識に最適化

### 操作方法
1. スクリプトを実行
2. 「音声を待機中...」と表示されたら話しかける
3. 音声が検出されると自動で文字起こし実行
4. GIFアニメーションが表示される
5. AI応答が生成される
6. AI応答が音声で再生される
7. 結果が表示される
8. Ctrl+C で終了

## 🔧 設定オプション

### AI対話設定
- `CHAT_MODEL`: ChatGPTモデル（デフォルト: gpt-4o-mini）
- `SYSTEM_PROMPT`: システムプロンプト

### 音声合成設定
- `TTS_MODEL`: TTSモデル（デフォルト: tts-1）
- `TTS_VOICE`: 音声の種類（alloy, echo, fable, onyx, nova, shimmer）
- `TTS_SPEED`: 音声速度（0.25 - 4.0）

### 音声設定
- `SAMPLE_RATE`: サンプルレート（デフォルト: 16000）
- `CHUNK_SIZE`: チャンクサイズ（デフォルト: 1024）
- `AUDIO_THRESHOLD`: 音声検出閾値（デフォルト: 1000）

### ログ設定
- `LOG_LEVEL`: ログレベル（DEBUG, INFO, WARNING, ERROR）

## 🍓 ラズパイでの注意点

### 音声デバイス設定
```bash
# 音声グループに追加
sudo usermod -a -G audio $USER

# 再ログイン後、音声デバイスを確認
arecord -l
```

### 音声再生テスト
```bash
# マイクテスト
arecord -d 3 test.wav
aplay test.wav
```

### トラブルシューティング
- **音声が検出されない**: `AUDIO_THRESHOLD`の値を下げる
- **音声デバイスエラー**: マイクデバイスを確認
- **APIエラー**: OpenAI APIキーを確認

## 📝 次のステップ

1. **AI対話機能の追加** - ChatGPT API連携
2. **音声合成機能の追加** - TTS API連携
3. **統合システムの実装** - 完全な音声対話システム
