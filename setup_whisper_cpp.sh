#!/bin/bash
# Whisper.cpp セットアップスクリプト

echo "🚀 Whisper.cpp セットアップを開始します..."

# 1. リポジトリのクローン
echo "📥 Whisper.cpp リポジトリをクローン中..."
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp

# 2. モデルのダウンロード（smallモデル - バランスが良い）
echo "📦 モデルをダウンロード中..."
bash ./models/download-ggml-model.sh small

# 3. ビルド
echo "🔨 ビルド中..."
make

# 4. Pythonバインディングのインストール
echo "🐍 Pythonバインディングをインストール中..."
pip install whisper-cpp-python

echo "✅ Whisper.cpp セットアップ完了！"
echo "📁 インストール場所: $(pwd)"
echo "🎯 モデルファイル: $(pwd)/models/ggml-small.bin"
