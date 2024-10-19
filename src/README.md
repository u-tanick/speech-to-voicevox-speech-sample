# 変更履歴

- 2024/10/19
  - 音声録音時に無音だった場合の判定処理を追加しました。
  - 録音した音声のホワイトノイズを除去しトランスクライブの性能が上がるように修正しました。
  - 生成AIの回答文章を適切な長さで区切り、区切った単位で音声ファイル化し、順次再生する処理を追加しました。
- 2024/10/14
  - 機能ごとにフォルダや関数ファイルを分けました（core/, util/）。
  - 生成AIのキャラクターロールを定義しました。
  - 音声の再生ライブラリをsimpleaudioに変更しました。
  - 実行ログ出力機能を追加しました（暫定で作ってみたものです）。
- 2024/10/6
  - 初版

# TODO

- pythonが無い環境でも利用できるように exe ファイルを作成しようと検討中。
  - Pyinstallerを使ったexeは作成できたがVirusTotalでマルウェア判定となる。
  - これはPyinstallerでのexe化あるあるの誤検知だがさすがに公開は気が引ける。
  - 一応設定ファイルのspecだけは同梱しておく。


## app/以下のフォルダ構造

- s2s-app.py
  - Speech to VOICEVOX Speechのアプリケーション本体
  - streamlitを使用したWebアプリ

- llm_character.toml
  - 生成AIのキャラクターロールの定義
  - s2s-app.py:L24 の `g.llm_character = data['default']` で変更可能
    - 初期は次の3種類から選択可能　default, zundamon, stackchan

- run_main.py
  - exe版作成用のスクリプト
- run_main.spec
  - exe版作成用のスクリプト

- core/
  - record_audio.py
    - 話しかけた声を音声ファイルに保存
  - transcribe.py
    - 音声ファイルをテキスト化（OpenAI Whisperを使用）
  - chat_llm.py
    - テキストを元にLLMに質問（OpenAI ChatGPTを使用）
  - split_text.py
    - LLMの回答テキストを適切な長さで区切る
  - text_to_speech.py
    - 適切に区切られたLLMの回答テキストをVOICEVOXの音声ファイルに変換し、発話

- util/
  - global_value.py
    - グローバル変数をすべての階層のプログラムで共有するための宣言用ファイル（中身は空）
    - 参考：https://qiita.com/minidaruma/items/11eafc95855c007335f6
  - logger/
    - loggingUtil.py
      - 標準のloggingライブラリを使用して作成したログ用デコレーター
      - メソッドの開始と終了および処理時間をログに出力
    - loggingUtil.yaml
      - ログ用デコレーターの設定ファイル
      - loggingライブラリのもの
    - log/
      - ログファイルの出力先（loggingUtil.yamlで変更可能）

- audio_in/
  - 話しかけた声の音声ファイルが格納されるフォルダ

- audio_out/
  - VOICEVOCで生成した音声ファイルが格納されるフォルダ

- hooks/
  - hook-streamlit.py
    - exe版作成用のスクリプト
