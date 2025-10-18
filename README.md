# ラズパイ音声認識システム

OpenAI Whisper APIを使用した音声認識システムです。

## 🚀 セットアップ

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. 環境設定
```bash
# 設定ファイルをコピー
cp config.env.example .env

# .envファイルを編集してAPIキーを設定
nano .env
```

`.env`ファイルの内容：
```
OPENAI_API_KEY=your_openai_api_key_here
SAMPLE_RATE=16000
CHUNK_SIZE=1024
AUDIO_THRESHOLD=1000
LOG_LEVEL=INFO
```

### 3. 音声デバイスの確認（ラズパイ）
```bash
# マイクデバイスを確認
arecord -l

# スピーカーデバイスを確認
aplay -l
```

## 🎤 使用方法

### 基本的な実行
```bash
python voice_recognition.py
```

### 機能
- **音声検出録音**: 音声が検出されるまで録音
- **自動文字起こし**: OpenAI Whisper APIで音声をテキストに変換
- **日本語対応**: 日本語音声の認識に最適化

### 操作方法
1. スクリプトを実行
2. 「音声を検出中...」と表示されたら話しかける
3. 音声が検出されると自動で文字起こし実行
4. 認識結果が表示される
5. Ctrl+C で終了

## 🔧 設定オプション

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
