import time
from pathlib import Path

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

import util.logger.loggingUtil as lu

# 録音データの取得
@lu.loggingAOP("録音データの取得")
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
