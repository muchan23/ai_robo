# ラズパイ音声制御ロボットシステム

OpenAI APIを使用した音声認識・AI解釈・モーター制御の統合システムです。

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
├── scripts/                  # 実行スクリプト
│   ├── main.py              # 基本音声対話システム
│   ├── main_simple.py       # シンプル音声対話
│   └── voice_motor_control.py # 音声制御ロボット（メイン）
├── examples/                 # サンプル・テストファイル
│   ├── debug_gif_animation.py
│   ├── test_display_gif.py
│   └── test_simple_gif.py
├── src/                      # ソースコード
│   ├── audio/                # 音声認識
│   │   ├── voice_recognition.py
│   │   └── voice_recognition_simple.py
│   ├── ai/                   # AI対話・解釈
│   │   ├── ai_chat.py        # 基本AI対話
│   │   └── motor_ai_chat.py  # モーター制御用AI
│   ├── motor/                # モーター制御
│   │   ├── motor_controller.py
│   │   └── motor_speed_test.py
│   └── tts/                  # 音声合成
├── assets/                   # アセットファイル
├── docs/                     # ドキュメント
├── tests/                    # テスト
├── requirements.txt          # 依存関係
└── env.example              # 環境設定例
```

## 🎤 使用方法

### 音声制御ロボット（メイン）
```bash
# 音声でロボットを制御
cd /home/murakami/ai_robo
python scripts/voice_motor_control.py
```

### 基本音声対話システム
```bash
# 音声対話システム
cd /home/murakami/ai_robo
python scripts/main.py

# シンプル音声対話
cd /home/murakami/ai_robo
python scripts/main_simple.py
```

### 個別テスト
```bash
# 音声認識テスト
python tests/test_audio.py

# AI対話テスト
python tests/test_ai.py

# 音声合成テスト
python tests/test_tts.py

# モーター制御テスト
python src/motor/motor_controller.py

# AI解釈テスト
python src/ai/motor_ai_chat.py
```

### 音声制御ロボットの機能
- **音声認識**: OpenAI Whisper APIで音声をテキストに変換
- **AI解釈**: 音声指示をモーター制御コマンドに変換
- **モーター制御**: 前進・後退・回転・停止の制御
- **自然な指示**: 「前に進んで」「右に回って」「止まって」など

### 音声指示の例
- **「前に進んで」** → 前進（速度50%、2秒）
- **「速く右に回って」** → 右回転（速度80%、1.5秒）
- **「止まって」** → 停止
- **「後ろに下がって」** → 後退（速度30%、1.5秒）

### 操作方法
1. スクリプトを実行
2. 「音声を待機中...」と表示されたら話しかける
3. 音声が検出されると自動で文字起こし実行
4. AI解釈でモーター制御コマンドを生成
5. モーターが動作する
6. Ctrl+C で終了

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

## 🚗 モーター制御の設定

### GPIO設定（4チャンネル制御）
- **モーターA (左モーター)**:
  - **IN1**: GPIO 17
  - **IN2**: GPIO 22
  - **ENA**: GPIO 18 (PWM)
- **モーターB (右モーター)**:
  - **IN3**: GPIO 23
  - **IN4**: GPIO 24
  - **ENB**: GPIO 25 (PWM)

### GPIO接続表

| L298Nピン | ラズパイGPIO | 物理ピン | 説明 |
|-----------|-------------|----------|------|
| IN1 | GPIO 17 | 11 | モーターA制御1 |
| IN2 | GPIO 22 | 15 | モーターA制御2 |
| ENA | GPIO 18 | 12 | モーターA速度制御 (PWM) |
| IN3 | GPIO 23 | 16 | モーターB制御1 |
| IN4 | GPIO 24 | 18 | モーターB制御2 |
| ENB | GPIO 25 | 22 | モーターB速度制御 (PWM) |
| VCC | 5V | 2 | 電源 (5V) |
| GND | GND | 6 | グランド |

### 制御可能な動作
- **前進**: `move_forward` (両モーター、左のみ、右のみ)
- **後退**: `move_backward` (両モーター、左のみ、右のみ)
- **左回転**: `turn_left` (右モーター前進、左モーター後退)
- **右回転**: `turn_right` (左モーター前進、右モーター後退)
- **停止**: `stop`

### モーター指定オプション
- `"both"`: 両方のモーター（デフォルト）
- `"left"`: 左モーターのみ（モーターA）
- `"right"`: 右モーターのみ（モーターB）

### パラメータ
- **速度**: 0-100%
- **時間**: 0.1-10秒

## 📝 次のステップ

1. **モーター制御の最適化** - 回転制御の改善
2. **音声指示の拡張** - より複雑な指示への対応
3. **センサー連携** - 距離センサーやカメラとの統合
4. **ロボット制御の高度化** - 自律走行機能の追加
