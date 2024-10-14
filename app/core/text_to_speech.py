import requests
from pydub import AudioSegment
import simpleaudio as sa
import tempfile
import util.logger.loggingUtil as lu

# 音声からテキストに変換
@lu.loggingAOP("音声からテキストに変換")
def text_to_speech(text, speaker_id):
    
    # 音声クエリのリクエスト
    response_audio = requests.post(f"http://localhost:50021/audio_query?text={text}&speaker={speaker_id}")
    if response_audio.status_code == 200:
        
        # 音声合成のリクエスト
        response_synthesis = requests.post(f"http://localhost:50021/synthesis?speaker={speaker_id}", json=response_audio.json())
        if response_synthesis.status_code == 200:
            
            # バイナリデータを取得
            data_binary = response_synthesis.content
            
            # 一時ファイルに保存
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                temp_wav.write(data_binary)
                temp_wav.flush()  # 確実に書き込む
                
                # 一時ファイルから音声を読み込み再生
                sound = AudioSegment.from_wav(temp_wav.name)
                
                # simpleaudioで再生
                play_obj = sa.play_buffer(sound.raw_data, 
                                          num_channels=sound.channels,
                                          bytes_per_sample=sound.sample_width,
                                          sample_rate=sound.frame_rate)
                play_obj.wait_done()  # 再生完了を待つ
