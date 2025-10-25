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
cd /home/murakamitomoki/ai_robo
python scripts/voice_motor_control.py
```

### 高度な音声制御ロボット（新機能）
```bash
# 複数ステップの指示に対応した高度な音声制御
cd /home/murakamitomoki/ai_robo
python scripts/advanced_voice_motor_control.py
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

# 高度なAI解析テスト
python src/ai/advanced_motor_ai.py

# 高度なモーター制御テスト
python src/motor/advanced_motor_controller.py
```

### 音声制御ロボットの機能

#### 基本システム（voice_motor_control.py）
- **音声認識**: OpenAI Whisper APIで音声をテキストに変換
- **AI解釈**: 音声指示をモーター制御コマンドに変換
- **モーター制御**: 前進・後退・回転・停止の制御
- **自然な指示**: 「前に進んで」「右に回って」「止まって」など

#### 高度なシステム（advanced_voice_motor_control.py）
- **複数ステップ指示対応**: 「まっすぐ行って、右に曲がって」など
- **LLM計画生成**: AIが柔軟に実行計画を作成
- **段階的実行**: 複数の動作を順次実行
- **実行確認**: 計画の確認と実行状態の監視

### 音声指示の例

#### 基本システムの指示例
- **「前に進んで」** → 前進（速度50%、2秒）
- **「速く右に回って」** → 右回転（速度85%、1.0秒）
- **「止まって」** → 停止
- **「後ろに下がって」** → 後退（速度30%、1.5秒）

#### 高度なシステムの指示例
- **「まっすぐ行って、右に曲がって」** → [前進→右回転]
- **「左に回って、前に進んで、止まって」** → [左回転→前進→停止]
- **「後ろに下がって、左に回って、前に進んで」** → [後退→左回転→前進]
- **「右に回って、速く前に進んで、左に回って」** → [右回転→高速前進→左回転]

### 操作方法

#### 基本システムの操作方法
1. スクリプトを実行
2. 「音声を待機中...」と表示されたら話しかける
3. 音声が検出されると自動で文字起こし実行
4. AI解釈でモーター制御コマンドを生成
5. モーターが動作する
6. Ctrl+C で終了

#### 高度なシステムの操作方法
1. スクリプトを実行
2. 「音声を待機中...」と表示されたら複雑な指示を話しかける
3. 音声が検出されると自動で文字起こし実行
4. 高度なAI解析で複数ステップの実行計画を生成
5. 実行計画が表示される（ステップ数、推定時間、各ステップの詳細）
6. Enterキーで実行確認、Ctrl+Cでキャンセル
7. 複数ステップの動作が順次実行される
8. Ctrl+C で終了

## 🚀 高度なシステムの詳細

### システム構成
```
高度な音声制御システム
├── 音声認識 (VoiceRecognition)
├── 高度なAI解析 (AdvancedMotorAI)
└── 高度なモーター制御 (AdvancedMotorController)
```

### 新機能の特徴

#### 1. 複数ステップ指示の解析
- **入力**: 「まっすぐ行って、右に曲がって」
- **AI解析**: 2ステップの実行計画を生成
- **出力**: [前進→右回転] の段階的実行

#### 2. LLM計画生成
- **柔軟性**: 毎回変わる指示にも対応
- **最適化**: 速度・時間・順序を自動決定
- **検証**: 計画の妥当性を自動チェック

#### 3. 実行制御
- **確認**: 実行前の計画確認
- **監視**: 実行状態のリアルタイム監視
- **中断**: 実行中の安全な中断

### 使用例

#### 基本指示
```bash
# 単一動作
「前に進んで」 → 前進のみ
「右に回って」 → 右回転のみ
```

#### 複雑な指示
```bash
# 複数ステップ
「まっすぐ行って、右に曲がって」
→ ステップ1: 前進（速度50%、2秒）
→ ステップ2: 右回転（速度85%、1秒）

「左に回って、前に進んで、止まって」
→ ステップ1: 左回転（速度85%、1秒）
→ ステップ2: 前進（速度50%、2秒）
→ ステップ3: 停止
```

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
| IN3 | GPIO 19 | 35 | モーターB制御1 |
| IN4 | GPIO 26 | 37 | モーターB制御2 |
| ENB | GPIO 13 | 33 | モーターB速度制御 (PWM) |
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
- **速度**: 30-100% (最低動作速度30%)
- **時間**: 0.1-10秒

### モーター制御ファイル構成
```
src/motor/
├── motor_controller.py          # メイン制御クラス
├── rotation_direction_test.py   # 回転方向テスト
└── speed_calibration_test.py    # 速度調整テスト
```

### テスト実行方法
```bash
# 回転方向テスト（タイヤの回転方向確認）
python src/motor/rotation_direction_test.py

# 速度調整テスト（左右の速度差調整）
python src/motor/speed_calibration_test.py

# メイン制御テスト（全機能テスト）
python src/motor/motor_controller.py
```

### 速度調整機能
- **自動補正**: 左右のモーターの個体差を自動補正
- **手動調整**: 補正係数を手動で設定可能
- **最低速度**: 30%未満は自動的に30%に調整

### トラブルシューティング
- **モーターが動かない**: 速度を30%以上に設定
- **左右の速度が違う**: `speed_calibration_test.py`を実行
- **回転方向が逆**: 配線を確認し、必要に応じて交換

## 📝 次のステップ

1. **モーター制御の最適化** - 回転制御の改善
2. **音声指示の拡張** - より複雑な指示への対応
3. **センサー連携** - 距離センサーやカメラとの統合
4. **ロボット制御の高度化** - 自律走行機能の追加
