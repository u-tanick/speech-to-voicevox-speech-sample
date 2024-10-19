# speech-to-voicevox-speech-sample

話しかけた声を元に、生成AIで作成した回答をVOICEVOXの音声で返すサンプルです。  
アプリケーションの実行ファイル本体は以下に格納されています。

![demo](img/demo.jpg)

個別ファイルの説明はsrcフォルダにあるREADMEを参照してください。

``` sh
src/s2s-app.py ほか
```

## 仕組み

基本的な処理の流れは下の図の通りとなってます。

![s2s](img/s2s.jpg)

- 音声のテキスト化
  - OpenAI Wisperを使用しています。
- テキストを元にした生成AIとの対話
  - OpenAI ChatGPT-4o-mini を使用しています。
- 生成AIの回答テキストを50文字程度の文章に区切る
- テキストの音声化
  - VOICEVOXのローカルインストール版を使用しています。
- UI
  - 入出力の内容を確認する用のUIをStreamlitで実装しています。

このアプリケーションではSpeech-to-Speechの部分のみを実装していますが、音声に合わせて反応するアバターを別途用意することで、キャラクターとの対話としても応用できます。

Windows PC用ですが、そのようなアバタープログラムもこちらで公開しています。  
https://github.com/u-tanick/m5stack-avatar-on-WinPC


## 実行環境

- Python 3.12 で動作確認済みです。
  - Python 3.13 は、まだ対応していないライブラリがある可能性があります。

- Python
  - 主なライブラリ
    - streamlit    // UI用
    - openai       // 生成AI用
    - sounddevice  // 音声録音用
    - numpy        // 音声録音用
    - pydub        // 音声再生用
    - requests     // REST-API呼び出し用(VOICEVOX)
    - など

インストールコマンド例（ほか足らないものあれば適宜追加してください）

``` sh
pip install streamlit
pip install openai
pip install sounddevice
pip install numpy
pip install pydub
pip install pathlib
pip install requests
pip install scipy
pip install regex
pip install mecab
pip install environ
pip install logging
pip install logging.config
pip install pyyaml
pip install noisereduce
pip install soundfile
pip install demoji
```

### ソフトウェアインストール

以下を取得しインストールします。

1. ダウンロード版VOICEVOX
   - 取得先：https://voicevox.hiroshiba.jp/
   - 参考：インストール方法など：https://sosakubiyori.com/voicevox-introduction/

2. FFmpeg
   - 取得先：https://ffmpeg.org/download.html
   - 参考：インストール方法など：https://jp.videoproc.com/edit-convert/how-to-download-and-install-ffmpeg.htm

### 環境変数の設定

以下をシステム環境変数に設定します。

1. OpenAI ChatGPT, Wipsper用のAPIキー
   - キー名
     - OPENAI_API_KEY
   - 値
     - OpenAIのアカウントを作成し取得したものを設定
     - 参考：取得手順など：https://qiita.com/kurata04/items/a10bdc44cc0d1e62dad3

2. FFmpegのパス
   - キー名
     - Path
   - 値の例
     - C:\ffmpeg\bin
     - インストールした場所に合わせて設定

## 実行手順

1. ダウンロード版VOICEVOXを起動します。
   - アプリを起動させた状態でREST APIサーバーも立ち上がった状態になります。

2. srcフォルダに移動して、以下のコマンドを実行するとブラウザが開き画面が立ち上がります。
   - ライブラリが足らないなどで起動に失敗する場合は適宜ライブラリを追加してください。

    ``` sh
    streamlit run s2s-app.py &
    ```

3. 画面上の `「ボタンを押したら質問してね」` ボタンを押し、話しかけるとVOICEVOCのずんだもん（ノーマル）の声で返事がきます。
   - 発話後に無音が2秒以上続いた時点で音声録音がストップし、対話処理に進みます。
   - 現時点では、対話履歴などの処理は実装していないため、会話は一回の応答で完結しています。
   - 画面右上のVOICEIDを変更することで、ずんだもん（ノーマル）以外の声に変えることも可能です。
     - VOICEVOXのスピーチID一覧
       - https://gist.github.com/u-tanick/1e27e681461496fd8d1a8792f971b398
     - こちらのサイトでIDの声を実際に確認できます
       - https://voicevox.hiroshiba.jp/

![demo](img/demo.jpg)



## 出典・参考・謝辞

STT, TTS部分の実装は、下記を多大に参考にさせていただきました。ありがとうございます。

- @mashmoeiar11さん  
  - [OpenAIの自動音声認識システムWhisperをつかってみる](https://qiita.com/mashmoeiar11/items/dc45be7252135b2173ca)

- @u0c8さん
  - [PythonでVOICEVOX APIを使ってwavを書きだす](https://qiita.com/u0c8/items/564046ef5a67a0639091)

- VOICEVOX
  - 利用規約
    - https://voicevox.hiroshiba.jp/term/
  - 本サンプルはローカル版のREST APIを利用させていただく仕組みとなっております。
