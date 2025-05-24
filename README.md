# MCP(Model Context Protocol)から私(人間)を管理してもらうプロジェクト
記事

https://note.com/sachi2222/n/nd566434fed6e

## 機能一覧
 - Webカメラの撮影
 - PCの画面キャプチャ
 - 現在時刻の取得
 - 指定時間待つ
 - 音声の読み上げ
 - ダイアログの表示
 
## 準備
必要なライブラリ
```shell
fastmcp
pywin32
mss
Pillow
opencv-python
pyttsx3
```

## 実行
stdioでこのMCPを実行します。

## 想定プロンプト
```
私は、19:30まで勉強をしたいです。
Human MCP toolsで、サボったり、他のことをしてないかscreencaptureやwebcamで監視してください。
適切と思われるタイミングでspeakやダイアログでアドバイスしてください。
私へのアドバイスは、やさしいお姉さん風にしてください。
あなたのコンテキストウインドウは上限があります。
作業完了までにコンテキストウインドウを使い切らないようにwaitを入れてください。
```