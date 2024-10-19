import time
from pathlib import Path
from pydub import AudioSegment
import noisereduce as nr
import soundfile as sf

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

import util.logger.loggingUtil as lu

# ファイルの冒頭3秒が無音かどうかを判定、無音の場合Trueを返す
def is_silent_check(audio_file, silence_threshold=-50.0, chunk_size=10, duration=3000):
    """
    audio_file: チェックする音声ファイルのパス
    silence_threshold: 無音とみなすデシベル閾値 (dBFS)
    chunk_size: チャンクのサイズ (ミリ秒)
    duration: 判定に使う冒頭部分の長さ (ミリ秒)
    """
    # 音声ファイルの冒頭数秒だけを読み込み
    audio = AudioSegment.from_file(audio_file)[:duration]

    # チャンクごとに音量レベルをチェック
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i + chunk_size]
        if chunk.dBFS > silence_threshold:  # dBFSは音量を表す単位
            return False  # 音が入っている

    return True  # 全てのチャンクが無音

# ホワイトノイズを除去
def reduce_noise(input_file, output_file):
    # 音声ファイルを読み込む
    audio, sample_rate = sf.read(input_file)

    # ホワイトノイズを除去
    reduced_noise = nr.reduce_noise(y=audio, sr=sample_rate)

    # 除去した音声を保存
    sf.write(output_file, reduced_noise, sample_rate)

# 録音データの取得
@lu.loggingAOP("録音データの取得")
def record_audio(fs=16000, output_dir="audio_in", silence_threshold=2.0, min_duration=0.1, amplitude_threshold=0.01):
    audio_directory = Path.cwd() / output_dir
    audio_directory.mkdir(parents=True, exist_ok=True)
    file_path_i = audio_directory / f"recorded_audio_{int(time.time())}.wav"
    file_path_o = audio_directory / f"recorded_audio_{int(time.time())}_rnz.wav"

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
    write(file_path_i, fs, audio_data)

    reduce_noise(file_path_i, file_path_o)

    if is_silent_check(file_path_o):
        return ""

    return file_path_o
