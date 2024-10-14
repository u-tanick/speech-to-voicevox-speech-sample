import util
import util.global_value as g

# 音声データのトランスクリプション
def transcribe(file_path):
    with open(file_path, 'rb') as audio_file:
        transcript = g.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    audio_file.close()
    return transcript.text
