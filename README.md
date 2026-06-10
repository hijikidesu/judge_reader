# judge_reader
SOUND VOLTEXのプレイ画面に表示される詳細判定を読み取るツールです

120 fpsで撮影された約2分間の動画の場合、約30秒で判定を読み取ることが出来ます

# 作成経緯
研究で各ノーツに対する判定情報が必要だったので、作成しました。また、一般的なOCRでは精度が低かったため、OCRモデルを自作しました。

# 使い方
1. "Download ZIP"や "git clone"でコードをダウンロード

2. 以下の画像のようにプレイ画面から判定が表示されている部分だけを切り取った動画をffmpegを用いて以下のコードから用意
 
   `ffmpeg -i プレイ画面の動画名 -vf "crop=22:94:555:403,transpose=1" -an 判定だけ切り取った動画名`
<img width="92" height="32" alt="Image" src="https://github.com/user-attachments/assets/2fbb8f02-183e-458e-9745-b7fc050a30e2" />

4. `python judge_reader.py`を実行する

# 動作確認環境
・conda 24.11.3

・python 3.9.23 

・opencv-python 4.11.0.86

・numpy  1.26.4

・pandas 1.5.1

・pillow 11.1.0

・tensorflow 2.9.0

# 注意点
・コナステ(pc版)の練習モードで撮影した動画の場合は、ほぼ100%の精度で読み取れることを確認しているが、それ以外は未検証

・`judge_reader.py`と`judge_read_re_model_h5`は、必ず同じディレクトリ内に配置してください

・UI化は後日予定


