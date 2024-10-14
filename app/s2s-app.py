import os
import streamlit as st
from openai import OpenAI
import tomllib

from core import record_audio
from core import chat_llm
from core import transcribe
from core import text_to_speech

import util.logger.loggingUtil as lu
import util.global_value as g

# ロガーの初期化
lu.init_logger("application")

# 環境変数の読み込み
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

# OpenAI APIの設定をグローバルに宣言（Whisperとチャットで利用）
g.client = OpenAI(api_key=OPENAI_API_KEY)

# TOMLファイルの読み込み
with open('llm_character.toml', 'rb') as file:
    data = tomllib.load(file)
# LLMのキャラクターロールを読み込む（default, zundamon, stackchan）
g.llm_character = data['default']

# ページ設定
st.set_page_config(page_title="Speech to VOICEVOX Speech", layout="wide")

# カスタムCSSを適用
custom_css = """
<style>
    .st-emotion-cache-h4xjwg {
        display: none;
    }
    .st-emotion-cache-1jicfl2 {
        width: 100%;
        padding: 1rem 2rem 1rem;
    }
    .stButton {
        text-align: center;
    }
    .st-emotion-cache-1cfn047{
        background-color: #339933;
    }
    .st-emotion-cache-1cfn047:hover{
        color: white !important;
        border-color: black !important;
        background-color: #00CCFF !important;
    }
    .st-emotion-cache-1cfn047:focus:not(:active) {
        color: white !important;
        border-color: black !important;
    }
    .st-ay {
        font-size: 5rem;
    }
    .st-emotion-cache-1xjb298 input {
        font-size: 1rem;
    }
    .st-emotion-cache-eq2h7m p {
        font-size: 3rem;
    }
    .st-emotion-cache-ml2xh6 {
        margin-top: 50px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# セッションステートで質問と回答を管理
if 'question' not in st.session_state:
    st.session_state.question = ""
if 'response' not in st.session_state:
    st.session_state.response = ""

@lu.loggingAOP("main関数の処理")
def main():

    SPK_ON = False

    # UIの設定
    st.title("音声アシスタント")

    # セッションステートの初期化
    if 'question' not in st.session_state:
        st.session_state.question = ""

    if 'response' not in st.session_state:
        st.session_state.response = ""

    # 2つのカラムに分割
    col1_a, col1_b = st.columns([3, 1])

    # 各カラムに要素を配置
    with col1_b:
        # スピーチID
        speaker_id = st.number_input('VOICEID', min_value=0, max_value=80, step=1, value=3)
    with col1_a:
        # STT、TTSとLLMの統合
        if st.button("ボタンを押したら質問してね"):

            print("-----------------------------")
            # print("録音開始")
            speech_file = record_audio()
            print(speech_file)
            # print("録音修了")

            print("-----------------------------")
            print("音声からテキストに変換開始")
            st.session_state.question = transcribe(speech_file)
            print(st.session_state.question)
            print("音声からテキストに変換修了")

            print("-----------------------------")
            print("テキストを使用して生成AIに質問開始")
            st.session_state.response = chat_llm(st.session_state.question)
            print(st.session_state.response)
            print("テキストを使用して生成AIに質問修了")
            SPK_ON=True

    # テキストエリアの表示
    st.text_area("ご質問内容", value=st.session_state.question, height=250)
    st.text_area("生成AIの回答", value=st.session_state.response, height=500)

    # テキストを先に画面に表示させてから音声を出力させるため、TTS部分を分離しフラグで管理
    # これをボタンのif文の中に入れると発話終了まで画面が更新されない（テキスト表示がされない）
    if SPK_ON :
        print("-----------------------------")
        print("生成AIの回答を音声に変換・再生開始")
        text_to_speech(st.session_state.response, speaker_id)
        print("生成AIの回答を音声に変換・再生修了")
        SPK_ON=False

    # [TBD]
    # if st.button("会話履歴クリア（新規に質問する場合）"):
    #     st.session_state.question = ""
    #     st.session_state.response = ""
    #     # historyをクリアする処理

if __name__ == '__main__':
    main()
