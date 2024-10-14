import util
import util.global_value as g
import util.logger.loggingUtil as lu

# 音声からテキストに変換（トランスクリプション）
@lu.loggingAOP("音声からテキストに変換（トランスクリプション）")
def transcribe(file_path):
    with open(file_path, 'rb') as audio_file:
        transcript = g.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    audio_file.close()
    return transcript.text
