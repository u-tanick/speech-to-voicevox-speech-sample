import os
import requests
import urllib.parse
from pydub import AudioSegment
from pydub.playback import play

# 音素データ生成
text = urllib.parse.quote("これはテスト出力なのだ")
response = requests.post("http://localhost:50021/audio_query?text=" + text + "&speaker=1")

# responseの中身を表示
# print(json.dumps(response.json(), indent=4))

# 音声合成
resp_wav = requests.post("http://localhost:50021/synthesis?speaker=1", json=response.json())

# バイナリデータ取り出し
data_binary = resp_wav.content

audio_path = "audio_out/output.wav"
with open(audio_path, "wb") as f:
    f.write(data_binary)
f.close()

print(os.path.exists(audio_path))  # ファイルが存在するか確認
sound = AudioSegment.from_wav(audio_path)
play(sound)
