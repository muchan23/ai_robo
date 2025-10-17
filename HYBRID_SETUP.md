# ハイブリッド音声会話システム セットアップガイド

Whisper.cpp（ローカル音声認識）+ OpenAI（ChatGPT + TTS）のハイブリッドシステムのセットアップ手順です。

## 🚀 セットアップ手順

### 1. Whisper.cppのインストール

#### **自動セットアップ（推奨）**
```bash
# セットアップスクリプトを実行
chmod +x setup_whisper_cpp.sh
./setup_whisper_cpp.sh
```

#### **手動セットアップ**
```bash
# 1. リポジトリのクローン
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp

# 2. モデルのダウンロード（smallモデル - バランスが良い）
bash ./models/download-ggml-model.sh small

# 3. ビルド
make

# 4. Pythonバインディングのインストール
pip install whisper-cpp-python
```

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定

`.env`ファイルを作成してOpenAI APIキーを設定：

```bash
cp config/env.example .env
```

`.env`ファイルを編集：
```
OPENAI_API_KEY=your_openai_api_key_here
```

## 🎯 使用方法

### 基本的な使用方法

#### 1. ハイブリッド自動音声検出モード
```bash
python hybrid_voice_chat.py
```

#### 2. 音声ファイル処理モード
```bash
python hybrid_voice_chat.py --file path/to/audio.wav
```

#### 3. モデルサイズ指定
```bash
python hybrid_voice_chat.py --whisper-model small
```

#### 4. テストモード
```bash
python hybrid_voice_chat.py --test
```

### モデルサイズの選択

| モデル | サイズ | 速度 | 精度 | 用途 |
|--------|--------|------|------|------|
| `tiny` | ~39MB | 最速 | 低 | テスト用 |
| `base` | ~74MB | 速 | 中 | 軽量用途 |
| `small` | ~244MB | 中 | 高 | **推奨** |
| `medium` | ~769MB | 遅 | 高 | 高精度用途 |
| `large` | ~1550MB | 最遅 | 最高 | 最高精度 |

## 🔧 システム構成

```
🎤 音声入力
    ↓
💾 メモリ内WAV作成（高速）
    ↓
🤖 Whisper.cpp（ローカル・高速）
    ↓
📝 テキスト変換
    ↓
🧠 ChatGPT API（OpenAI）
    ↓
💬 AI応答生成
    ↓
🔊 TTS API（OpenAI）
    ↓
▶️ 音声再生
```

## ✨ 特徴

### 🚀 高速化
- **ファイル保存なし**: メモリ内で音声処理
- **ローカル音声認識**: Whisper.cppで高速処理
- **遅延削減**: 200-500msの高速化

### 🔒 プライバシー保護
- **音声データ**: ローカルで処理（外部送信なし）
- **テキストデータ**: ChatGPT APIに送信
- **一時ファイル**: 自動削除

### 🎯 高品質
- **音声認識**: Whisper.cpp（高精度）
- **AI対話**: ChatGPT API（最新モデル）
- **音声合成**: OpenAI TTS API（自然な音声）

## 🐛 トラブルシューティング

### よくある問題

#### 1. Whisper.cppモデルが見つからない
```
FileNotFoundError: Whisper.cppモデルファイルが見つかりません
```

**解決方法**:
```bash
# モデルファイルの場所を確認
find . -name "ggml-small.bin"

# 手動でモデルをダウンロード
cd whisper.cpp
bash ./models/download-ggml-model.sh small
```

#### 2. whisper-cpp-pythonがインストールできない
```
ImportError: whisper-cpp-pythonがインストールされていません
```

**解決方法**:
```bash
# 依存関係をインストール
sudo apt update
sudo apt install build-essential cmake

# Pythonバインディングをインストール
pip install whisper-cpp-python
```

#### 3. メモリ不足エラー
```
RuntimeError: メモリ不足
```

**解決方法**:
```bash
# より小さなモデルを使用
python hybrid_voice_chat.py --whisper-model tiny
# または
python hybrid_voice_chat.py --whisper-model base
```

#### 4. 音声認識精度が低い
**解決方法**:
- より大きなモデルを使用: `--whisper-model medium`
- 音声の品質を向上（ノイズ除去など）
- マイクの位置を調整

## 📊 パフォーマンス比較

| 方式 | 音声認識 | AI対話 | 音声合成 | 総遅延 | プライバシー |
|------|----------|--------|----------|--------|--------------|
| **従来版** | OpenAI API | OpenAI API | OpenAI API | ~2-3秒 | 低 |
| **ハイブリッド版** | Whisper.cpp | OpenAI API | OpenAI API | ~1-2秒 | 高 |

## 🎉 まとめ

ハイブリッドシステムにより：
- ✅ **高速化**: 200-500msの遅延削減
- ✅ **プライバシー**: 音声データのローカル処理
- ✅ **高品質**: 最新のAI技術を活用
- ✅ **柔軟性**: モデルサイズの選択可能

音声認識はローカルで高速処理し、AI対話と音声合成は高品質なOpenAI APIを活用する最適な構成です！
