import time
import requests
import threading
from queue import Queue
from pathlib import Path
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import util.logger.loggingUtil as lu

# pygameの初期化を一度だけ行う
pygame.mixer.init()

# 音声ファイルの生成
def fetch_voice_data(text, speaker_id):
    query_url = f"http://localhost:50021/audio_query?text={text}&speaker={speaker_id}"
    synthesis_url = f"http://localhost:50021/synthesis?speaker={speaker_id}"

    # 音声クエリのリクエスト
    response_audio = requests.post(query_url)
    if response_audio.status_code != 200:
        raise Exception(f"Failed to fetch audio query: {response_audio.status_code}")

    audio_query = response_audio.json()

    # 音声合成のリクエスト
    response_synthesis = requests.post(synthesis_url, json=audio_query)
    if response_synthesis.status_code != 200:
        raise Exception(f"Failed to synthesize: {response_synthesis.status_code}")

    # 保存先ディレクトリの設定
    output_dir = "audio_out"
    output_path = Path.cwd() / output_dir

    # ディレクトリが存在しない場合は作成
    if not output_path.exists():
        output_path.mkdir(parents=True)

    # ファイル名を「create_play_audio_{int(time.time())}.wav」に設定
    file_name = f"create_play_audio_{int(time.time())}.wav"
    audio_file_path = output_path / file_name

    # 音声ファイルを指定の場所に保存
    with open(audio_file_path, 'wb') as audio_file:
        audio_file.write(response_synthesis.content)

    return str(audio_file_path)

# キューに入った音声ファイル再生を順に再生する
def play_audio_from_queue(audio_queue):
    while True:
        # キューから音声ファイルのパスを取得
        audio_path = audio_queue.get()
        if audio_path is None:  # 終了信号
            break
        print(f"Playing audio file: {audio_path}")
        play_audio(audio_path)
        audio_queue.task_done()

# 音声ファイル再生のコア
def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # 再生が終わるまで待機
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# 各行ごとの処理
def process_sentences(sentences, speaker_id, audio_queue):
    
    for sentence in sentences:
        print("-----------------------------------------")
        print(sentence)

        # 音声データを生成
        audio_path = fetch_voice_data(sentence, speaker_id)
        print("Audio file created:", audio_path)

        # 生成した音声ファイルをキューに追加
        audio_queue.put(audio_path)

# 音声からテキストに変換
@lu.loggingAOP("音声からテキストに変換")
def text_to_speech(sentences, speaker_id):

    print("text_to_speechの中")
    
    # 音声ファイルのパスを保持するキュー
    audio_queue = Queue()

    # 再生スレッドを開始
    playback_thread = threading.Thread(target=play_audio_from_queue, args=(audio_queue,))
    playback_thread.start()

    # 音声ファイルの生成
    process_sentences(sentences, speaker_id, audio_queue)

    # 音声ファイルの生成が終わった後、再生スレッドに終了信号を送る
    audio_queue.put(None)
    playback_thread.join()  # 再生スレッドが終了するまで待機
