# AI Robot - 自律型音声認識ロボット制御プロジェクト

## プロジェクト概要
音声認識技術と周囲環境認識技術を組み合わせて、話しかけた内容に基づいてロボットが動作し、さらに周囲の状況を自動的に認識して適切なタスクを実行する自律型システムを構築する。

---

# Raspberry Pi - マイクとスピーカーの使い方

Raspberry Pi に USBマイクと USBスピーカーを接続して、録音・再生を行う方法をまとめます。

## 🎤 マイクの利用方法

### 1. 接続確認
USBマイクが認識されているか確認します：
```bash
arecord -l
```

出力例：
```
**** List of CAPTURE Hardware Devices ****
card 3: Microphone [USB Microphone], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```
👉 card番号 と device番号 を確認します（例: card 3, device 0）。

### 2. 録音
5秒間録音する例：
```bash
arecord -D plughw:3,0 -f cd -t wav -d 5 test.wav
```
- `-D plughw:3,0` → card番号3, device番号0を指定
- `-f cd` → 44.1kHz, 16bit, ステレオ録音
- `-d 5` → 5秒間録音
- `test.wav` → 保存ファイル名

## 🔊 スピーカーの利用方法

### 1. 接続確認
USBスピーカーが認識されているか確認します：
```bash
aplay -l
```

出力例：
```
card 4: UACDemoV10 [UACDemoV1.0], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```
👉 card番号 と device番号 を確認します（例: card 4, device 0）。

### 2. 再生
録音したファイルを再生する例：
```bash
aplay -D plughw:4,0 test.wav
```
- `-D plughw:4,0` → card番号4, device番号0を指定

## ⚙️ デフォルトデバイスの設定（任意）
毎回番号を指定するのが面倒な場合は `/etc/asound.conf` を編集します：
```bash
sudo nano /etc/asound.conf
```

例：スピーカーを card 4 に固定する場合
```conf
pcm.!default {
    type hw
    card 4
}

ctl.!default {
    type hw
    card 4
}
```

保存して再起動すると、次のようにシンプルに使えます：
```bash
arecord test.wav
aplay test.wav
```

## ✅ 動作確認フロー
1. `arecord -l` でマイクを確認
2. `aplay -l` でスピーカーを確認
3. `arecord` で録音
4. `aplay` で再生