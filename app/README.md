## 変更履歴

- 2024年10月14日
  - 機能ごとにフォルダや関数ファイルを分けました（core/, util/）。
  - 生成AIのキャラクターロールを定義しました。
  - 音声の再生ライブラリをsimpleaudioに変更しました。
  - 実行ログ出力機能を追加しました（暫定で作ってみたものです）。
- 2024年10月6日
  - 初版

# app/以下のフォルダ構造

- s2s-app.py
  - Speech to VOICEVOX Speechのアプリケーション本体
  - streamlitを使用したWebアプリ
- llm_character.toml
  - 生成AIのキャラクターロールの定義
  - s2s-app.py:L24 の `g.llm_character = data['default']` で変更可能
    - 初期は次の3種類から選択可能　default, zundamon, stackchan
- core/
  - record_audio.py
    - 話しかけた声を音声ファイルに保存
  - transcribe.py
    - 音声ファイルをテキスト化（OpenAI Whisperを使用）
  - chat_llm.py
    - テキストを元にLLMに質問（OpenAI ChatGPTを使用）
  - text_to_speech.py
    - LLMの回答テキストをVOICEVOXの音声ファイルに変換し、発話
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
