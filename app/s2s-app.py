import os
import time
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from openai import OpenAI
from pathlib import Path
import requests
import streamlit as st
from pydub import AudioSegment
from pydub.playback import play

# ページ設定
st.set_page_config(page_title="Voice Assistant", layout="wide")

# .envファイルの読み込み
LLM_API_KEY=os.getenv('OPENAI_API_KEY')

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

# 録音データの取得
def record_audio(fs=16000, output_dir="audio_in", silence_threshold=2.0, min_duration=0.1, amplitude_threshold=0.01):
    audio_directory = Path.cwd() / output_dir
    audio_directory.mkdir(parents=True, exist_ok=True)
    file_path = audio_directory / f"recorded_audio_{int(time.time())}.wav"

    recorded_audio = []
    silent_time = 0

    with sd.InputStream(samplerate=fs, channels=1) as stream:
        while True:
            data, overflowed = stream.read(int(fs * min_duration))
            if overflowed:
                print("Overflow occurred. Some samples might have been lost.")
            recorded_audio.append(data)
            if np.all(np.abs(data) < amplitude_threshold):
                silent_time += min_duration
                if silent_time >= silence_threshold:
                    break
            else:
                silent_time = 0

    audio_data = np.concatenate(recorded_audio, axis=0)
    audio_data = np.int16(audio_data * 32767)  # 録音データを16ビット整数に変換
    write(file_path, fs, audio_data)

    return file_path

# OpenAI APIの設定
# wisper用
client = OpenAI(api_key=LLM_API_KEY)

# 音声データのトランスクリプション
def transcribe(file_path):
    with open(file_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    audio_file.close()
    return transcript.text

# OpenAI APIの設定
# gpt-4o用
# llm_client = OpenAI(api_key=LLM_API_KEY)
MODEL_NAME = "gpt-4o-mini"
MAX_TOKENS = 2000
llm_character = "あなたはミラクル三井です"

# OpenAI GPTにクエリを投げる
def ask_openai(question):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": llm_character
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            },
        ]
    )
    return response.choices[0].message.content

# テキストを音声に変換して再生
# Speaker ID : 3 は「ずんだもん（ノーマル）」です
# その他のスピーチID一覧
# https://gist.github.com/u-tanick/1e27e681461496fd8d1a8792f971b398
# 声を確認したい場合はこちらから
# https://voicevox.hiroshiba.jp/
def text_to_speech(text, speaker_id):
    print(speaker_id)
    response_audio = requests.post(f"http://localhost:50021/audio_query?text={text}&speaker={speaker_id}")
    if response_audio.status_code == 200:
        response_synthesis = requests.post(f"http://localhost:50021/synthesis?speaker={speaker_id}", json=response_audio.json())
        if response_synthesis.status_code == 200:
            # バイナリデータを取り出しwaveファイルを作成
            data_binary = response_synthesis.content
            audio_path = "audio_out/output.wav"
            with open(audio_path, "wb") as f:
                f.write(data_binary)
            f.close()
            # waveファイルを再生
            sound = AudioSegment.from_wav(audio_path)
            play(sound)

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
            print("録音開始")
            speech_file = record_audio()
            print(speech_file)
            print("録音修了")

            print("-----------------------------")
            print("音声からテキストに変換開始")
            st.session_state.question = transcribe(speech_file)
            print(st.session_state.question)
            print("音声からテキストに変換修了")

            print("-----------------------------")
            print("テキストを使用して生成AIに質問開始")
            st.session_state.response = ask_openai(st.session_state.question)
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
