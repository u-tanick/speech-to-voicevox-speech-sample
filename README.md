# speech-to-voicevox-speech-sample

話しかけた声を元に、生成AIで作成した回答をVOICEVOXの音声で返すサンプルです。  
アプリケーションの実行ファイル本体は以下に格納されています。

```
app/s2s-app.py
```

## 仕組み

基本的な処理の流れは下の図の通りとなってます。

![s2s](img/s2s.jpg)

- STT：音声のテキスト化
  - OpenAI Wisperを使用しています。
- LLM：テキストを元にした生成AIとの対話
  - OpenAI ChatGPT-4o-mini を使用しています。
- TTS：テキストの音声化
  - VOICEVOXのローカルインストール版を使用しています。
- UI
  - 入出力の内容を確認する用のUIをStreamlitで実装しています。

このアプリケーションではSpeech-to-Speechの部分のみを実装していますが、音声に合わせて反応するアバターを別途用意することで、キャラクターとの対話としても応用できます。

Windows PC用ですが、そのようなアバタープログラムもこちらで公開しています。  
https://github.com/u-tanick/m5stack-avatar-on-WinPC


## 実行環境

- Python
  - 主なライブラリ
    - streamlit    // UI用
    - sounddevice  // 音声録音用
    - numpy        // 音声録音用
    - openai       // 生成AI用
    - requests     // REST-API呼び出し用(VOICEVOX)
    - pydub        // 音声再生用
  - 適宜、pip install などでご準備ください。
    - その他必要なものについては実行ファイル冒頭のimport宣言をご参照ください。

- 個別インストール
  - VOICEVOX
    - ローカルインストール版を使用します。
      - Web APIを使用される場合は改修してください。
    - インストール手順など
      - https://voicevox.hiroshiba.jp/
      - https://yuushablog.info/voicevox-inst/
  - FFmpegのインストール手順
    - pydub ライブラリが参照するために必要です。
    - インストール手順など
      - https://ffmpeg.org/download.html
      - https://qiita.com/Tadataka_Takahashi/items/9dcb0cf308db6f5dc31b

- APIキー
  - OpenAIのAPIキーが必要です。
  - APIキーは `OSのシステム環境変数` または `ユーザー環境変数` に設定してください。
    - キー名：OPENAI_API_KEY


## 出典・参考・謝辞

STT, TTS部分の実装は、下記を多大に参考にさせていただきました。ありがとうございます。

- @mashmoeiar11さん  
  - [OpenAIの自動音声認識システムWhisperをつかってみる](https://qiita.com/mashmoeiar11/items/dc45be7252135b2173ca)

- @u0c8さん
  - [PythonでVOICEVOX APIを使ってwavを書きだす](https://qiita.com/u0c8/items/564046ef5a67a0639091)
